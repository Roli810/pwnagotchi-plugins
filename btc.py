import logging
import time
import requests
import json
import os
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK

class BitcoinPrice(plugins.Plugin):
    __author__ = 'Roli810'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Displays the current Bitcoin price in USD'
    
    PRICE_FILE = 'bitcoin_price.json'  # Path to save the price

    def on_loaded(self):
        logging.info("BitcoinPrice plugin loaded.")
        self.last_update = 0  # Track the last update time
        self.price = self.load_price()  # Load price from file

    def load_price(self):
        """Load the Bitcoin price from a file."""
        if os.path.exists(self.PRICE_FILE):
            with open(self.PRICE_FILE, 'r') as f:
                try:
                    data = json.load(f)
                    return data.get('price', 'Loading...')
                except json.JSONDecodeError:
                    logging.error("Failed to decode JSON from price file.")
        return 'Loading...'

    def save_price(self, price):
        """Save the Bitcoin price to a file."""
        with open(self.PRICE_FILE, 'w') as f:
            json.dump({'price': price}, f)

    def on_ui_setup(self, ui):
        # Position the text based on your screen type or set custom position
        position = (10, 100)  # Adjust x, y for your screen layout
        ui.add_element(
            'bitcoin_price',
            LabeledValue(
                color=BLACK,
                label='BTC: $',
                value=self.price,  # Use loaded price here
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
                self.save_price(price)  # Save the price to file
                self.last_update = current_time  # Update the last fetch time
            except Exception as e:
                logging.error(f"Failed to fetch Bitcoin price: {e}")
