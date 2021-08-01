import pandas as pd
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

    # ask user which rows they'd like done
    usrIn = input("Press ENTER to search all, or provide a list of indices separated by spaces you'd like to search (this number is the row on the tracking sheet minus 2): ")
    usrList = usrIn.split()
    usrList = list(map(int, usrList))
    print("You entered:")
    print(usrList)
    if(len(usrList) == 0):
        print("Searching all links . . .")
        usrList = range(len(links))

    # parse through links
    for i in usrList:
        # skip ones that fail
        if pd.isnull(links[i]):
            raised.append(0)
            continue
        # open page in chrome headless
        driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
        driver.get(links[i])
        # seach the html for the class containing raised amount
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        found = soup.find_all("strong", {"class":"dd-thermo-raised"})
        # skip if not found to prevent errors
        if(len(found) == 0):
            raised.append(0)
            continue
        # convert to number
        foundNum = found[0].text
        foundNum = re.findall(r'[0-9][0-9,]+', foundNum)
        # add to list of raised amount
        if foundNum:
            raised.append(foundNum[0])
        else:
            raised.append(0)
        print("Found: " + str(raised[i]) + " on link: " + str(i)) # debug
        driver.quit() # close chrome
    print(raised) # debug

    # print to csv for copying
    df = pd.DataFrame(raised, columns=["raised"])
    df.to_csv('raised.csv', index=False)