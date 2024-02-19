import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def get_aruba_dashboard_cookie(ip_addr, account, password):
    '''
    get_aruba_dashboard_cookie: Returns the cookie of an ARUBA Dashboard
        Parameters:
            - url       : URL of Aruba dashboard login website
            - account   : User account
            - password  : User password
    '''
    aruba_dashboard_cookie = ''
    params = {
        'dashboard_url': 'https://' + ip_addr + ':4343/screens/wms/wms.login',
        'payload': 'opcode=login&url=%2Flogin.html&needxml=0&uid=' + account +'&passwd='+ password,
        'headers': {'Content-Type': 'text/html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
    }

    get_aruba_login_data = requests.post(params['dashboard_url'],
                                  data=params['payload'].encode('utf-8'),
                                  headers=params['headers'],
                                  verify=False
                                  )

    status_code = get_aruba_login_data.status_code

    if status_code != 200:
        print("Error Status Code: ", status_code)
    else:
        aruba_dashboard_cookie = get_aruba_login_data.cookies['SESSION']
        #print("Successfully Retrieved Aruba Cookie")
    return aruba_dashboard_cookie
