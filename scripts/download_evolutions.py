import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Get the html content of the website
url = 'https://pokemon.fandom.com/wiki/List_of_Pok%C3%A9mon_by_evolution'
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")

# Find the table
table = soup.find("table", attrs={
    "style": "border-collapse:collapse;", "width": "330", "cellspacing": "0", "cellpadding": "5", "border": "1"})
table_data = table.tbody.find_all("tr")  # contains 3 rows

# First row as header
headers = []
for th in table_data[0].find_all("th"):
    headers.append(th.text.replace('\n', ' ').strip())

headers[0] = 'Pokédex_Number'  # Fix the first column header

# Get all the rows of the table
rows = []
for tr in table_data:
    t_row = []
    for td in tr.find_all("td"):
        t_row.append(td.text.replace('\n', ' ').strip())
    rows.append(t_row)

rows = rows[1:]  # Remove the first row as it is header

# Make a dataframe
df = pd.DataFrame(rows, columns=headers)

# Split into multiple rows if more than one Pokémon in a cell
df = df.set_index('Pokédex_Number').stack().str.split(' ', expand=True).stack().unstack(-2).reset_index(-1, drop=True).\
                                                                                                        reset_index()

# Fill forward the Pokémon name
df['Unevolved Pokémon/Basic Pokémon'] = df['Unevolved Pokémon/Basic Pokémon'].fillna(method='ffill')

# Fill forward the second evolved Pokémon name
df['Second-Evolved/Stage 2'] = df['Second-Evolved/Stage 2'].fillna(method='ffill')

# Remove the first column
df.drop(columns=['Pokédex_Number'], inplace=True)

# Save the dataframe as a csv file
os.makedirs('../data/', exist_ok=True)
os.chdir('../data/')
df.to_csv('evolutions.csv', index=False)
