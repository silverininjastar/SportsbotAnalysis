import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import socket
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
import sys, getopt

chrome_options = Options()
chrome_options.add_argument("--headless")

rollbit_sports_by_price_low = "https://rollbit.com/nft/lobby/sportsbots?count=10000&sort=price.asc"
rollbit_sports_by_price_high = "https://rollbit.com/nft/lobby/sportsbots?count=10000&sort=price.desc"

def open_rollbit_sports():
    print("Opening Chrome to Rollbit Sportsbots Marketplace")   
    if sort == "low":
        browser.get(rollbit_sports_by_price_low)
    elif sort == "high":
        browser.get(rollbit_sports_by_price_high)
    time.sleep(10)

    #Grab Data
    elem = browser.find_elements_by_class_name("css-midcvu")

    x=len(elem)
    for i in range(x):
        el = elem[i]
        soup = BeautifulSoup(el.text, 'html.parser')
        lst = [0]
        var = []
        j = 0
        for pos,char in enumerate(str(soup)):
             if(char == '\n'):
                lst.append(pos)
                var.append(str(soup)[lst[j]+1:lst[j+1]])                
                j = j + 1

        #Print all results to terminal window. Does not seem to function properly if not included.
        print(var)

        #Formulas for various column outputs
        d10_str="=IFERROR(LEFT(I" + str(i+2) + ",LEN(I" + str(i+2) + ")-1)*10^(SEARCH(RIGHT(I" + str(i+2) + "),\"kmbt\")*3),I" + str(i+2) + ")"
        d11_str="=LEFT(D" + str(i+2) + ",SEARCH(\"·\",D" + str(i+2) + ")-1)"
        d12_str="=MID(D" + str(i+2) + ",SEARCH(\"·\",D" + str(i+2) + ")+2,SEARCH(\"·\",D" + str(i+2) + ",SEARCH(\"·\",D" + str(i+2) + ")+1)-SEARCH(\"·\",D" + str(i+2) + ")-2)"
        d13_str="=RIGHT(D" + str(i+2) + ",4)"
        d14_str="=K" + str(i+2) + "+0.6*L" + str(i+2)
        d15_str="=J" + str(i+2) + "/N" + str(i+2)
        d16_str="=J" + str(i+2) + "/(0.6*L"  + str(i+2) + ")"


        if len(var[0]) < 5:
            d0.append(var[0])
            d1.append("Unrevealed")
            d2.append(var[1])
            d3.append("Unrevealed")
            d4.append(var[2])
            d5.append(var[3])
            d6.append(var[4])
            d8.append(var[5])
            d9.append(var[7])
            d10.append(d10_str)
            d11.append("N/A")
            d12.append("N/A")
            d13.append("N/A")
            d14.append("N/A")
            d15.append("N/A")
            d16.append("N/A")
        else:
            title=var[0].split()
            d0.append(title[0])
            sport=""
            for l in range(1,len(title)):
                sport+=(title[l] + " ")
            d1.append(sport)
            d2.append(var[1])
            d3.append(var[2])
            d4.append(var[3])
            d5.append(var[4])

            #Check if Rollbit shows suggested prices properly
            if var[3] != "Suggested prices not available":
                #d5.append(var[4])
                d6.append(var[5])
                d8.append(var[6])
                d9.append(var[8])
            else:
                d6.append(var[3])
                d8.append(var[3])
                d9.append(var[5])
        

            d10.append(d10_str)
            d11.append(d11_str)
            d12.append(d12_str)
            d13.append(d13_str)
            d14.append(d14_str)
            d15.append(d15_str)
            d16.append(d16_str)


#Use headless chromedriver for browser
browser = webdriver.Chrome(chrome_options=chrome_options)
#browser = webdriver.Chrome()
d0 = []
d1 = []
d2 = []
d3 = []
d4 = []
d5 = []
d6 = []
d8 = []
d9 = []
d10 = []
d11 = []
d12 = []
d13 = []
d14 = []
d15 = []
d16 = []

#Sorting can be changed from "low" to "high"
sort = "low"

#Check if using VPN based on current IP
h_name = socket.gethostname()
IP_address = socket.gethostbyname(h_name)

vpn = True

#Check if you are connected to a vpn
if vpn == True:
    if '192.168' in IP_address :
        print("VPN disconnected...")
    else:
        print("VPN active")
        open_rollbit_sports()
else:
    open_rollbit_sports()

#Create excel file and column headers
df = pd.DataFrame({'Number': d0, 'Name': d1, 'Collection': d2, 'Stats': d3, 'User': d4, 'Low': d5, 'Suggested': d6, 'High': d8, 'Current': d9, 'Current(adjusted)': d10, 'Share(current)': d11, 'Free Bet': d12, 'Parlay': d13, 'Monthly': d14, 'ROI(monthly)': d15, 'ROI(no shares)': d16})
df.to_csv('sports_rollbots.csv', index=False, encoding='utf-8')

browser.quit()
