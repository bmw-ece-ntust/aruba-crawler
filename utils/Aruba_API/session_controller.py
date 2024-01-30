import datetime
import requests
import json


def get_aruba_id(aopsid, id, password):
    '''
    get_aruba_id: Returns the ARUBA ID of an ARUBA Controller
        Parameters:
            - aopsid    : API Token
            - id        : Username Credential
            - password  : User password
    '''
    aruba_id = ''
    params = {
        'url': 'https://' + aopsid + ':4343/v1/api/login',
        'payload': 'username=' + id + '&password=' + password,
        'headers': {
            'Content-type': 'application/json'
        }
    }

    get_aruba_uid = requests.post(params['url'],
                                  data=params['payload'],
                                  headers=params['headers'],
                                  verify=False
                                  )

    status_code = get_aruba_uid.status_code

    if status_code != 200:
        print("Error Status Code: ", status_code)
    else:
        aruba_id = get_aruba_uid.json()['_global_result']['UIDARUBA']
        print(aruba_id)
        print("Successfully Retrieved ARUBA ID")
    return aruba_id
