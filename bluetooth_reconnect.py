import subprocess
import time
from pwnagotchi import plugins

class BluetoothReconnect(plugins.Plugin):
    __author__ = 'Roli0810'
    __version__ = '1.0.0'
    __description__ = "A plugin that reconnects to bluetooth tethering."
    __help__ = "It reconnects to tethering in case the base reconnect doesn't work"

    def __init__(self):
        super().__init__()
        self.target_device = "MAC ADDRESS"  # Replace with your device's MAC

    def on_loaded(self):
        self.log("Bluetooth Reconnect plugin loaded!")

    def on_internet_available(self, agent):
        self.check_and_reconnect()

    def is_connected(self):
        result = subprocess.run(['bluetoothctl', 'info', self.target_device], capture_output=True, text=True)
        return "Connected: yes" in result.stdout

    def connect_bluetooth(self):
        subprocess.run(['bluetoothctl', 'connect', self.target_device])

    def check_and_reconnect(self):
        if not self.is_connected():
            self.log("Device not connected. Reconnecting...")
            self.connect_bluetooth()