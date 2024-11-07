import threading
import time
import subprocess
import os
from pwnagotchi import plugins

class BluetoothReconnect(plugins.Plugin):
    __author__ = 'Roli0810'
    __version__ = '1.1.0'
    __license__ = 'GPL3'
    
    def __init__(self):
        super().__init__()
        self.target_device = "MAC ADDRESS"  # Replace with your device's MAC
        self.running = True

    def on_loaded(self):
        self.log("Bluetooth Reconnect plugin loaded!")
        # Start a background thread to monitor and reconnect
        self.monitor_thread = threading.Thread(target=self._monitor_bluetooth)
        self.monitor_thread.daemon = True  # Allows thread to exit when Pwnagotchi stops
        self.monitor_thread.start()

    def _monitor_bluetooth(self):
        while self.running:
            if not self._is_connected():
                self.log("Device not connected. Attempting to reconnect...")
                self._connect_bluetooth()
                time.sleep(5)  # Delay after reconnect attempt
            else:
                self.log("Device is connected.")
            
            # Check internet availability by pinging a reliable server (e.g., Google's DNS)
            if not self._is_internet_available():
                self.log("Internet unavailable. Reconnecting Bluetooth...")
                self._connect_bluetooth()

            time.sleep(10)  # Check every 10 seconds

    def _is_connected(self):
        # Check if the Bluetooth device is connected
        result = subprocess.run(['bluetoothctl', 'info', self.target_device], capture_output=True, text=True)
        return "Connected: yes" in result.stdout

    def _connect_bluetooth(self):
        # Attempt to connect using bluetoothctl
        subprocess.run(['bluetoothctl', 'connect', self.target_device])

    def _is_internet_available(self):
        # Check if the internet is available by pinging Google's DNS (8.8.8.8)
        response = os.system("ping -c 1 8.8.8.8")
        return response == 0  # Returns True if ping succeeds, indicating internet is available

    def on_unloaded(self):
        # Stop the monitoring loop when the plugin is unloaded
        self.running = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join()
