from dotenv import load_dotenv
import os
import argparse
from controller.APDataCollector import APDataCollector
from controller.Database import Database


load_dotenv()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--t',
        '--time',
        help='crawler active duration (minutes)',
        dest='time',
        default=5,
        type=int
    )

    args = parser.parse_args()

    ap_names = ['D1_1F_AP01', 'D1_1F_AP02', 
                'D1_1F_AP03', 'D1_1F_AP04',
                'D1_1F_AP05', 'D1_1F_AP06', 
                'D1_1F_AP07', 'D1_1F_AP08']  # Your AP names

    aruba_username = os.getenv('ARUBA_USERNAME')
    aruba_password = os.getenv('ARUBA_PASSWORD')
    aruba_ipaddress = os.getenv('ARUBA_IPADDRESS')

    database = Database()
    data_controller = APDataCollector(
        ap_names, aruba_username, aruba_password, aruba_ipaddress, database)

    data_controller.collect_and_store_data()
