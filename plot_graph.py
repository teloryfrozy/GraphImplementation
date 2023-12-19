import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import yfinance as yf
from io import StringIO
import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm




url = "https://en.wikipedia.org/wiki/Nasdaq-100"

# Fetch HTML content from the URL
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table with id="constituents"
constituents_table = soup.find('table', {'id': 'constituents'})

if constituents_table:
    # Convert the HTML code table to a string
    table_str = str(constituents_table)
    # wrap the table into a 
    table_file = StringIO(table_str)
    # Convert the found table to DataFrame
    df = pd.read_html(table_file)[0]

    # List of all symbol of stocks in NASDAQ 100
    symbols = list(df["Ticker"])
else:
    print("No table found with id='constituents'.")


frames, edgelist = [], []
# creation of a loading bar
#with tqdm(total=len(symbols)-1,  unit="%", bar_format='{percentage:3.0f}%|{bar}|') as pbar:
for symbol in symbols:
        var = yf.Ticker(symbol)
        print(symbol)
        # top 10 share holders
        frame = var.institutional_holders

        edgelist.append(frame.iloc[0]['Value']/50_000_000_000)
        frame['Company'] = var.ticker
        frames.append(frame)
        # update progress bar for each symbol
        #pbar.update(1)


all_together = pd.concat(frames)#[:30]
print(all_together, len(all_together))

print(edgelist)

G = nx.from_pandas_edgelist(all_together, 'Holder', 'Company')


colors = []
for node in G:
    if node in all_together['Company'].values:
        colors.append("red")
    else:
        colors.append("green")



    


#width=[v[2]['Value']/50_000_000_000 for v in edgelist]

nx.draw_spring(G,
        with_labels=True,
        node_color=colors,
        node_size=[v * 100 for v in dict(G.degree()).values()],     
        width=edgelist,
        edgecolors='black',
        linewidths=1.5   
        )

plt.get_current_fig_manager().full_screen_toggle()
plt.show()