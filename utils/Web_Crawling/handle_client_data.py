from hashing import create_hash

def handle_client_data_value(client_data_dataframe):
    
    '''
    handle_ap_data: Handle empty value & Revise the format 
        Parameters:
            - url       : URL of Aruba dashboard website
            - account   : User account
    '''
    aruba_client_data_dictformat = client_data_dataframe.to_dict(orient='records')

    for i in range(len(aruba_client_data_dictformat)):
        
        # This judgement exists due to delettion of useless client
        if i == len(aruba_client_data_dictformat):
            break
            
        # Delete the useless client (The value of client_health is empty => Almost parameter value of this client are empty)
        if aruba_client_data_dictformat[i]["client_health"] == "":   
            print("Can't crawl the data from the user", aruba_client_data_dictformat[i]["client_user_name"] ,"(", aruba_client_data_dictformat[i]["sta_mac_address"], ")") 
            del aruba_client_data_dictformat[i]

        # Handle the radio_band 0 (2.4HZ) & 1 (5HZ)
        if aruba_client_data_dictformat[i]["radio_band"] == "0":
            aruba_client_data_dictformat[i]["radio_band"] = 2.4
        else:
            aruba_client_data_dictformat[i]["radio_band"] = float(5)
        
        # Handle the empty value
        if aruba_client_data_dictformat[i]["client_ip_address"] == "":
            aruba_client_data_dictformat[i]["client_ip_address"] = -1
        if aruba_client_data_dictformat[i]["avg_data_rate"] == "":
            aruba_client_data_dictformat[i]["avg_data_rate"] = -1
        if aruba_client_data_dictformat[i]["tx_bytes_transmitted"] == "":
            aruba_client_data_dictformat[i]["tx_bytes_transmitted"] = -1
        if aruba_client_data_dictformat[i]["rx_data_bytes"] == "":
            aruba_client_data_dictformat[i]["rx_data_bytes"] = -1
        if aruba_client_data_dictformat[i]["total_data_throughput"] == "":
            aruba_client_data_dictformat[i]["total_data_throughput"] = -1
        if aruba_client_data_dictformat[i]["total_data_bytes"] == "":
            aruba_client_data_dictformat[i]["total_data_bytes"] = -1
        if aruba_client_data_dictformat[i]["speed"] == "":
            aruba_client_data_dictformat[i]["speed"] = -1
        if aruba_client_data_dictformat[i]["snr"] == "":
            aruba_client_data_dictformat[i]["snr"] = -1
        
        # De-identify the user privacy
        aruba_client_data_dictformat[i]["client_ip_address_hashing"] = create_hash(aruba_client_data_dictformat[i]["client_user_name"])
        aruba_client_data_dictformat[i]["client_ip_address_hashing"] = create_hash(aruba_client_data_dictformat[i]["client_ip_address"])
        aruba_client_data_dictformat[i]["sta_mac_address_hashing"] = create_hash(aruba_client_data_dictformat[i]["sta_mac_address"])
        aruba_client_data_dictformat[i]["bssid_hashing"] = create_hash(aruba_client_data_dictformat[i]["bssid"])
        
       
    return aruba_client_data_dictformat