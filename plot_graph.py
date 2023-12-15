import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import yfinance as yf
from io import StringIO
import pandas as pd
from bs4 import BeautifulSoup
import requests




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



frames = []

for i, symbol in enumerate(symbols):
    var = yf.Ticker(symbol)
    frame = var.institutional_holders
    print(i, symbol, frame)
    frame['Company'] = var.ticker
    
    frames.append(frame)

all_together = pd.concat(frames)
print(all_together)




G = nx.from_pandas_edgelist(all_together, 'Holder', 'Company')


colors = []
for node in G:
    if node in all_together['Company'].values:
        colors.append("red")
    else:
        colors.append("green")





plt.figure(figsize=(50, 40))

    


nx.draw(G, with_labels=True,
        node_color=colors,
        node_size=[v * 100 for v in dict(G.degree()).values()],
        
        )


edgelist = nx.to_edgelist(G)
print(edgelist)

# width=[v[2]['Value']/50_000_000_000 for v in edgelist]
plt.show()
