from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class influxdb_instance_for_WebCrawling:
    def __init__(self, url: str, org: str, bucket: str, token: str):
        self.uri = url
        self.org = org
        self.bucket = bucket
        self.token = token
        self.influxdb_client = InfluxDBClient(url=url, token=token, org=org)
    
    def instantiate_write_api(self):
      """Instantiates a write API client for InfluxDB.
    
      Args:
        url: The URL of the InfluxDB.
        token: The InfluxDB authentication token.
        org: The InfluxDB organization.
    
      Returns:
        A write API client for InfluxDB.
      """
      write_api = self.influxdb_client.write_api(write_options=SYNCHRONOUS)
      return write_api

    def write_wifi_client_data_to_ComputerCenter_influxdb(self, write_api, client_data):
      """Writes the wifi client data to InfluxDB.
    
      Args:
        write_api: A write API client for InfluxDB.
        bucket: The InfluxDB bucket to write the data to.
        client_data: A list of wifi client data.
    
      Returns:
        None.
      """
    
      for i in range(len(client_data)):
         
        # Create a wifi client Point object
        _client_point = Point("Client")\
                .tag("sta_mac_address", client_data[i]["sta_mac_address"])\
                .tag("client_user_name", client_data[i]["client_user_name"])\
                .tag("ap_name", client_data[i]["ap_name"])\
                .tag("client_ip_address", client_data[i]["client_ip_address"])\
                .tag("bssid", client_data[i]["bssid"])\
                .tag("ssid", client_data[i]["ssid"])\
                .tag("client_role_name", client_data[i]["client_role_name"])\
                .field("client_health", int(client_data[i]["client_health"]))\
                .field("channel", int(client_data[i]["channel"]))\
                .field("radio_band", client_data[i]["radio_band"])\
                .field("speed", int(client_data[i]["speed"]))\
                .field("snr", int(client_data[i]["snr"]))\
                .field("total_data_bytes", int(client_data[i]["total_data_bytes"]))\
                .field("avg_data_rate", int(client_data[i]["avg_data_rate"]))\
                .field("tx_bytes_transmitted", int(client_data[i]["tx_bytes_transmitted"]))\
                .field("rx_data_bytes", int(client_data[i]["rx_data_bytes"]))\
                .field("total_data_throughput", int(client_data[i]["total_data_throughput"]))\
                #.time(client_data[i]["time_stamp"])
    
        # Write the data to InfluxDB
        write_api.write(bucket=self.bucket, record=[_client_point])
                
      print("Finish writing", len(client_data), "WiFi Client data to computer center")
    
    def write_wifi_client_data_to_IoTserver_influxdb(self, write_api, client_data):
      """Writes the wifi client data to InfluxDB.
    
      Args:
        write_api: A write API client for InfluxDB.
        bucket: The InfluxDB bucket to write the data to.
        client_data: A list of wifi client data.
    
      Returns:
        None.
      """
    
      for i in range(len(client_data)):
         
        # Create a wifi client Point object
        _client_point = Point("Client")\
                .tag("sta_mac_address", client_data[i]["sta_mac_address_hashing"])\
                .tag("client_user_name", client_data[i]["client_user_name"])\
                .tag("ap_name", client_data[i]["ap_name"])\
                .tag("client_ip_address", client_data[i]["client_ip_address_hashing"])\
                .tag("bssid", client_data[i]["bssid_hashing"])\
                .tag("ssid", client_data[i]["ssid"])\
                .tag("client_role_name", client_data[i]["client_role_name"])\
                .field("client_health", int(client_data[i]["client_health"]))\
                .field("channel", int(client_data[i]["channel"]))\
                .field("radio_band", client_data[i]["radio_band"])\
                .field("speed", int(client_data[i]["speed"]))\
                .field("snr", int(client_data[i]["snr"]))\
                .field("total_data_bytes", int(client_data[i]["total_data_bytes"]))\
                .field("avg_data_rate", int(client_data[i]["avg_data_rate"]))\
                .field("tx_bytes_transmitted", int(client_data[i]["tx_bytes_transmitted"]))\
                .field("rx_data_bytes", int(client_data[i]["rx_data_bytes"]))\
                .field("total_data_throughput", int(client_data[i]["total_data_throughput"]))\
                #.time(client_data[i]["time_stamp"])
    
        # Write the data to InfluxDB
        write_api.write(bucket=self.bucket, record=[_client_point])
                
      print("Finish writing", len(client_data), "WiFi Client data to IoT Server")    
    
    def write_wifi_ap_data_to_influxdb(self, write_api, ap_data):
      """Writes the wifi AP data to InfluxDB.
    
      Args:
        write_api: A write API client for InfluxDB.
        bucket: The InfluxDB bucket to write the data to.
        ap_data: A list of wifi AP data.
    
      Returns:
        None.
      """
    
      for i in range(len(ap_data)):

              # Create a wifi AP Point object
              _ap_point = Point("AP")\
                      .tag("ap_name", ap_data[i]["ap_name"])\
                      .tag("radio_band", ap_data[i]["radio_band"])\
                      .tag("ap_group_building", ap_data[i]["ap_group_building"])\
                      .tag("channel", ap_data[i]["channel_str"])\
                      .tag("ap_group_floor", ap_data[i]["ap_group_floor"])\
                      .field("total_data_bytes", int(ap_data[i]["total_data_bytes"]))\
                      .field("radio_mode", int(ap_data[i]["radio_mode"]))\
                      .field("eirp_10x", int(ap_data[i]["eirp_10x"]))\
                      .field("max_eirp", int(ap_data[i]["max_eirp"]))\
                      .field("noise_floor", int(ap_data[i]["noise_floor"]))\
                      .field("arm_ch_qual", int(ap_data[i]["arm_ch_qual"]))\
                      .field("sta_count", int(ap_data[i]["sta_count"]))\
                      .field("rx_time", ap_data[i]["rx_time"])\
                      .field("tx_time", ap_data[i]["tx_time"])\
                      .field("channel_interference", ap_data[i]["channel_interference"])\
                      .field("channel_free", ap_data[i]["channel_free"])\
                      .field("channel_busy", ap_data[i]["channel_busy"])\
                      .field("avg_data_rate", int(ap_data[i]["avg_data_rate"]))\
                      .field("tx_avg_data_rate", int(ap_data[i]["tx_avg_data_rate"]))\
                      .field("rx_avg_data_rate", int(ap_data[i]["rx_avg_data_rate"]))\
                      .field("ap_quality", int(ap_data[i]["ap_quality"]))\
                      .field("rx_data_bytes", int(ap_data[i]["rx_data_bytes"]))\
                      .field("arm_ch_qual", int(ap_data[i]["arm_ch_qual"]))
                      #.time(ap_data[i]["time_stamp"])
                      
              #Write the data to InfluxDB
              write_api.write(self.bucket, record=[_ap_point])
                    
      print("Finish writing", len(ap_data), "WiFi AP data")
    
    def close_influxdb_api(self, write_api):
        """
        Closes the InfluxDB write API and client.
    
        Args:
            write_api: An InfluxDB write API object.
            client: An InfluxDB client object.
        """
        self.influxdb_client.close()
        write_api.close()
        
        
