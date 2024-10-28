import logging
import time
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

    def on_ui_setup(self, ui):
        # Position the text based on your screen type or set custom position
        position = (120, 10)  # Adjust x, y for your screen layout
        ui.add_element(
            'bitcoin_price',
            LabeledValue(
                color=BLACK,
                label='BTC/USD: $',
                value='Loading...',
                position=position,
                label_font=fonts.Small,
                text_font=fonts.Small,
            )
        )

    def on_ui_update(self, ui):
        try:
            # Fetch current Bitcoin price from CoinDesk API
            response = requests.get("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
            time.sleep(20)
            data = response.json()
            price = data['bpi']['USD']['rate']
            ui.set('bitcoin_price', price)
            logging.info(f"Updated Bitcoin price: {price}")
        except Exception as e:
            logging.error(f"Failed to fetch Bitcoin price: {e}")
