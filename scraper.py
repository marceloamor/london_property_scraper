# Rightmove scraper

# Requirements
# pip install requests
# pip install bs4
# pip install pandas

#import libraries
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import random

# create lists to store our data
all_apartment_links = [] # stores apartment links
all_description = [] # stores number of bedrooms in the apartment
all_address = [] # stores address of apartment
all_price = [] # stores the listing price of apartment


# Creating index and setting search location
index = 0
TowerHamletsCode = "5E61417"   #important!!!! replace with target area in london, visible in Rightmove's URL

for pages in range(41):

    # define user headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }

  # the website changes if you are on page 1 as compared to other pages
    if index == 0:
        rightmove = f"https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%{TowerHamletsCode}&sortType=6&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords="
        
    elif index != 0:
        rightmove = f"https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%{TowerHamletsCode}&sortType=6&index={index}&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords="

    # request our webpage
res = requests.get(rightmove, headers=headers)

# check status
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser") #save HTML soup for parsing

### Let the scraping begin!!!


# This gets the list of flats
apartments = soup.find_all("div", class_="l-searchResult is-list")

# This gets the number of listings
number_of_listings = soup.find(
    "span", {"class": "searchHeader-resultCount"}
)
number_of_listings = number_of_listings.get_text()
number_of_listings = int(number_of_listings.replace(",", ""))

for i in range(len(apartments)):

    # tracks which apartment we are on in the page
    apartment_no = apartments[i]

    # append link
    apartment_info = apartment_no.find("a", class_="propertyCard-link")
    link = "https://www.rightmove.co.uk" + apartment_info.attrs["href"]
    all_apartment_links.append(link)

    # append address
    address = (
        apartment_info.find("address", class_="propertyCard-address")
        .get_text()
        .strip()
    )
    all_address.append(address)

    # append description
    description = (
        apartment_info.find("h2", class_="propertyCard-title")
        .get_text()
        .strip()
    )
    all_description.append(description)

    # append price
    price = (
        apartment_no.find("span", class_="propertyCard-priceValue")
        .get_text()
        .strip()
    )
    price = re.sub("[^0-9]", "", price)
    all_price.append(price)
    
    # Code to count how many listings we have scraped already.
    index = index + 24

    if index >= number_of_listings:
        break


## create usable data
# convert data to dataframe
data = {
    "Links": all_apartment_links,
    "Address": all_address,
    "Description": all_description,
    "Price": all_price,
    }
df = pd.DataFrame.from_dict(data)

df.to_csv(r"sales_data.csv", encoding="utf-8", header="true", index = False) #save scraped data in a csv

print(df)




