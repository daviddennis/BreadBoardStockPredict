import csv
import requests
import json

with open('data/stock_opening_prices.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader, None)
    
    stock_data_list = []
    
    for row in csv_reader:
        symbol, date, opening_price = row
        stock_data_list.append({
            "Symbol": row[0],
            "Date": row[1],
            "Opening Price": float(row[2]),
        })

response = requests.post("http://127.0.0.1:5000/stocks", json=stock_data_list)
print(response.status_code)
print(json.dumps(response.json(), indent=4))