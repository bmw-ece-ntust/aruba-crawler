from controller.aruba_data_collector import Controller_data_collector
from controller.APDataCollector import APDataCollector

def Data_Collector_based_on_WebCrawling():
    # Instantiate the data collector instance
    controller_data_collector = Controller_data_collector()
    
    # Get controller cookie
    controller248_cookie, controller249_cookie, ap251_cookie, ap252_cookie = controller_data_collector.get_controller_cookie()
    
    # Collect the AP data of Controller 248 & 249
    ap_data = controller_data_collector.get_ap_data(controller248_cookie, controller249_cookie, ap251_cookie, ap252_cookie)
    
    # Collect the Client data of Controller 248 & 249
    client_data = controller_data_collector.get_client_data(controller248_cookie, controller249_cookie, ap251_cookie, ap252_cookie)
    
    # Store the data to the InfluxDB in Computer Center 
    controller_data_collector.store_data_to_ComputerCenter_influxdb(ap_data, client_data)
    
    # Store the data to the InfluxDB in IoT Server
    controller_data_collector.store_data_to_IoTserver_influxdb(ap_data, client_data)
    
def AP_Collector_based_on_ArubaAPI():
    # Instantiate the ap collector instance
    ap_data_collector = APDataCollector()
     
    # Get AP data
    ap_data = ap_data_collector.collect_ap_data()
    
    # Store AP data
    print("Computer center:")
    ap_data_collector.store_data_to_ComputerCenter_influxdb(ap_data)
    print("IoT Server:")
    ap_data_collector.store_data_to_IoTserver_influxdb(ap_data)

if __name__ == '__main__':
    print("[INFO] Collect the AP data (RSSI) from Aruba Controller 248")
    AP_Collector_based_on_ArubaAPI()
    print("[INFO] Collect the AP and Client data (No RSSI) from Aruba Controller 248 & 249 & 251 & 252")
    Data_Collector_based_on_WebCrawling()
    


    
