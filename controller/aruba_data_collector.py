import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.getcwd()))

from utils.Web_Crawling.get_aruba_cookie import get_aruba_dashboard_cookie
from utils.Web_Crawling.get_ap_data import get_aruba_ap248_249_data, get_aruba_ap251_252_data
from utils.Web_Crawling.get_client_data import get_aruba_client248_249_data, get_aruba_client251_252_data
from utils.write_data_to_influxdb import influxdb_instance_for_WebCrawling

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
        
        # Aruba controller 251
        self.aruba_controller251_ipaddress = os.getenv('Controller_251_url')
        self.aruba_controller251_username = os.getenv('Controller_251_account')
        self.aruba_controller251_password = os.getenv('Controller_251_password')
        
        # Aruba controller 252
        self.aruba_controller252_ipaddress = os.getenv('Controller_252_url')
        self.aruba_controller252_username = os.getenv('Controller_252_account')
        self.aruba_controller252_password = os.getenv('Controller_252_password')
        
        # Connection Information of InfluxDB in Computer Center
        self.influxdb_ComputerCenter_url = os.getenv('InfluxDB_ComputerCenter_url')
        self.influxdb_ComputerCenter_token = os.getenv('InfluxDB_ComputerCenter_token')
        self.influxdb_ComputerCenter_org = os.getenv('InfluxDB_ComputerCenter_organization')
        self.influxdb_ComputerCenter_bucket = os.getenv('InfluxDB_ComputerCenter_bucket')
        
        # Connection Information of InfluxDB in IoT Server
        self.influxdb_IoTserver_url = os.getenv('InfluxDB_IoTserver_url')
        self.influxdb_IoTserver_token = os.getenv('InfluxDB_IoTserver_token')
        self.influxdb_IoTserver_org = os.getenv('InfluxDB_IoTserver_organization')
        self.influxdb_IoTserver_bucket = os.getenv('InfluxDB_IoTserver_bucket')
        
        
    def get_controller_cookie(self):
        # Aruba controller 248
        ap248_cookie = get_aruba_dashboard_cookie(self.aruba_controller248_ipaddress, self.aruba_controller248_username, self.aruba_controller248_password)
        print("Successfully Retrieved Controller248 Cookie")
        
        # Aruba controller 249
        ap249_cookie = get_aruba_dashboard_cookie(self.aruba_controller249_ipaddress, self.aruba_controller249_username, self.aruba_controller249_password)
        print("Successfully Retrieved Controller249 Cookie")
        
        # Aruba controller 251
        ap251_cookie = get_aruba_dashboard_cookie(self.aruba_controller251_ipaddress, self.aruba_controller251_username, self.aruba_controller251_password)
        print("Successfully Retrieved Controller251 Cookie")
        
        # Aruba controller 252
        ap252_cookie = get_aruba_dashboard_cookie(self.aruba_controller252_ipaddress, self.aruba_controller252_username, self.aruba_controller252_password)
        print("Successfully Retrieved Controller252 Cookie")
        
        return ap248_cookie, ap249_cookie, ap251_cookie, ap252_cookie
    
    def get_ap_data(self, ap248_cookie, ap249_cookie, ap251_cookie, ap252_cookie):
        # Aruba controller 248
        print("Retrieved Controller248 AP data :")
        ap248_data = get_aruba_ap248_249_data(self.aruba_controller248_ipaddress, ap248_cookie)
        
        # Aruba controller 249
        print("Retrieved Controller249 AP data :")
        ap249_data = get_aruba_ap248_249_data(self.aruba_controller249_ipaddress, ap249_cookie)
        
        # Aruba controller 251
        print("Retrieved Controller251 AP data :")
        ap251_data = get_aruba_ap251_252_data(self.aruba_controller251_ipaddress, ap251_cookie)
        
        # Aruba controller 252
        print("Retrieved Controller252 AP data :")
        ap252_data = get_aruba_ap251_252_data(self.aruba_controller252_ipaddress, ap252_cookie)
        
        # Combine them
        ap_data = [*ap248_data, *ap249_data, *ap251_data, *ap252_data]
        
        return ap_data
    
    def get_client_data(self, ap248_cookie, ap249_cookie, ap251_cookie, ap252_cookie):
        # Aruba controller 248
        print("Retrieved Controller248 Client data :")
        client248_data = get_aruba_client248_249_data(self.aruba_controller248_ipaddress, ap248_cookie)
        
        # Aruba controller 249
        print("Retrieved Controller249 Client data :")
        client249_data = get_aruba_client248_249_data(self.aruba_controller249_ipaddress, ap249_cookie)
        
        # Aruba controller 251
        print("Retrieved Controller251 Client data :")
        client251_data = get_aruba_client251_252_data(self.aruba_controller251_ipaddress, ap251_cookie)
        
        # Aruba controller 252
        print("Retrieved Controller252 Client data :")
        client252_data = get_aruba_client251_252_data(self.aruba_controller252_ipaddress, ap252_cookie)
        
        client_data = [*client248_data, *client249_data, *client251_data, *client252_data]
        
        return client_data
        
    def store_data_to_ComputerCenter_influxdb(self, ap_data, client_data):
        
        # Instantiate the InfluxDB API
        client_ComputerCenter = influxdb_instance_for_WebCrawling(url=self.influxdb_ComputerCenter_url, token=self.influxdb_ComputerCenter_token, org=self.influxdb_ComputerCenter_org, bucket=self.influxdb_ComputerCenter_bucket)
        write_api =  client_ComputerCenter.instantiate_write_api()
        
        # Write the AP data to InfluxDB
        client_ComputerCenter.write_wifi_ap_data_to_influxdb(write_api, ap_data)
        
        # Write the Client data to InfluxDB
        client_ComputerCenter.write_wifi_client_data_to_ComputerCenter_influxdb(write_api, client_data)
        
        # Close the InfluxDB API
        client_ComputerCenter.close_influxdb_api(write_api)
        
    def store_data_to_IoTserver_influxdb(self, ap_data, client_data):
        
        # Instantiate the InfluxDB API
        client_IoTserver = influxdb_instance_for_WebCrawling(url=self.influxdb_IoTserver_url, token=self.influxdb_IoTserver_token, org=self.influxdb_IoTserver_org, bucket=self.influxdb_IoTserver_bucket)
        write_api =  client_IoTserver.instantiate_write_api()
        
        # Write the AP data to InfluxDB
        client_IoTserver.write_wifi_ap_data_to_influxdb(write_api, ap_data)
        
        # Write the Client data to InfluxDB
        client_IoTserver.write_wifi_client_data_to_IoTserver_influxdb(write_api, client_data)
        
        # Close the InfluxDB API
        client_IoTserver.close_influxdb_api(write_api)
            
            
    
    
    
    
    
    
    
    