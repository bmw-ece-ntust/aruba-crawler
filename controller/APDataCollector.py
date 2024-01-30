from dotenv import load_dotenv
import datetime
import time
import requests
import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

from Aruba_API.session_controller import get_aruba_id
from Aruba_API.show_command import list_show_command
from Aruba_API.parse_data import parse_data
from utils.hashing import create_hash
from utils.write_data_to_influxdb import influxdb_instance_for_ArubaAPI

load_dotenv()

class APDataCollector:
    """Collects and stores data from Aruba APs.

    This class is responsible for collecting data from Aruba Access Points (APs), processing it, and storing it
    in a database.

    Args:
        ap_names (list[str]): List of AP names to collect data from.
        aruba_username (str): Aruba controller username.
        aruba_password (str): Aruba controller password.
        aruba_ipaddress (str): Aruba controller IP address.

    Methods:
        get_aruba_token(): Get the Aruba access token.
        get_ap_data(token, ap_name): Get AP data from Aruba controller.
        get_eirp_data(token, ap_name): Get EIRP data from Aruba controller.
        collect_data(): Collect the data from APs.
        store_data_to_ComputerCenter_influxdb(): Store AP data to InfluxDB in Computer Center.
        store_data_to_IoTserver_influxdb(): Store AP data to InfluxDB in BMWLab IoT Server.
    """

    def __init__(self):
        """Initialize the APDataCollector instance."""
        # Aruba controller 248
        self.ap_names = ['IY_B1F_AP01','IY_B1F_AP03','IY_B1F_AP05','IY_1F_AP01','IY_1F_AP03','IY_1F_AP05','IY_1F_AP07']
        self.ARUBA_USERNAME = os.getenv('Controller_248_account')
        self.ARUBA_PASSWORD = os.getenv('Controller_248_password')
        self.ARUBA_IPADDRESS = os.getenv('Controller_248_url')
        
        # InfluxDB connection info
        self.ComputerCenter_influxdb_url = os.getenv('InfluxDB_ComputerCenter_url')
        self.IoTServer_influxdb_url = os.getenv('InfluxDB_IoTserver_url')

    def get_aruba_token(self):
        """Get the Aruba access token.

        Returns:
            str or None: Aruba access token, or None if an error occurred.
        """
        try:
            token = get_aruba_id(
                self.ARUBA_IPADDRESS,
                self.ARUBA_USERNAME,
                self.ARUBA_PASSWORD
            )
            return token
        except Exception as e:
            print("[ERROR] Error getting Aruba token:", e)
            return None

    def get_ap_data(self, token, ap_name):
        """Get AP data from Aruba controller.

        Args:
            token (str): Aruba access token.
            ap_name (str): AP name to retrieve data for.

        Returns:
            dict or None: AP data dictionary, or None if an error occurred.
        """
        try:
            command = 'show+ap+monitor+ap-list+ap-name+' + ap_name
            list_ap_database = list_show_command(
                self.ARUBA_IPADDRESS, token, command)
            return list_ap_database
        except Exception as e:
            print("[ERROR] Error getting AP data:", e)
            return None

    def get_eirp_data(self, token, ap_name):
        """Get EIRP data from Aruba controller.

        Args:
            token (str): Aruba access token.
            ap_name (str): AP name to retrieve EIRP data for.

        Returns:
            tuple: A tuple containing radio 0 EIRP and radio 1 EIRP, or empty strings if an error occurred.
        """
        try:
            command = 'show+ap+active+details'
            eirptest = list_show_command(self.ARUBA_IPADDRESS, token, command)
            for ap in eirptest['Active AP Table']:
                if ap['Name'] == ap_name:
                    return ap['Radio 0 Band Ch/EIRP/MaxEIRP/Clients'], ap['Radio 1 Band Ch/EIRP/MaxEIRP/Clients']
            return '', ''
        except requests.exceptions.ConnectionError as ConnectionError:
            print(f"[ERROR] Unexpected Connection Error Encountered! \n {ConnectionError}")
            return '', ''
        except Exception as e:
            print("[ERROR] Error getting EIRP data:", e)
            return '', ''

    def collect_ap_data(self):
        """
        Collects data from Aruba APs.

        This method performs the following steps:
        1. Retrieves an Aruba token for authentication.
        2. If the token is unavailable, it waits for 5 seconds.
        3. Iterates through each AP name to collect data.
        4. Processes and augments the collected AP data.
        5. Handles exceptions and logs errors if they occur.

        Returns:
            List or None: AP data in the AP list, or None if an error occurred. 
        """


        data_rows = {}
        token = self.get_aruba_token()
        retries = 5
        count = 0
        ap_data_total = []
        if token is None:
            print("[INFO] No Aruba token available. Waiting for 5 seconds...")
            time.sleep(5)

        for ap_name in self.ap_names:
            list_ap_database = self.get_ap_data(token, ap_name)

            for ap in list_ap_database['Monitored AP Table']:
                ap['bssid_hashing'] = create_hash(ap['bssid'])
                
            # Should there be a request error, handles the error by retrying to fetch EIRP data
            for _ in range(retries):
                try:
                    radio0_eirp, radio1_eirp = self.get_eirp_data(token, ap_name)
                    break
                except requests.exceptions.ConnectionError as ConnectionError:
                    print(f"[WARNING] Connection Error Encountered. Retrying ...")
                    time.sleep(5)
                except Exception as e:
                    print("[ERROR] An Unknown Error Encountered ", e)
                    break
                finally:
                    pass
            
            list_ap_database['Radio0_EIRP'] = radio0_eirp
            list_ap_database['Radio1_EIRP'] = radio1_eirp

            try:
                list_ap_database['count'] = count
                list_ap_database['timestamp'] = datetime.datetime.now()
                list_ap_database['ap_name'] = ap_name

                #print("[INFO] Inserting raw documents into 'raw_crawl' collection")

                #self.database.insert_raw_documents('raw_crawl', list_ap_database)

                ap_data = list_ap_database['Monitored AP Table']

                for monitored_ap in ap_data:
                    monitored_ap['ap_name'] = ap_name
                    monitored_ap['timestamp'] = time.time()
                    monitored_ap['count'] = count
                    essid = monitored_ap['essid']

                    if 'band/chan/ch-width/ht-type' in monitored_ap:
                        band, chan, ch_width, ht_type = parse_data(
                            monitored_ap['band/chan/ch-width/ht-type'])
                    else:
                        chan = monitored_ap['chan']
                        band = ''

                    rssi_key = f"rssi_{ap_name}"

                    if (essid, chan) not in data_rows:
                        data_rows[(essid, chan)] = {
                            'count': count, 'bssid': monitored_ap['bssid'], 'chan': chan, 'band': band}

                    data_rows[(essid, chan)][rssi_key] = monitored_ap['curr-rssi']
                    
                
            except requests.exceptions.ConnectionError as ConnectionError:
                print(f"[ERROR] Unexpected Connection Error Encountered! \n {ConnectionError}")
            except Exception as e:
                print("[ERROR] An error occurred:", e)
            
            ap_data_total.append(list_ap_database)
        
        time.sleep(5)
        count += 1
        return ap_data_total
    
    def store_data_to_ComputerCenter_influxdb(self, ap_data):
        
        # Instantiate the InfluxDB API
        client = influxdb_instance_for_ArubaAPI(url=self.ComputerCenter_influxdb_url, token="8gI7PJtbvzURdS_ASOG1jG2j9lNWPBjBWSNgUZawnoo3KYFF5tTXiVhBwF392OUClDJDZiZK5hmKJk6L-jwrrQ==", org="ian", bucket="ap")
        write_api = client.instantiate_write_api()
        
        # Write the AP RSSI to InfluxDB
        client.write_wifi_ap_rssi_to_ComputerCenter_influxdb(write_api, ap_data)
        
        # Write the AP EIRP to InfluxDB
        client.write_wifi_ap_eirp_to_influxdb(write_api, ap_data)
        
        # Close the InfluxDB API
        client.close_influxdb_api(write_api)
    
    def store_data_to_IoTserver_influxdb(self, ap_data):
        
        # Instantiate the InfluxDB API
        client = influxdb_instance_for_ArubaAPI(url=self.IoTServer_influxdb_url, token="lRr8ngrKAlyseejkmzhlNOpx0G-jXFAQ2ljtCvSZpKU3fgd2hJQGD-5mI53RDnIs7AyljM73g43Y5nxTCD6gtA==", org="ian", bucket="ap")
        write_api = client.instantiate_write_api()
        
        # Write the AP RSSI to InfluxDB
        client.write_wifi_ap_rssi_to_IoTserver_influxdb(write_api, ap_data)
        
        # Write the AP EIRP to InfluxDB
        client.write_wifi_ap_eirp_to_influxdb(write_api, ap_data)
        
        # Close the InfluxDB API
        client.close_influxdb_api(write_api)
    
