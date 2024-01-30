import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.getcwd()))

from utils.Web_Crawling.get_aruba_cookie import get_aruba_dashboard_cookie
from utils.Web_Crawling.get_ap_data import get_aruba_ap_data
from utils.Web_Crawling.get_client_data import get_aruba_client_data
from write_data_to_influxdb import influxdb_instance_for_WebCrawling

load_dotenv()

class Controller_data_collector:
    def __init__(self):
        # Aruba controller 248
        self.aruba_controller248_ipaddress = os.getenv('Controller_248_url')
        self.aruba_controller248_username = os.getenv('Controller_248_account')
        self.aruba_controller248_password = os.getenv('Controller_248_password')
        
        # Aruba controller 249
        self.aruba_controller249_ipaddress = os.getenv('Controller_249_url')
        self.aruba_controller249_username = os.getenv('Controller_249_account')
        self.aruba_controller249_password = os.getenv('Controller_249_password')
        
        # InfluxDB connection info
        self.influxdb_url = os.getenv('InfluxDB_ComputerCenter_url')
    
    def get_controller_cookie(self):
        # Aruba controller 248
        ap248_cookie = get_aruba_dashboard_cookie(self.aruba_controller248_ipaddress, self.aruba_controller248_username, self.aruba_controller248_password)
        print("Successfully Retrieved Controller248 Cookie")
        
        # Aruba controller 249
        ap249_cookie = get_aruba_dashboard_cookie(self.aruba_controller249_ipaddress, self.aruba_controller249_username, self.aruba_controller249_password)
        print("Successfully Retrieved Controller249 Cookie")
        
        return ap248_cookie, ap249_cookie
    
    def get_ap_data(self, ap248_cookie, ap249_cookie):
        # Aruba controller 248
        print("Retrieved Controller248 AP data :")
        ap248_data = get_aruba_ap_data(self.aruba_controller248_ipaddress, ap248_cookie)
        
        # Aruba controller 249
        print("Retrieved Controller249 AP data :")
        ap249_data = get_aruba_ap_data(self.aruba_controller249_ipaddress, ap249_cookie)
        
        # Combine them
        ap_data = [*ap248_data, *ap249_data]
        
        return ap_data
    
    def get_client_data(self, ap248_cookie, ap249_cookie):
        # Aruba controller 248
        print("Retrieved Controller248 Client data :")
        client248_data = get_aruba_client_data(self.aruba_controller248_ipaddress, ap248_cookie)
        
        # Aruba controller 249
        print("Retrieved Controller249 Client data :")
        client249_data = get_aruba_client_data(self.aruba_controller249_ipaddress, ap249_cookie)
        
        client_data = [*client248_data, *client249_data]
        
        return client_data
        
    def store_data_to_influxdb(self, ap_data, client_data):
        
        # Instantiate the InfluxDB API
        client = influxdb_instance_for_WebCrawling(url=self.influxdb_url, token="gNZLlI7EMLP3ZxL2DJ2lwo7kyobu0YxTk-Jn9MrJB_e4Z-5nu1E-erotDp1XMxuARkdibvI8koRBCT9uX1YOxw==", org="month", bucket="m1")
        write_api = client.instantiate_write_api()
        
        # Write the AP data to InfluxDB
        client.write_wifi_ap_data_to_influxdb(write_api, ap_data)
        
        # Write the Client data to InfluxDB
        client.write_wifi_client_data_to_influxdb(write_api, client_data)
        
        # Close the InfluxDB API
        client.close_influxdb_api(write_api)
        
    
print()
            
            
    
    
    
    
    
    
    
    