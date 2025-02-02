import requests
from bot.email1 import send_email
from bs4 import BeautifulSoup
from .db import Insert
from .db import Select
import time
class Main:
    # dictionary to map the province and the kijiji code
    provinceDict = {"canada":"l0","ontario":"l9004","british-columbia":"l9007","alberta":"l9003","quebec":"l9001","saskatchewan":"l9009","nova-scotia":"l9002","new-brunswick":"l9005","manitoba":"l9006","prince-edward-island":"l9011","newfoundland":"l9008",}
    categoryDict = {1:"c35",2:"c643",3:"c641"}

    def __init__(self,menu,location,budget,city,email=""):
        self.email = email
        self.menu = menu
        self.location = location
        self.budget = budget
        self.city = city

    def findList(self):
        # the word will be low case and all the spaces will be replaced by '_'
        lowerLocationValue = self.location.lower().replace(" ","-")
        #from class Main will get the provinceDict dictionary value of the key lowerLocationValue. The default value if none was found will be l0, which is canada
        kijiji_code = Main.provinceDict.get(lowerLocationValue, "l0")
        kijiji_category = Main.categoryDict.get(self.menu, "c30353001")
        url = f"https://www.kijiji.ca/b-for-sale/{lowerLocationValue}/{kijiji_category}{kijiji_code}?sort=dateDesc&price=0__{self.budget}"

        print(f"-------------------->{url}")
        # Send a GET request to the website
        response = requests.get(url)

        # Check if request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')

            # Example of how to search for house listings (you'll need to inspect the site to get the right tags/classes)
            listings_price = soup.find_all("p", {"data-testid": "listing-price"})  # This might vary based on actual HTML
            listings_location = soup.find_all("p", {"data-testid": "listing-location"})
            listings_url = soup.find_all("a", {"data-testid":"listing-link"})
            listings_description = soup.find_all("a", {"class":"sc-78b01f6c-0 hnlgXi"})
            listings_image = soup.find_all("img",{"data-testid":"listing-card-image"})

            print(f'-------------->{listings_image}<------------------')

            # print(listings_description,listings_image,listings_location,listings_price,listings_url)

            insert = Insert(listings_price,listings_location,listings_description,listings_url,listings_image,self.location,self.budget,self.city)
            insert.insert()
            # if self.email:
            #     print(self.email)
            #     body = (
            #         f"Hello,\n\nWe found listings for your search:\nLocation: {self.location}\n"
            #         f"Budget: {self.budget}\nCity: {self.city}\n\n"
            #         f"Please visit the visit telegran Bot for more details.\n\nRegards,\nKijiji Bot"
            #     )
            #     send_email(self.email, body)

