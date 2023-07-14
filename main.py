import requests
from tabulate import tabulate

# Define the API endpoint URL
url = "https://fapi.binance.com/fapi/v1/depth"

# Define the symbol and optional limit
symbol = "BTCUSDT"
limit = 100

# Define the parameters for the API request
params = {
    "symbol": symbol,
    "limit": limit
}

# Send GET request to retrieve the order book data
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    data = response.json()

    # Access the bids and asks from the response
    bids = data["bids"]
    asks = data["asks"]

    # Filter bids and asks with quantity > 25
    filtered_bids = [(price, quantity) for price, quantity in bids if float(quantity) > 10]
    filtered_asks = [(price, quantity) for price, quantity in asks if float(quantity) > 10]

    # Sort filtered bids and asks by quantity
    sorted_filtered_bids = sorted(filtered_bids, key=lambda x: float(x[1]), reverse=True)
    sorted_filtered_asks = sorted(filtered_asks, key=lambda x: float(x[1]), reverse=True)

    # Prepare data for tabulate
    bids_table_data = [["Price ($)", "Quantity"]] + sorted_filtered_bids
    asks_table_data = [["Price ($)", "Quantity"]] + sorted_filtered_asks

    # Print the bids and asks tables
    print("Filtered Bids (Quantity > 25):")
    print(tabulate(bids_table_data, headers="firstrow", tablefmt="psql"))
    print()
    print("Filtered Asks (Quantity > 25):")
    print(tabulate(asks_table_data, headers="firstrow", tablefmt="psql"))
else:
    # Handle request error
    print("Error occurred:", response.status_code)
