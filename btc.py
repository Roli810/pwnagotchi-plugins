import logging
import time
import json
import requests
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK

class BitcoinPrice(plugins.Plugin):
    __author__ = 'YourName'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Displays the current Bitcoin price in USD'
    
    def on_loaded(self):
        logging.info("BitcoinPrice plugin loaded.")
        self.last_update = 0  # Track the last update time
        self.price_file = '/root/bitcoin_price.json'  # Path to save the price

    def save_price(self, price):
        # Save the price to a JSON file
        with open(self.price_file, 'w') as f:
            json.dump({'price': price}, f)

    def load_price(self):
        # Load the price from the JSON file
        try:
            with open(self.price_file, 'r') as f:
                data = json.load(f)
                return data.get('price', 'N/A')
        except (FileNotFoundError, json.JSONDecodeError):
            return 'N/A'  # Return 'N/A' if the file doesn't exist or is empty

    def on_ui_setup(self, ui):
        # Position the text based on your screen type or set custom position
        position = (10, 100)  # Adjust x, y for your screen layout
        ui.add_element(
            'bitcoin_price',
            LabeledValue(
                color=BLACK,
                label='BTC: $',
                value='Loading...',
                position=position,
                label_font=fonts.Small,
                text_font=fonts.Small,
            )
        )

    def on_ui_update(self, ui):
        current_time = time.time()
        # Check if 30 seconds have passed since the last update
        if current_time - self.last_update >= 30:
            try:
                # Fetch current Bitcoin price from CoinDesk API
                response = requests.get("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
                data = response.json()
                price = data['bpi']['USD']['rate']
                ui.set('bitcoin_price', price)
                logging.info(f"Updated Bitcoin price: {price}")
                self.save_price(price)  # Save the fetched price
                self.last_update = current_time  # Update the last fetch time
            except requests.ConnectionError:
                logging.error("No internet connection. Loading last known price.")
                price = self.load_price()  # Load last known price
                ui.set('bitcoin_price', price)  # Set the UI to display the last known price
            except Exception as e:
                logging.error(f"Failed to fetch Bitcoin price: {e}")

