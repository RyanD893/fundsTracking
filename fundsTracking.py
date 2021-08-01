import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re

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


    for i in range(len(links)):
        if(links[i] == ""):
            continue
        driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
        driver.get(links[i])
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        found = soup.find("strong", {"class":"dd-thermo-raised"})
        foundNum = re.findall(r'\d+', found.text)
        if foundNum:
            raised.append(foundNum[0])
        else:
            raised.append(0)
        print(raised[i])
        driver.quit()
    print(raised)
    