import logging
import json
import os

class DataLoader:
    """
    A class to load JSON data files and construct analysis prompts for UniFi networks.
    """

    def __init__(self):
        """
        Initializes the DataLoader by setting the data directory to the script's directory.
        """
        self.data_directory = os.path.dirname(os.path.abspath(__file__))
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self._configure_logging()

    def _configure_logging(self):
        """
        Configures logging to display DEBUG messages in the console.
        """
        if not self.logger.handlers:
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def load_json_file(self, filename: str) -> dict:
        """
        Loads a JSON file and returns its content.

        Args:
            filename (str): Name of the JSON file to load.

        Returns:
            dict: Parsed JSON data if successful, None otherwise.
        """
        file_path = os.path.join(self.data_directory, filename)
        self.logger.debug(f"Attempting to load file: {filename} from {file_path}")

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            self.logger.debug(f"Successfully loaded {filename}")
            return data
        except FileNotFoundError:
            self.logger.error(f"File not found: {filename}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from {filename}: {e}")
        return None

    def load_all_data(self) -> dict:
        """
        Loads all required JSON data files.

        Returns:
            dict: Dictionary containing all loaded data.
        """
        filenames = [
            'device_config.json',
            'performance_data.json',
            'wifi_scans.json',
            'rf_environment.json',
            'client_devices.json',
            'historical_data.json',
            'channel_utilization.json'
        ]

        data = {}
        for filename in filenames:
            loaded_data = self.load_json_file(filename)
            data_key = filename.replace('.json', '')
            data[data_key] = loaded_data

        if not all(data.values()):
            self.logger.error("One or more JSON files could not be loaded. Please check the file paths and contents.")
            exit(1)

        return data

    def create_prompt(self, data: dict) -> str:
        """
        Constructs the analysis prompt using the loaded JSON data.

        Args:
            data (dict): Dictionary containing all loaded JSON data.

        Returns:
            str: Formatted prompt string.
        """
        prompt = f"""
            Analyze the UniFi network data and provide optimization recommendations based on the following context:

            Network Context:
            - This is a UniFi network with 100s of total devices, including 3 access points.
            - We want to optimize the network's performance.
            - The following data files are available for analysis:
            1. device_config.json: Contains configuration details of all network devices.
            2. performance_data.json: Includes daily site performance statistics.
            3. wifi_scans.json: Contains WLAN configuration data.
            4. rf_environment.json: Provides RF environment data for access points.
            5. client_devices.json: Lists all client devices connected to the network.
            6. historical_data.json: Contains hourly site statistics for the past 7 days.
            7. channel_utilization.json: Provides channel utilization data.
            
            Please provide very specific recommendations for imporving network performane and security.  For example if high 
            retry rates are detected, please recommend a new channel or new settings for the access points.  If low SNR is detected,
            please recommend a new channel or new settings for the access points.  If high client device is detected, please recommend
            a new channel or new settings for the access points.  
            
            When providing recommendations please use device names so the engineers can easily understand the recommendations.

            Please provide a comprehensive analysis of the network in the following JSON format:

            {{
                "overall_health": "string",
                "potential_issues": ["string", ...],
                "recommendations": ["string", ...],
                "additional_insights": ["string", ...]
            }}
            Here are the data files:

                <<<device_config.json>>>
                {json.dumps(data['device_config'], separators=(',', ':'))}

                <<<performance_data.json>>>
                {json.dumps(data['performance_data'], separators=(',', ':'))}

                <<<wifi_scans.json>>>
                {json.dumps(data['wifi_scans'], separators=(',', ':'))}

                <<<rf_environment.json>>>
                {json.dumps(data['rf_environment'], separators=(',', ':'))}

                <<<client_devices.json>>>
                {json.dumps(data['client_devices'], separators=(',', ':'))}

                <<<historical_data.json>>>
                {json.dumps(data['historical_data'], separators=(',', ':'))}

                <<<channel_utilization.json>>>
                {json.dumps(data['channel_utilization'], separators=(',', ':'))}

            """
        self.logger.debug("Prompt created successfully.")
        return prompt

    def generate_prompt(self) -> str:
        """
        Loads all data and constructs the analysis prompt.

        Returns:
            str: Formatted prompt string.
        """
        data = self.load_all_data()
        prompt = self.create_prompt(data)
        return prompt