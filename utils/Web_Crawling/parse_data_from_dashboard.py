from bs4 import BeautifulSoup
from bs4.builder import XMLParsedAsHTMLWarning
import warnings
import time
import pandas as pd

warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

def parse_aruba_data_to_dataframe(aruba_raw_data):
    '''
    parse_aruba_data_to_dataframe: Parse the AP or Client data to DataFrame format 
        Parameters:
            - aruba_raw_data     : AP or Client raw data from aruba dashboard
    '''
    # Parse AP data
    parsed_raw_data = BeautifulSoup(aruba_raw_data, 'html.parser')
    parameter_name = parsed_raw_data.find_all('header')
    parameter_value = parsed_raw_data.find_all('row')
    
    """
    DataFrame format
    """
    
    aruba_data = pd.DataFrame() 
    index = 0
 
    # Parameter value
    for values in parameter_value:
        
        parameter_value_total = []
        parameter_value = values.find_all('value')
        
        time_stamp = int(time.time())
        parameter_value_total.append(time_stamp)

        for i in range(len(parameter_value)):
            parameter_value_total.append(parameter_value[i].text)

        index += 1
        aruba_data[index] = parameter_value_total
    
    # Parameter name
    for names in parameter_name:
        
        parameter_name_total = []
        parameter_name_total.append('time_stamp')
        parameter_name = names.find_all('column_name')
        
        for i in range(len(parameter_name)):
            parameter_name_total.append(parameter_name[i].text)

    aruba_data.index = parameter_name_total
    aruba_data = aruba_data.T
    aruba_data.reset_index(drop=True, inplace=True) 
    
    return aruba_data