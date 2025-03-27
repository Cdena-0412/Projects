import streamlit as st
import requests
import pandas as pd

st.title("Cryptocurrency Price Tracker")

# Instructions for the user
st.write("""
    This is a simple app to track real-time cryptocurrency prices.
    Enter a cryptocurrency symbol (like `bitcoin` for Bitcoin) to see its price, market cap, and volume.
""")

# Get the cryptocurrency symbol from the user
crypto_symbol = st.text_input("Enter cryptocurrency symbol (e.g., 'bitcoin', 'ethereum'):", "bitcoin")

# Convert symbol to lowercase for consistency
crypto_symbol = crypto_symbol.lower()

# Fetch data from CoinGecko API
url = f'https://api.coingecko.com/api/v3/coins/{crypto_symbol}'
response = requests.get(url)

# Check if the response is valid
if response.status_code == 200:
    data = response.json()

    # Check if the coin data is available
    if 'error' not in data:
        # Extract necessary data
        crypto_name = data['name']
        current_price = data['market_data']['current_price']['usd']
        market_cap = data['market_data']['market_cap']['usd']
        volume = data['market_data']['total_volume']['usd']
        price_change_24h = data['market_data']['price_change_percentage_24h']

        # Display the results
        st.write(f"### {crypto_name} ({crypto_symbol.upper()})")
        st.write(f"**Current Price (USD):** ${current_price}")
        st.write(f"**Market Cap (USD):** ${market_cap:,}")
        st.write(f"**24h Price Change:** {price_change_24h:.2f}%")
        st.write(f"**24h Trading Volume (USD):** ${volume:,}")

        # Get historical prices for the past 30 days
        historical_url = f'https://api.coingecko.com/api/v3/coins/{crypto_symbol}/market_chart'
        historical_response = requests.get(historical_url, params={'vs_currency': 'usd', 'days': '30'})
        
        if historical_response.status_code == 200:
            historical_data = historical_response.json()
            prices = historical_data['prices']
            
            # Convert the data to a pandas DataFrame
            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('date', inplace=True)
            
            # Display historical price chart
            st.subheader(f"{crypto_symbol.upper()} Price Over the Last 30 Days")
            st.line_chart(df['price'])
        else:
            st.error("Error fetching historical data. Please try again later.")

    else:
        st.error(f"Coin not found for the symbol '{crypto_symbol}'. Please check the symbol and try again.")
else:
    # Handle 404 and other errors
    if response.status_code == 404:
        st.error(f"Error: CoinGecko could not find data for the symbol '{crypto_symbol}'. Please check the symbol and try again.")
    else:
        st.error(f"Error fetching data from CoinGecko API. Status code: {response.status_code}. Please try again later.")
