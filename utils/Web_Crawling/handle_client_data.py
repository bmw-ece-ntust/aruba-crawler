import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from utils.hashing import create_hash

def handle_client_data_value(client_data_dataframe):
    
    '''
    handle_ap_data: Handle empty value & Revise the format 
        Parameters:
            - url       : URL of Aruba dashboard website
            - account   : User account
    '''
    aruba_client_data_dictformat = client_data_dataframe.to_dict(orient='records')
    data_index = -1
    
    for i in range(len(aruba_client_data_dictformat)):
        data_index = data_index + 1
        
        # This judgement exists due to delettion of useless client
        if data_index == len(aruba_client_data_dictformat):
            break
            
        # Delete the useless client (The value of client_health is empty => Almost parameter value of this client are empty)
        if aruba_client_data_dictformat[data_index]["client_health"] == "":  
            print("Can't crawl the data from the user", aruba_client_data_dictformat[data_index]["client_user_name"] ,"(", aruba_client_data_dictformat[data_index]["sta_mac_address"], ")") 
            del aruba_client_data_dictformat[data_index]
            data_index = data_index - 1
            continue

                  
        # Handle the radio_band 0 (2.4HZ) & 1 (5HZ)
        if aruba_client_data_dictformat[data_index]["radio_band"] == "0":
            aruba_client_data_dictformat[data_index]["radio_band"] = 2.4
        else:
            aruba_client_data_dictformat[data_index]["radio_band"] = float(5)
        
        # Handle the empty value
        if aruba_client_data_dictformat[data_index]["client_ip_address"] == "":
            aruba_client_data_dictformat[data_index]["client_ip_address"] = -1
        if aruba_client_data_dictformat[data_index]["avg_data_rate"] == "":
            aruba_client_data_dictformat[data_index]["avg_data_rate"] = -1
        if aruba_client_data_dictformat[data_index]["tx_bytes_transmitted"] == "":
            aruba_client_data_dictformat[data_index]["tx_bytes_transmitted"] = -1
        if aruba_client_data_dictformat[data_index]["rx_data_bytes"] == "":
            aruba_client_data_dictformat[data_index]["rx_data_bytes"] = -1
        if aruba_client_data_dictformat[data_index]["total_data_throughput"] == "":
            aruba_client_data_dictformat[data_index]["total_data_throughput"] = -1
        if aruba_client_data_dictformat[data_index]["total_data_bytes"] == "":
            aruba_client_data_dictformat[data_index]["total_data_bytes"] = -1
        if aruba_client_data_dictformat[data_index]["speed"] == "":
            aruba_client_data_dictformat[data_index]["speed"] = -1
        if aruba_client_data_dictformat[data_index]["snr"] == "":
            aruba_client_data_dictformat[data_index]["snr"] = -1
        if aruba_client_data_dictformat[data_index]["channel"] == "":
            aruba_client_data_dictformat[data_index]["channel"] = -1
            
        # De-identify the user privacy
        aruba_client_data_dictformat[data_index]["client_ip_address_hashing"] = create_hash(aruba_client_data_dictformat[data_index]["client_user_name"])
        aruba_client_data_dictformat[data_index]["client_ip_address_hashing"] = create_hash(aruba_client_data_dictformat[data_index]["client_ip_address"])
        aruba_client_data_dictformat[data_index]["sta_mac_address_hashing"] = create_hash(aruba_client_data_dictformat[data_index]["sta_mac_address"])
        aruba_client_data_dictformat[data_index]["bssid_hashing"] = create_hash(aruba_client_data_dictformat[data_index]["bssid"])
        
       
    return aruba_client_data_dictformat