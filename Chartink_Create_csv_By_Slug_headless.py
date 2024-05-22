# Function to read the screenmapper from filter.txt
def readFilterFile():
    try:
        filepath = 'Filters//filter.txt'
        screenmapper = []
        with open(filepath, 'r') as file:
            for line in file:
                screenmapper.append(line.strip())
        return screenmapper
    except Exception as e:
        print(f"An error occurred: {e}")


def GetDataFromChartink(payload):

    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import logging
    # from win10toast import ToastNotifier
    #toast = ToastNotifier()
    #toast.show_toast("Hello, World!")
    
    Charting_Link = "https://chartink.com/screener/"
    Charting_url = 'https://chartink.com/screener/process'

    payload = {'scan_clause': payload}
    
    try:

        with requests.Session() as s:
            r = s.get(Charting_Link)
            soup = BeautifulSoup(r.text, "html.parser")
            csrf = soup.select_one("[name='csrf-token']")['content']
            s.headers['x-csrf-token'] = csrf
            #headers={}
            s.headers['Content-Type']='application/x-www-form-urlencoded'
            r = s.post(Charting_url, data=payload)

            df = pd.DataFrame()
            df = pd.concat([df, pd.DataFrame.from_records(r.json()['data'])])
            # for item in r.json()['data']:
            #     df = pd.concat(df, item, ignore_index=True)
            
        return df
    except requests.exceptions.HTTPError as e:
        #print(e)
        logging.info(e)
        #print("some error in the connection")
        logging.info("Error in network connection")
    except requests.exceptions.RequestException as e:
        #print(e)
        logging.info(e)

# Python code to remove whitespace
from functools import reduce

#Function to remove white space
def removespaces(txt):
	#return reduce(lambda x, y: (x+y) if (y != " ") else x, string, "");
    import re

    res = re.sub('  ([\(]) ?',r'\1', txt)  #re.sub(' +', ' ', str)
    res = re.sub(' ([\(]) ?',r'\1', res)
    s = res
    return s


	
# Python3 code to demonstrate working of
# remove additional space from string
# Using re.sub()


def CreateCsvFile(marketdirection):
    from pathlib import Path
    from datetime import datetime
    
    today = datetime.now().strftime("%d_%m_%Y")
    filename = today+"/"+marketdirection+".csv"
    output_file = Path(filename)
       
    output_file.parent.mkdir(exist_ok=True, parents=True)
    return output_file
    


def ChartInkScraper(marketdirection):

    import pandas as pd
    from datetime import datetime
    from selenium import webdriver
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver import DesiredCapabilities as dc
    from selenium.webdriver.chrome.service import Service
    import pyperclip
    import logging


    chrome_driver_path = "/usr/bin/chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=500,100")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    service = Service(executable_path=chrome_driver_path)
    browser = webdriver.Chrome(service=service, options=options)
    # browser = webdriver.Chrome(chrome_driver_path)
    dc.CHROME["unexpectedAlertBehaviour"] = "accept"

    listOfDataFramesOuter = pd.DataFrame()
    
    try:
        payloaddata = marketdirection
        print("--------------------------------------------------- payloaddata ---------------------------------------------------")
        print(payloaddata)
        print("-------------------------------------------------------------------------------------------------------------------")
        try:
            browser.switch_to.alert.dismiss()
        except Exception:
            #print('No alert present')
            logging.info("No alert present")
        
        data = GetDataFromChartink(payloaddata)
        if data is not None:
    
            if data.empty == False:
                data = data.sort_values(by='per_chg', ascending=False)
            print(data)
            # data['ScreenerName'] = marketdirection
            data['TimeOfDay'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            #print(data.info())
            if data.shape[1] != 2:
                data['nsecode']=data['nsecode'].astype('string')
        
            #toast.show_toast(data)
            if listOfDataFramesOuter.empty == True:
                listOfDataFramesOuter = data
            else:
                if data.empty == False:
                    listOfDataFramesOuter = pd.concat([listOfDataFramesOuter,data])

            browser.back()

        formattedfilepath = CreateCsvFile('marketdirection')
        
        # Check if the CSV file already exists
        if formattedfilepath.is_file():
            
            empty_df = pd.DataFrame([{}] * 3)
            
            # Concatenate the empty DataFrames with the main DataFrame
            listOfDataFramesOuter = pd.concat([empty_df, listOfDataFramesOuter], ignore_index=True)
        
            # Append mode (mode='a'), don't include header
            listOfDataFramesOuter.to_csv(formattedfilepath, mode='a', header=False, index=False)
        else:
            # Write mode (mode='w'), include header
            listOfDataFramesOuter.to_csv(formattedfilepath, mode='w', header=True, index=False)
        print("-------------------------------------------------------------------------------------------------------------------")
        print("file updated")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:     
        print("━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸")
        browser.quit()



if __name__ == '__main__':
    try:
        screenmapper = readFilterFile()
        print(screenmapper)
        for marketdirection in screenmapper:
            ChartInkScraper(marketdirection)

    except Exception as e:
        pass
