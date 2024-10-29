import logging
import requests
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
from time import sleep
import json
short = True
class BitcoinPrice(plugins.Plugin):
    __author__ = 'YourName'
    __version__ = '1.1.0'
    __license__ = 'GPL3'
    __description__ = 'Displays the current Bitcoin price in USD'

    def on_loaded(self):
        logging.info("BitcoinPrice plugin loaded.")
        self.price = "Loading..."
        self.connected = False  # Track connection status

    def on_ui_setup(self, ui):
        position = (0, 44)  # Adjust x, y for your screen layout
        ui.add_element(
            'bitcoin_price',
            LabeledValue(
                color=BLACK,
                label='BTC:',
                value=self.price,
                position=position,
                label_font=fonts.Small,
                text_font=fonts.Small,
            )
        )
        self.update_price(ui)  # Initial price fetch

    def update_price(self, ui):
        try:
            file_path = '/boot/USD.json'  # Path where the JSON will be saved
            url = "https://api.coindesk.com/v1/bpi/currentprice/USD.json"
            download = requests.get(url)

            # Check if the request was successful
            if download.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(download.content)
                logging.info(f"File downloaded and saved to {file_path}")
            else:
                logging.error(f"Failed to download file: {download.status_code}")
                return  # Exit if download fails

            # Load the data from the saved file
            with open(file_path, 'r') as f:
                data = json.load(f)  # Use json.load to read from file

            self.price = data['bpi']['USD']['rate']
            truncated_price = self.truncate_price(self.price)

            self.connected = True  # Set connected to True if successful
            ui.set('bitcoin_price', truncated_price)
            logging.info(f"Fetched Bitcoin price: {truncated_price}")
        except requests.ConnectionError:
            logging.warning("No network connection. Price will not update.")
            file_path = '/boot/USD.json'  # Path where the JSON will be saved
            url = "https://api.coindesk.com/v1/bpi/currentprice/USD.json"
            with open(file_path, 'r') as f:
                data = json.load(f)  # Use json.load to read from file

            self.price = data['bpi']['USD']['rate']
            truncated_price = self.truncate_price(self.price)

            self.connected = True  # Set connected to True if successful
            ui.set('bitcoin_price', truncated_price)
            self.connected = False  # Set connected to False if there's no connection
        except Exception as e:
            logging.error(f"Failed to fetch Bitcoin price: {e}")

    def truncate_price(self, price):
        """Custom formatting based on the price range."""
        price_float = float(price.replace(',', ''))  # Remove commas and convert to float
        if short == True:
            if price_float >= 1000:
                return f"${int(price_float) / 1000:.1f}K"
            else:
                return f"${price_float:,.2f}"
        else:
            
            if price_float >= 1000:
                # Show whole number part only for large prices
                return f"${price}"
            else:
                # For lower prices, show two decimal places
                return f"${price:,.2f}"

    def on_ui_update(self, ui):
        if self.connected:
            self.update_price(ui)  # Update price only if connected
            sleep(30)  # Wait for 30 seconds before the next update

    def on_unload(self, ui):
        ui.remove_element('bitcoin_price')
