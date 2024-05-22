
screenmapper={

    '1': '1-year-brackout',
    '2': '5-year-brackout',
    '3': 'weekly-brackout-intraday-2',
    '4': '5-year-brackout-new',
    '5': 'stocks-near-52-week-and-down-25-from-52-week-high'
}

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


def CreateTxtFile(marketdirection):
    from pathlib import Path
    from datetime import datetime
    
    filename = "Filters/filter.txt"
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
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(executable_path=chrome_driver_path)
    browser = webdriver.Chrome(service=service, options=options)
    # browser = webdriver.Chrome(chrome_driver_path)
    dc.CHROME["unexpectedAlertBehaviour"] = "accept"

  
    browser.get("https://chartink.com/screener/"+marketdirection)

    listOfDataFramesOuter = pd.DataFrame()
    
    try:

        # element = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.LINK_TEXT, "https://chartink.com/screener/"+marketdirection)))
        element = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, "//div[@class='atlas-heading']"))) 


        # Get all the elements available with tag name 'i'
        elements = element.find_elements(By.TAG_NAME, 'i')
        
        for e in elements:
            #print(e.accessible_name)
            e.click()
    
        #print(pyperclip.paste())
        payloaddata = pyperclip.paste()

        #payloaddata='( {33489} ( latest ema( close,20 ) > 20 and latest sma( volume,20 ) >= 100000 and latest ichimoku conversion line( 3,7,14 ) >= latest ichimoku base line( 3,7,14 ) and latest ichimoku span a( 3,7,14 ) >= latest ichimoku span b( 3,7,14 ) and latest close >= latest ichimoku cloud bottom( 3,7,14 ) and( {33489} ( latest close >= latest parabolic sar( 0.02,0.02,0.2 ) and latest rsi( 10 ) >= 20 and latest stochrsi( 10 ) >= 20 and latest cci( 10 ) >= 0 and latest mfi( 10 ) >= 20 and latest williams %r( 10 ) >= -80 and latest close >= latest ema( close,14 ) and latest adx di positive( 10 ) >= latest adx di negative( 10 ) and latest aroon up( 10 ) >= latest aroon down( 10 ) and latest slow stochastic %k( 5,3 ) >= latest slow stochastic %d( 5,3 ) and latest fast stochastic %k( 5,3 ) >= latest fast stochastic %d( 5,3 ) and latest close >= latest sma( close,10 ) ) ) and ( {33489} ( latest macd line( 14,5,3 ) >= latest macd signal( 14,5,3 ) and latest macd histogram( 14,5,3 ) >= 0 ) ) and ( {33489} ( latest rsi( 14 ) > 50 and latest stochrsi( 14 ) > 50 and latest rsi( 10 ) < 80 and latest close >= latest upper bollinger band( 20,2 ) and latest close >= latest ichimoku cloud bottom( 9,26,52 ) and latest close > latest open and latest volume > 100000 and latest ema( close,5 ) > latest ema( close,20 ) and latest ema( close,20 ) > latest ema( close,50 ) and latest close > latest ema( close,50 ) ) ) ) ) '
        payloaddata = removespaces(payloaddata)
        print("--------------------------------------------------- payloaddata ---------------------------------------------------")
        print(payloaddata)
        print("-------------------------------------------------------------------------------------------------------------------")

        output_file = CreateTxtFile(marketdirection)
        
        with open(output_file, 'a') as file:
            file.write(payloaddata + "\n")
              
        
        print(f"Data successfully written to {output_file}")
    finally:
        print("━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸━╸")
        # browser.quit()



if __name__ == '__main__':
    try:
        for index in range(0,len(screenmapper)):
            ChartInkScraper(screenmapper.get(str(index+1)))

    except Exception as e:
        pass
