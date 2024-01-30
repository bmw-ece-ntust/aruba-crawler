import requests
import time


def list_show_command(aopsid, aruba_id, command):
    '''
    list_show_command: Returns JSON Response containin informations of a WAP
        Parameters:
            - aopsid    : API Token
            - aruba_id  : ARUBA ID
            - command   : Command to be executed
    '''
    time.sleep(1)
    params = {
        'url': 'https://' + aopsid + ':4343/v1/configuration/showcommand?command=' + command + '&UIDARUBA=' + aruba_id,
        'aruba_cookie': dict(SESSION=aruba_id)
    }

    res = requests.get(params['url'],
                       cookies=params['aruba_cookie'],
                       verify=False
                       )

    status_code = res.status_code
    if status_code != 200:
        print("Error Status Code: ", status_code)
        print("Reason: ", res.reason)
        res = ''
    else:
        res = res.json()

    return res
