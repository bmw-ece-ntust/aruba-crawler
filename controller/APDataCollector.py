from dotenv import load_dotenv
import datetime
import time
import pandas as pd
import requests
from utils.session_controller import get_aruba_id
from utils.show_command import list_show_command
from controller.Database import Database
from test_ap.show_command_test import list_show_command_test
from utils.parse_data import parse_data
from utils.hashing import create_hash
from controller.Database import DatabaseInterface

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
        database (DatabaseInterface): An instance of the DatabaseInterface for database operations.

    Methods:
        get_aruba_token(): Get the Aruba access token.
        get_ap_data(token, ap_name): Get AP data from Aruba controller.
        get_eirp_data(token, ap_name): Get EIRP data from Aruba controller.
        collect_and_store_data(): Collect and store data from APs iteratively.
    """

    def __init__(self, ap_names: list[str], aruba_username: str, aruba_password: str,
                 aruba_ipaddress: str, duration: int, database: DatabaseInterface):
        """Initialize the APDataCollector instance."""
        self.ap_names = ap_names
        self.ARUBA_USERNAME = aruba_username
        self.ARUBA_PASSWORD = aruba_password
        self.ARUBA_IPADDRESS = aruba_ipaddress
        self.duration = duration
        self.database = database

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

    def collect_and_store_data(self):
        """
        Collects data from Aruba APs iteratively and stores it in the database.

        This method performs the following steps:
        1. Establishes a connection to the database.
        2. Enters an infinite loop to collect data periodically.
        3. Retrieves an Aruba token for authentication.
        4. If the token is unavailable, it waits for 5 seconds and continues to the next iteration.
        5. Iterates through each AP name to collect data.
        6. Processes and augments the collected AP data.
        7. Inserts raw documents into the 'raw_crawl' collection.
        8. Formats and inserts individual AP data into the specified collection.
        9. Handles exceptions and logs errors if they occur.
        10. Waits for 5 seconds before starting the next iteration.

        This method facilitates the continuous collection and storage of AP data from Aruba controllers.

        Returns:
            None
        """
        end_time = time.time() + (self.duration * 60)
        self.database.connect()
        collection_name = 'AP'
        count = 0
        while time.time() < end_time:
            data_rows = {}
            token = self.get_aruba_token()
            retries = 5
            if token is None:
                print("[INFO] No Aruba token available. Waiting for 5 seconds...")
                time.sleep(5)
                continue

            print(f"[INFO] Collecting and storing data - Iteration {count}")
            for ap_name in self.ap_names:
                list_ap_database = self.get_ap_data(token, ap_name)

                for ap in list_ap_database['Monitored AP Table']:
                    ap['bssid'] = create_hash(ap['bssid'])

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

                    print(
                        "[INFO] Inserting raw documents into 'raw_crawl' collection")

                    self.database.insert_raw_documents(
                        'raw_crawl', list_ap_database)

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
                        print(f"[INFO] Inserting documents into '{collection_name}' collection")
                        self.database.insert_documents(collection_name, data_rows)
                        
                except requests.exceptions.ConnectionError as ConnectionError:
                    print(f"[ERROR] Unexpected Connection Error Encountered! \n {ConnectionError}")
                except Exception as e:
                    print("[ERROR] An error occurred:", e)
            print("[INFO] Waiting for 5 seconds before the next iteration...")
            time.sleep(5)
            count += 1
