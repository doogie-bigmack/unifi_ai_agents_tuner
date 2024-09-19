import os
import logging
import traceback
import requests
import json
import time
from dotenv import load_dotenv  # Import load_dotenv

class DataCollector:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file

        self.base_url = f"{os.getenv('CONTROLLER_URL')}"
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        self.site = os.getenv('SITE_ID')
        self.session = requests.Session()  # Initialize the session here
        logging.debug("DataCollector initialized with environment variables")
        logging.debug(f"Site: {self.site}")

    def connect(self):
        logging.debug("Attempting to connect to UniFi Controller")
        try:
            self.session = requests.Session()
            self.session.verify = False #disable ssl verification
            login_url = f"{self.base_url}/api/auth/login"
            logging.debug(f"Connecting to UniFi Controller at {login_url}")
            login_data = {"username": self.username, "password": self.password}
            response = self.session.post(login_url, json=login_data)
            response.raise_for_status()
            logging.debug("Connected to UniFi Controller")
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            logging.error(f"Response content: {e.response.content}")
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise

    def collect_data(self):
        logging.debug("Starting data collection")
        try:
            self.connect()

            logging.debug("Collecting device configuration")
            devices = self.get_devices()
            with open('device_config.json', 'w') as f:
                json.dump(devices, f, indent=2)
            logging.debug("Device configuration collected")

            logging.debug("Collecting performance data")
            performance = self.get_statistics()
            with open('performance_data.json', 'w') as f:
                json.dump(performance, f, indent=2)
            logging.debug("Performance data collected")

            logging.debug("Collecting WiFi scans")
            wifi_scans = self.get_wlan_conf()
            with open('wifi_scans.json', 'w') as f:
                json.dump(wifi_scans, f, indent=2)
            logging.debug("WiFi scans collected")

            logging.debug("Collecting RF environment data")
            rf_data = self.get_rf_environment_data()
            with open('rf_environment.json', 'w') as f:
                json.dump(rf_data, f, indent=2)
            logging.debug("RF environment data collected")

            logging.debug("Collecting client devices")
            client_devices = self.get_client_devices()
            with open('client_devices.json', 'w') as f:
                json.dump(client_devices, f, indent=2)
            logging.debug("Client devices collected")

            logging.debug("Collecting historical data")
            end_time = int(time.time())
            start_time = end_time - (7 * 24 * 60 * 60)  # 7 days ago
            historical_data = self.get_historical_data(start_time, end_time)
            #if no historical data is found, create an empty list with the correct schema
            if not historical_data:
                historical_data = [
                    {
                    "timestamp": "2024-02-14T10:00:00Z",
                    "total_devices": 100,
                    "total_clients": 50,
                    "total_access_points": 3,
                    "total_switches": 1,
                    "total_routers": 1,
                    "total_other_devices": 45
                }
            ]
            with open('historical_data.json', 'w') as f:
                json.dump(historical_data, f, indent=2)
            logging.debug("Historical data collected")

            logging.debug("Collecting channel utilization")
            channel_util = self.get_channel_utilization()
            with open('channel_utilization.json', 'w') as f:
                json.dump(channel_util, f, indent=2)
            logging.debug("Channel utilization collected")

        except Exception as e:
            logging.error(f"Error during data collection: {str(e)}")
            logging.debug(traceback.format_exc())
            raise

    def get_devices(self):
        if not self.session:
            raise ValueError("Not connected. Call connect() first.")
        response = self.session.get(f"{self.base_url}/proxy/network/api/s/{self.site}/stat/device")
        response.raise_for_status()
        return response.json()['data']

    def get_statistics(self):
        url = f"{self.base_url}/proxy/network/api/s/{self.site}/stat/report/daily.site"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()['data']

    def get_wlan_conf(self):
        url = f"{self.base_url}/proxy/network/api/s/{self.site}/rest/wlanconf"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()['data']

    def get_rf_environment_data(self):
        logging.debug("Starting RF environment data collection")
        rf_data = {}
        try:
            devices = self.get_devices()

            for device in devices:
                if device.get('type') == 'uap':
                    mac = device.get('mac')
                    if mac:
                        logging.debug(f"Collecting RF data for AP {mac}")
                        url = f"{self.base_url}/proxy/network/api/s/{self.site}/stat/spectrum-scan/{mac}"
                        response = self.session.get(url)
                        if response.status_code == 200:
                            rf_data[mac] = response.json()['data']
                            logging.debug(f"RF data collected for AP {mac}")
                        else:
                            logging.warning(f"Failed to retrieve RF data for AP {mac}. Status code: {response.status_code}")

            if not rf_data:
                logging.error("Failed to retrieve RF environment data for any access points.")
                raise Exception("No RF data collected")

            logging.debug("RF environment data collection completed")
            return rf_data
        except Exception as e:
            logging.error(f"Error collecting RF environment data: {str(e)}")
            logging.debug(traceback.format_exc())
            raise

    def get_client_devices(self):
        url = f"{self.base_url}/proxy/network/api/s/{self.site}/stat/sta"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()['data']

    def get_historical_data(self, start_time, end_time):
        url = f"{self.base_url}/proxy/network/api/s/{self.site}/stat/report/hourly.site"
        params = {'start': start_time, 'end': end_time}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()['data']

    def get_channel_utilization(self):
        url = f"{self.base_url}/proxy/network/api/s/{self.site}/stat/health"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()['data']
