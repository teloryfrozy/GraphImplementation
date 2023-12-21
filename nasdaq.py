# Introduction to Big Data - NASDAQ100 Stock Graph Plotter
# Inspired by: https://www.youtube.com/watch?v=x6PNcuZk83g

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from requests import get
from io import StringIO
from bs4 import BeautifulSoup
from colorama import Fore, Style
from tqdm import tqdm


################### MERGE SORT ADAPTED ###################
def merge_sorted(left: list, right: list) -> list:
    merged = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i][1] < right[j][1]:
            merged.append([left[i][0], left[i][1]])
            i += 1
        else:
            merged.append([right[j][0], right[j][1]])
            j += 1

    while i < len(left):
        merged.append([left[i][0], left[i][1]])
        i += 1
    while j < len(right):
        merged.append([right[j][0], right[j][1]])
        j += 1
    
    return merged

def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    left = merge_sort(left)
    right = merge_sort(right)
    
    return merge_sorted(left, right)


################### SCRAPING DATA NASDAQ ###################
def get_top_n_stocks(n: int) -> list:
    """Returns the list of the top n biggest market capitalisation of the NASDAQ100"""
    url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    
    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    constituents_table = soup.find('table', {'id': 'constituents'})
    
    if constituents_table:
        table_str = str(constituents_table)
        table_file = StringIO(table_str)
        # Convert table to DataFrame
        df = pd.read_html(table_file)[0]

        # NASDAQ100 stocks
        symbols = list(df["Ticker"])
    else:
        raise ValueError("No table found with id='constituents'.")

    # Retrieve market capitalization of each stock
    comp_ndx = []
    with tqdm(total=len(symbols)-1,  unit="%", bar_format='{percentage:3.0f}%|{bar}|') as pbar:
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            # store market cap for merge sort
            comp_ndx.append([stock, stock.info['marketCap']])
            pbar.update(1)

    comp_ndx = merge_sort(comp_ndx)
    return comp_ndx[len(comp_ndx)-n:]


################### User choices ###################
n = 100
print(f"{Fore.BLUE}Collecting the top {n} stocks by market capitalization from NASDAQ100{Style.RESET_ALL}")
list_stocks = get_top_n_stocks(n)
print(f"{Fore.GREEN}Stocks loaded successfully!{Style.RESET_ALL}")


################### Rescaling Data ###################
total_market_cap = 0
holders_weight = {}
stocks_market_caps = {}

for stock in list_stocks:
    print(f'{Fore.BLUE}[Loading]{Fore.LIGHTRED_EX} {stock[0].info["longName"]} ({stock[0].ticker})')

    stock_market_cap = stock[1]
    total_market_cap += stock_market_cap
    
    try:        
        df = pd.DataFrame(stock[0].institutional_holders)
    except Exception as e:        
        print(Style.RESET_ALL + Fore.RESET)
        raise ValueError(f"An error occurred: {e}")
    
    stocks_market_caps[stock[0].ticker] = stock_market_cap

    # Update holder values based on sample stocks
    for i, holder in enumerate(list(df['Holder'])):
        if holder not in holders_weight.keys():
            holders_weight[holder] = list(df['Value'])[i]
        else:
            holders_weight[holder] += list(df['Value'])[i]

print(Style.RESET_ALL + Fore.RESET)

for holder in holders_weight.keys():
    holders_weight[holder] = holders_weight[holder] / total_market_cap

for stock_market_cap in stocks_market_caps.keys():
    stocks_market_caps[stock_market_cap] = stocks_market_caps[stock_market_cap] / total_market_cap


################### Graph Drawing ###################
G = nx.Graph()

# Adding stocks as nodes with their market cap as node size
for stock, market_cap in stocks_market_caps.items():
    G.add_node(stock, type='stock', size=market_cap)

# Adding holders as nodes with their weights as node size
for holder, weight in holders_weight.items():
    G.add_node(holder, type='holder', size=weight)

# Adding edges between stocks and holders with weights as ownership percentages
for stock in list_stocks:
    df = pd.DataFrame(stock[0].institutional_holders)
    for i, holder in enumerate(list(df['Holder'])):
        ownership_percentage = list(df['Value'])[i] / total_market_cap
        G.add_edge(stock[0].ticker, holder, weight=ownership_percentage)

# Custom the graph
pos = nx.spring_layout(G, k=1.8) # space between nodes
node_sizes = [data['size'] * 200 for _, data in G.nodes(data=True)]
node_colors = ['red' if data['type'] == 'stock' else 'green' for _, data in G.nodes(data=True)]
# edge thickness scaled according to the % of each holder with the stock
edge_weights = [data['weight'] * 100 for _, _, data in G.edges(data=True)]

nx.draw(G,
        pos=pos,
        with_labels=True,
        node_color=node_colors,
        node_size=node_sizes,
        edgecolors='black',
        linewidths=1.5,
        width=edge_weights
        )

plt.title(f'Top {n} Market Cap Stocks in NASDAQ100')
plt.get_current_fig_manager().full_screen_toggle()
plt.show()