class influxdb_instance_for_ArubaAPI:
    def __init__(self, url: str, org: str, bucket: str, token: str):
        self.uri = url
        self.org = org
        self.bucket = bucket
        self.token = token
        self.influxdb_client = InfluxDBClient(url=url, token=token, org=org)
    
    def instantiate_write_api(self):
      """Instantiates a write API client for InfluxDB.
    
      Args:
        url: The URL of the InfluxDB.
        token: The InfluxDB authentication token.
        org: The InfluxDB organization.
    
      Returns:
        A write API client for InfluxDB.
      """
      write_api = self.influxdb_client.write_api(write_options=SYNCHRONOUS)
      return write_api     
    
    
    
    def write_wifi_ap_rssi_to_ComputerCenter_influxdb(self, write_api, ap_data):
      """Writes the wifi AP data to InfluxDB.
    
      Args:
        write_api: A write API client for InfluxDB.
        bucket: The InfluxDB bucket to write the data to.
        ap_data: A list of wifi AP data.
    
      Returns:
        None.
      """

      for i in range(len(ap_data)):
          for j in range(len(ap_data[i]['Monitored AP Table'])):
              # Create a wifi AP Point object
              _ap_point = Point("IY_RSSI")\
                      .tag("ap_name", ap_data[i]['Monitored AP Table'][j]['ap_name'])\
                      .tag("ap_type", ap_data[i]['Monitored AP Table'][j]['ap-type'])\
                      .tag("bssid", ap_data[i]['Monitored AP Table'][j]['bssid'])\
                      .tag("essid", ap_data[i]['Monitored AP Table'][j]['essid'])\
                      .tag("phy_type", ap_data[i]['Monitored AP Table'][j]['phy-type'])\
                      .field("curr-rssi", int(ap_data[i]['Monitored AP Table'][j]['curr-rssi']))\
                      .field("curr-snr", int(ap_data[i]['Monitored AP Table'][j]['curr-snr']))\
                      #.time(ap_data[i]["time_stamp"])
        
              #Write the data to InfluxDB
              write_api.write("ap", record=[_ap_point])
                    
      print("Finish writing", len(ap_data), "WiFi AP - RSSI")
   
      
    def write_wifi_ap_rssi_to_IoTserver_influxdb(self, write_api, ap_data):
      """Writes the wifi AP data to InfluxDB.
    
      Args:
        write_api: A write API client for InfluxDB.
        bucket: The InfluxDB bucket to write the data to.
        ap_data: A list of wifi AP data.
    
      Returns:
        None.
      """

      for i in range(len(ap_data)):
          for j in range(len(ap_data[i]['Monitored AP Table'])):
              # Create a wifi AP Point object
              _ap_point = Point("IY_RSSI")\
                      .tag("ap_name", ap_data[i]['Monitored AP Table'][j]['ap_name'])\
                      .tag("ap_type", ap_data[i]['Monitored AP Table'][j]['ap-type'])\
                      .tag("bssid", ap_data[i]['Monitored AP Table'][j]['bssid_hashing'])\
                      .tag("essid", ap_data[i]['Monitored AP Table'][j]['essid'])\
                      .tag("phy_type", ap_data[i]['Monitored AP Table'][j]['phy-type'])\
                      .field("curr-rssi", int(ap_data[i]['Monitored AP Table'][j]['curr-rssi']))\
                      .field("curr-snr", int(ap_data[i]['Monitored AP Table'][j]['curr-snr']))\
                      #.time(ap_data[i]["time_stamp"])
        
              #Write the data to InfluxDB
              write_api.write("ap", record=[_ap_point])
                    
      print("Finish writing", len(ap_data), "WiFi AP - RSSI")     

    def write_wifi_ap_eirp_to_influxdb(self, write_api, ap_data):
      """Writes the wifi AP data to InfluxDB.
    
      Args:
        write_api: A write API client for InfluxDB.
        bucket: The InfluxDB bucket to write the data to.
        ap_data: A list of wifi AP data.
    
      Returns:
        None.
      """

      for i in range(len(ap_data)):

              # Create a wifi AP Point object - 2.4GHZ
              _ap_point = Point("IY_EIRP")\
                      .tag("ap_name", ap_data[i]['ap_name'])\
                      .tag("radio_band", ap_data[i]['Radio0_EIRP'].split("/")[0])\
                      .field("eirp", float(ap_data[i]['Radio0_EIRP'].split("/")[1]))\
                      .field("max_eirp", float(ap_data[i]['Radio0_EIRP'].split("/")[2]))\
                      .field("client_number", int(ap_data[i]['Radio0_EIRP'].split("/")[3]))\
                      #.time(ap_data[i]["time_stamp"])
        
              #Write the data to InfluxDB
              write_api.write("ap", record=[_ap_point])
              
              # Create a wifi AP Point object - 5GHZ
              _ap_point = Point("IY_EIRP")\
                      .tag("ap_name", ap_data[i]['ap_name'])\
                      .tag("radio_band", ap_data[i]['Radio1_EIRP'].split("/")[0])\
                      .field("eirp", float(ap_data[i]['Radio1_EIRP'].split("/")[1]))\
                      .field("max_eirp", float(ap_data[i]['Radio1_EIRP'].split("/")[2]))\
                      .field("client_number", int(ap_data[i]['Radio1_EIRP'].split("/")[3]))\
                      #.time(ap_data[i]["time_stamp"])
        
              #Write the data to InfluxDB
              write_api.write("ap", record=[_ap_point])
                    
      print("Finish writing", len(ap_data), "WiFi AP - EIRP")
    
    def close_influxdb_api(self, write_api):
        """
        Closes the InfluxDB write API and client.
    
        Args:
            write_api: An InfluxDB write API object.
            client: An InfluxDB client object.
        """
        self.influxdb_client.close()
        write_api.close()    
        
        