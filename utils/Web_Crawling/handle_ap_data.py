import re
from hashing import create_hash

def handle_ap_data_value(ap_data_dataframe):
    
    '''
    handle_ap_data: Handle empty value & Revise the format 
        Parameters:
            - url       : URL of Aruba dashboard website
            - account   : User account
    '''
    aruba_ap_data_dictformat = ap_data_dataframe.to_dict(orient='records')

    for i in range(len(aruba_ap_data_dictformat)):
        
        # This judgement exists due to delettion of useless AP
        if i == len(aruba_ap_data_dictformat):
            break
            
        # Delete the useless AP (The value of ap_quality is empty => Almost parameter value of this AP are empty)
        if aruba_ap_data_dictformat[i]["ap_quality"] == "":   
            print("Can't crawl the data from the AP ",aruba_ap_data_dictformat[i]["ap_name"])
            # There are two radio band in one AP, so delete twice  
            del aruba_ap_data_dictformat[i]
            del aruba_ap_data_dictformat[i]
        
        # Handle the radio_band 0 (2.4HZ) & 1 (5HZ)
        if aruba_ap_data_dictformat[i]["radio_band"] == "0":
            aruba_ap_data_dictformat[i]["radio_band"] = 2.4
        else:
            aruba_ap_data_dictformat[i]["radio_band"] = float(5)
        
        # Handle the empty value (0 STA means that 0 data rate) to -1 (Just my definition)
        if aruba_ap_data_dictformat[i]["avg_data_rate"] == "":
            aruba_ap_data_dictformat[i]["avg_data_rate"] = -1
        if aruba_ap_data_dictformat[i]["tx_avg_data_rate"] == "":
            aruba_ap_data_dictformat[i]["tx_avg_data_rate"] = -1
        if aruba_ap_data_dictformat[i]["rx_avg_data_rate"] == "":
            aruba_ap_data_dictformat[i]["rx_avg_data_rate"] = -1
        if aruba_ap_data_dictformat[i]["total_data_bytes"] == "":
            aruba_ap_data_dictformat[i]["total_data_bytes"] = -1
            
        # Handle the channel utilization
        aruba_ap_data_dictformat[i]["channel_busy"] = float(int(re.findall("([0-9]+)\/", aruba_ap_data_dictformat[i]["channel_busy"])[0])/60000)
        aruba_ap_data_dictformat[i]["channel_free"] = float(int(re.findall("([0-9]+)\/", aruba_ap_data_dictformat[i]["channel_free"])[0])/60000)
        aruba_ap_data_dictformat[i]["channel_interference"] = float(int(re.findall("([0-9]+)\/", aruba_ap_data_dictformat[i]["channel_interference"])[0])/60000)
        aruba_ap_data_dictformat[i]["rx_time"] = float(int(re.findall("([0-9]+)\/", aruba_ap_data_dictformat[i]["rx_time"])[0])/60000)
        aruba_ap_data_dictformat[i]["tx_time"] = float(int(re.findall("([0-9]+)\/", aruba_ap_data_dictformat[i]["tx_time"])[0])/60000)
        
        # Generate the fields of AP name, building and floor
        aruba_ap_data_dictformat[i]["ap_group_building"] = aruba_ap_data_dictformat[i]["ap_name"].split("_")[0]
        aruba_ap_data_dictformat[i]["ap_group_floor"] = aruba_ap_data_dictformat[i]["ap_name"].split("_")[1]
       
    return aruba_ap_data_dictformat