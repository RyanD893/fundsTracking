import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import threading
import time

links = []
raised = []
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")

class getRaised(threading.Thread):
    def __init__(self, i):
       threading.Thread.__init__(self)
       self.i = i
       return

    def run(self):
        global raised
        print(f"starting thread {self.i}")
        # chrome options 
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        # skip ones that don't exist
        if pd.isnull(links[self.i]):
            # raised.append(0)
            return
                # keep trying
        failed = 0
        while(failed == 0):
            failed = 1            
            # open page in chrome headless
            driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
            driver.get(links[self.i])
            # seach the html for the class containing raised amount
            content = driver.page_source
            soup = BeautifulSoup(content, "html.parser")
            found = soup.find_all("strong", {"class":"dd-thermo-raised"})
            # skip if not found to prevent errors
            if(len(found) == 0):
                print('Failed to find in html on link:' + str(self.i)) # debug
                # raised.append(0)
                failed = 0
                continue
            driver.quit() # close chrome
        # convert to number
        foundNum = found[0].text
        foundNum = re.findall(r'[0-9,]+', foundNum)
        # add to list of raised amount
        if len(foundNum) > 0:
            raised[self.i] = foundNum[0]
            print("Found: " + str(raised[self.i]) + " on link: " + str(self.i)) # debug
        else:
            # raised.append(0)
            print('Failed to find regex on link:' + str(self.i)) # debug

        return

if __name__ == "__main__":
    # open excel as panda data frame
    linksX = pd.read_excel('links.xlsx', header=None)

    # create list of links
    
    for column in linksX.columns:
        links.append(linksX[column].tolist())
    links = links[0]
    
    # create list of raised amount
    raised = [0] * len(links)


    # # ask user which rows they'd like done
    # usrIn = input("Press ENTER to search all, or provide a list of indices separated by spaces you'd like to search (this number is the row on the tracking sheet minus 2): ")
    # usrList = usrIn.split()
    # usrList = list(map(int, usrList))
    # print("You entered:")
    # print(usrList)
    # if(len(usrList) == 0):
    #     print("Searching all links . . .")
    #     usrList = range(len(links))
    
    

    # parse through links
    threads = []
    for i in range(len(raised)):
        # create thread
        threads.append(getRaised(i))
    for t in threads:
        t.start()
        time.sleep(.1)
    for t in threads:
        t.join()

        # # skip ones that don't exist
        # if pd.isnull(links[i]):
        #     raised.append(0)
        #     continue
        # # keep trying
        # failed = 0
        # while(failed == 0):
        #     failed = 1            
        #     # open page in chrome headless
        #     driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
        #     driver.get(links[i])
        #     # seach the html for the class containing raised amount
        #     content = driver.page_source
        #     soup = BeautifulSoup(content, "html.parser")
        #     found = soup.find_all("strong", {"class":"dd-thermo-raised"})
        #     # skip if not found to prevent errors
        #     if(len(found) == 0):
        #         print('Failed to find in html on link:' + str(i)) # debug
        #         # raised.append(0)
        #         failed = 0
        #         continue
        #     driver.quit() # close chrome
        # # convert to number
        # foundNum = found[0].text
        # foundNum = re.findall(r'[0-9,]+', foundNum)
        # # add to list of raised amount
        # if len(foundNum) > 0:
        #     raised.append(foundNum[0])
        #     print("Found: " + str(raised[i]) + " on link: " + str(i)) # debug
        # else:
        #     raised.append(0)
        #     print('Failed to find regex on link:' + str(i)) # debug
    print(raised) # debug

    # print to csv for copying
    df = pd.DataFrame(raised, columns=["raised"])
    df.to_csv('raised.csv', index=False)