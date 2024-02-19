import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))

from utils.Web_Crawling.parse_data_from_dashboard import parse_aruba_data_to_dataframe
from utils.Web_Crawling.handle_client_data import handle_client_data_value
import requests

def get_aruba_client248_249_data(ip_addr, cookie):
    '''
    get_aruba_client_data: Returns all of Client data in Aruba controller 
        Parameters:
            - url       : URL of Aruba dashboard website
            - account   : User account
    '''
    payload_parameter = 'sta_mac_address client_ip_address client_user_name client_role_name client_health ssid ap_name channel radio_band bssid speed snr total_data_bytes avg_data_rate tx_bytes_transmitted rx_data_bytes total_data_throughput'
    params = {
        'dashboard_url': 'https://' + ip_addr + ':4343/screens/cmnutil/execUiQuery.xml',
        'payload': 'query=<aruba_queries><query><qname>backend-observer-sta-13</qname><type>list</type><list_query><device_type>sta</device_type><requested_columns>' + payload_parameter +'</requested_columns><sort_by_field>client_ip_address</sort_by_field><sort_order>asc</sort_order><pagination><start_row>0</start_row><num_rows>200</num_rows></pagination></list_query><filter><global_operator>and</global_operator><filter_list><filter_item_entry><field_name>client_conn_type</field_name><comp_operator>not_equals</comp_operator><value><![CDATA[0]]></value></filter_item_entry></filter_list></filter></query></aruba_queries>&UIDARUBA=' + cookie,
        'dashboard_cookie' : {"SESSION": cookie},
        'headers': {'Content-Type': 'text/plain'}
    }

    aruba_client_raw_data = requests.post(params['dashboard_url'],
                                  data=params['payload'].encode('utf-8'),
                                  cookies=params['dashboard_cookie'],
                                  headers=params['headers'],
                                 verify=False
                                  )

    status_code = aruba_client_raw_data.status_code

    if status_code != 200:
        print("Error Status Code: ", status_code)
    else:
        print("Successfully Retrieved the raw data of Aruba Clients")
    
    aruba_client_data_dataframe = parse_aruba_data_to_dataframe(aruba_client_raw_data.text)
    aruba_client_data = handle_client_data_value(aruba_client_data_dataframe)
        
    return aruba_client_data

def get_aruba_client251_252_data(ip_addr, cookie):
    '''
    get_aruba_client_data: Returns all of Client data in Aruba controller 
        Parameters:
            - url       : URL of Aruba dashboard website
            - account   : User account
    '''
    payload_parameter = 'sta_mac_address client_ip_address client_user_name client_role_name client_health ssid ap_name channel radio_band bssid speed snr total_data_bytes avg_data_rate tx_bytes_transmitted rx_data_bytes total_data_throughput'
    client_number_range = 2000
    aruba_client_data_tmp = []
    aruba_client_data_total = []
    
    # A maximum of 150 records can be obtained per request
    for data_index in range(0,client_number_range,150):
        params = {
            'dashboard_url': 'https://' + ip_addr + ':4343/screens/cmnutil/execUiQuery.xml',
            'payload': 'query=<aruba_queries xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="/screens/monxml/monitoring_schema.xsd"><query><qname>comp_nw_client_tbl</qname><type>list</type><list_query><device_type>sta</device_type><requested_columns>' + payload_parameter +'</requested_columns><sort_by_field>total_data_throughput</sort_by_field><sort_order>desc</sort_order><pagination><key_value></key_value><start_row>' + str(data_index) + '</start_row><num_rows>150</num_rows></pagination></list_query></query></aruba_queries>&UIDARUBA=' + cookie,
            'dashboard_cookie' : {"SESSION": cookie},
            'headers': {'Content-Type': 'text/plain'}
        }
    
        aruba_client_raw_data = requests.post(params['dashboard_url'],
                                      data=params['payload'].encode('utf-8'),
                                      cookies=params['dashboard_cookie'],
                                      headers=params['headers'],
                                     verify=False
                                      )
    
        status_code = aruba_client_raw_data.status_code
    
        if status_code != 200:
            print("Error Status Code: ", status_code)
        else:
            print("Successfully Retrieved the raw data of Aruba Clients")
        
        aruba_client_data_dataframe = parse_aruba_data_to_dataframe(aruba_client_raw_data.text)
        aruba_client_data = handle_client_data_value(aruba_client_data_dataframe)
        aruba_client_data_tmp.append(aruba_client_data)
    
    # Combine data per request
    for data_merge_index in range(0,int(client_number_range/150)):
        if len(aruba_client_data_tmp[data_merge_index]) > 0:
            aruba_client_data_total.extend(aruba_client_data_tmp[data_merge_index])
       
    return aruba_client_data_total
