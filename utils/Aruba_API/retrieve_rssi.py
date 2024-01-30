from show_command import list_show_command
import pandas as pd

def retrieve_rssi(waps, floor, ap_prefix, aosip, aruba_id, MIN_VAL=0, MAX_VAL=100):
    '''
    retrieve_rssi: Returns a DataFrame that contains WAPs informations
        Parameter:
            - waps      : WAPS List
            - floor     : Building Floor
            - ap_prefix : AP Building Name Prefix e.g IY
            - aosip     : API Token
            - aruba_id  : ARUBA ID
            - MIN_VAL   : RSSI Min Value
            - MAX_VAL   : RSSI Max Value
    '''
    wap_df = list()
    for wap in waps:
        cmd = 'show+ap+monitor+ap-list+ap-name' + ap_prefix + '_' + wap
        list_waps = list_show_command(aosip, aruba_id, cmd)
        wap_df[wap] = pd.DataFrame(list_waps['Monitored AP Table'])
        wap_df[wap]['curr-rssi'] = pd.to_numeric(wap_df[wap]['curr-rssi'])
        wap_df[wap] = wap_df[wap][(wap_df[wap]['ap-type']!='valid')
                                  &(wap_df[wap]['essid']!='NTUST-UAM')
                                  &(wap_df[wap]['essid']!='NTUST-PEAP')
                                  &(wap_df[wap]['essid']!='sensor')
                                  &(wap_df[wap]['essid']!='eduroam')][['ap-type','essid','bssid','curr-rssi']]
        wap_df[wap] = wap_df[wap][(wap_df[wap]['curr-rssi']>=MIN_VAL)
                                  &(wap_df[wap]['curr-rssi']<=MAX_VAL)
                                 ]
    inter_aps = []

    # 1 3 5 7 9

    for i in range(5):
        try:
            ap_inter = wap_df[waps[i]]['bssid']
        except Exception:
            ap_inter = None
        inter_aps.append(ap_inter)
    
    ap13_inter = pd.concat([inter_aps[0],inter_aps[1]]).reset_index(drop=True).drop_duplicates()
    try:
        ap57_inter = pd.concat([inter_aps[2], inter_aps[3]]).reset_index(drop=True).drop_duplicates()
        all_inter_ap = pd.concat([ap13_inter, ap57_inter]).reset_index(drop=True).drop_duplicates()
        all_inter_ap = pd.concat([all_inter_ap, inter_aps[4]]).reset_index(drop=True).drop_duplicates()
    except Exception:
        all_inter_ap = inter_aps[0].reset_index(drop=True).drop_duplicates()
    
    all_ap = pd.DataFrame(all_inter_ap).reset_index(drop=True)
    all_ap['essid'], all_ap['ap-type'] = '', ''

    for i in range(len(waps)):
        try:
            all_ap[waps[i][-4:]] = None
        except Exception:
            pass
    
    all_ap['mon AP number'] = None

    # Pass all the information to be captured here
    for ap in range(len(all_ap)):
        no_ap = 0
        for ap in waps:
            try:
                all_ap['essid'][ap] = list(wap_df[ap][(wap_df[ap]['bssid'] == all_ap[''])])
                all_ap['bssid'][ap] = list(wap_df[ap][(wap_df[ap]['essid'] == all_ap[''])])
                all_ap['ap-type'][ap] = list(wap_df[ap][wap_df[ap]['essid'] == all_ap['']])
                
            except Exception:
                pass
    return wap_df
