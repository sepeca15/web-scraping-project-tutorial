# your app code here
import pandas as pd
import requests
import sqlite3
from bs4 import BeautifulSoup

url = " https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data, "html.parser")

tables = soup.find_all("table")

for index, table in enumerate(tables):
    if "Tesla Quarterly Revenue" in str(table):
        table_index = index

# create a dataframe
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if col != []:
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        tesla_revenue = tesla_revenue.append(
            {"Date": Date, "Revenue": Revenue}, ignore_index=True
        )

tesla_revenue = tesla_revenue[tesla_revenue["Revenue"] != ""]

records = tesla_revenue.to_records(index=False)

print(f"hay estos records :{len(records)}")

list_of_tuples = list(records)

connection = sqlite3.connect("Tesla.db")

cursor = connection.cursor()

# Create table
cursor.execute(
    """CREATE TABLE IF NOT EXISTS revenue
             (Date, Revenue)"""
)

cursor.executemany("INSERT INTO revenue VALUES (?,?)", list_of_tuples)
# Save (commit) the changes
connection.commit()