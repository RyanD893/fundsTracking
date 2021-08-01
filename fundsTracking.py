import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import math

if __name__ == "__main__":
    # open excel as panda data frame
    linksX = pd.read_excel('links.xlsx', header=None)

    # create list of links
    links = []
    for column in linksX.columns:
        links.append(linksX[column].tolist())
    links = links[0]
    
    # create list of raised amount
    raised = []
    
    # chrome options 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    for i in len(links):
        if pd.isnull(links[i]):
            raised.append(0)
            continue
        driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
        driver.get(links[i])
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        found = soup.find_all("strong", {"class":"dd-thermo-raised"})
        if(len(found) == 0):
            raised.append(0)
            continue
        # foundNum = found.text.replace(',', '')
        foundNum = found[0].text
        foundNum = re.findall(r'[0-9][0-9,]+', foundNum)
        if foundNum:
            raised.append(foundNum[0])
        else:
            raised.append(0)
        print(raised[i])
        driver.quit()
    print(raised)

    df = pd.DataFrame(raised, columns=["raised"])
    df.to_csv('raised.csv', index=False)