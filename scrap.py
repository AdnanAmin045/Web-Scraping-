from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from selenium.webdriver.chrome.service import Service

service = Service(executable_path='D:\\University Material\\3rd Semester\\DataStructuresAndAlgorithms\\Mid Project DSA\\chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)


URLList= []
nameList = []
statusList = []
priceList = []
availableList = []
shippingPriceList = []
ratingList= []
returnPolicyList = []
shippingCityList = []
informationList = []
with open("D:\\University Material\\3rd Semester\\DataStructuresAndAlgorithms\\Mid Project DSA\\WatchesURL2.txt","r") as f:
    URL_Links = f.read().split("\n")

count = 155
page = 1
url = str(URL_Links[count]) + str(page)
with open("LastURL.txt","w") as f:
        data_to_write = f"{URL_Links[count]} {page}\n"
        f.write(data_to_write)
while url:
    try:
        if page == 45:
            page = 1
            count-=1
            url = str(URL_Links[count]) + str(page)
            with open("LastURL.txt","w") as f:
                data_to_write = f"{URL_Links[count]} {page}\n"
                # Write the concatenated string to the file
                f.write(data_to_write)
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for a in soup.findAll('div', attrs={'class', 's-item__wrapper clearfix'}):
            name = (a.find('div', attrs={'class': 's-item__title'})).find('span')
            status = a.find('span', attrs={'class': 'SECONDARY_INFO'})
            price = a.find('span', attrs={'class': 's-item__price'})
            available = a.find('span', attrs={'class': 's-item__purchase-options s-item__purchaseOptions'})
            shippingPrice = a.find('span', attrs={'class': 's-item__shipping s-item__logisticsCost'})
            rate = a.find('span', attrs={'class': 's-item__reviews-count'})
            returnPolicy = a.find('span', attrs={'class': 's-item__free-returns s-item__freeReturnsNoFee'})
            shippingCity = a.find('span', attrs={'class': 's-item__location s-item__itemLocation'})
            information = a.find('span', attrs={'class': 'BOLD'})
            if name:
                nameList.append(name.text)
            else:
                nameList.append('None')
            if status:
                statusList.append(status.text)
            else:
                statusList.append('None')
            if price:
                priceList.append(price.text)
            else:
                priceList.append('None')
            if available:
                availableList.append(available.text)
            else:
                availableList.append('None')
            if shippingPrice:
                shippingPriceList.append(shippingPrice.text)
            else:
                shippingPriceList.append('None')
            if rate:
                ratingList.append(rate.text)
            else:
                ratingList.append('0')
            if returnPolicy:
                returnPolicyList.append(returnPolicy.text)
            else:
                returnPolicyList.append('No Return')
            if shippingCity:
                shippingCityList.append(shippingCity.text)
            else:
                shippingCityList.append('None')
            if information:
                informationList.append(information.text)
            else:
                informationList.append('No Information')


        page +=1
        url = str(URL_Links[count]) + str(page)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        break


df = pd.DataFrame({'Product Name': nameList, 'Product Condition': statusList, 'Product Status': availableList, 'Price': priceList,'Shipping Price':shippingPriceList,'Review Points':ratingList,'Return Policy':returnPolicyList,'Shipping City':shippingCityList,'Other Information':informationList})
df.to_csv('ExtraData.csv', index=False, encoding='utf-8')
