from parse_data_from_dashboard import parse_aruba_data_to_dataframe
from handle_ap_data import handle_ap_data_value
import requests

def get_aruba_ap_data(ip_addr, cookie):
    '''
    get_aruba_ap_data: Returns all of AP data in Aruba controller 
        Parameters:
            - url       : URL of Aruba dashboard website
            - account   : User account
    '''
    payload_parameter = 'ap_name radio_band total_data_bytes rx_data_bytes channel_str radio_mode eirp_10x max_eirp noise_floor arm_ch_qual sta_count current_channel_utilization rx_time tx_time channel_interference channel_free channel_busy avg_data_rate tx_avg_data_rate rx_avg_data_rate ap_quality'
    params = {
        'dashboard_url': 'https://' + ip_addr + ':4343/screens/cmnutil/execUiQuery.xml',
        'payload': 'query=<aruba_queries><query><qname>backend-observer-radio-28</qname><type>list</type><list_query><device_type>radio</device_type><requested_columns>' + payload_parameter +'</requested_columns><sort_by_field>ap_name</sort_by_field><sort_order>asc</sort_order><pagination><start_row>0</start_row><num_rows>400</num_rows></pagination></list_query></query></aruba_queries>&UIDARUBA=' + cookie,
        'dashboard_cookie' : {"SESSION": cookie},
        'headers': {'Content-Type': 'text/plain'}
    }

    aruba_ap_raw_data = requests.post(params['dashboard_url'],
                                  data=params['payload'].encode('utf-8'),
                                  cookies=params['dashboard_cookie'],
                                  headers=params['headers'],
                                 verify=False
                                  )

    status_code = aruba_ap_raw_data.status_code

    if status_code != 200:
        print("Error Status Code: ", status_code)
    else:
        print("Successfully Retrieved the raw data of Aruba APs")
    
    # Parse the ap data
    aruba_ap_data_dataframe = parse_aruba_data_to_dataframe(aruba_ap_raw_data.text)
    aruba_ap_data = handle_ap_data_value(aruba_ap_data_dataframe)
    
    return aruba_ap_data


    