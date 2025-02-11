import sqlite3
import time
# set the US curency in the select method
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
# import module for regular expression
import re
import os

# Path to the SQLite database
db_path = "/app/database.db"

# Ensure the directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Connect to SQLite database (creates file if it doesn't exist)
con = sqlite3.connect(db_path)

# Create a sample table (optional)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS SCRAP (PRICE NUMBER(50, 2), LOCATION VARCHAR2(1000), DESCRIPTION VARCHAR2(1000), URL VARCHAR2(1000), IMAGES VARCHAR2(1000), DATE DATE)")
con.commit()

print("Database initialized successfully.")

class Insert:
    def __init__(self,listings_price,listings_location,listings_description,listings_url,listings_image,location,budget,city):
        self.listings_price = listings_price
        self.listings_location = listings_location
        self.listings_description = listings_description
        self.listings_url = listings_url
        self.listings_image = listings_image
        self.location = location
        self.budget = budget
        self.city = city
    def insert(self):
        con = sqlite3.connect(db_path)
        # zip function will make all the list the same size
        # getting the values of price, url, image, location, description and images 
        cityCap = self.city.split()[0].capitalize()
        time_epoch = int(time.time())
        # print(f"#--------------------->{self.listings_location.text}<------------------------#")
        # print(f"#####################>{cityCap}<#######################")
        for i, l, j, k, z in zip(self.listings_price,self.listings_location,self.listings_description,self.listings_url,self.listings_image):
            print("TESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTEST")
            print(f"--------------------->{l.text}<------------------------")
            print(f"#####################>{cityCap}<#######################")
            # If the value of i.text contains 'Please Contact' or l.text does not contain the value of the variable 'cityCap' will jump to the next iteration
            if (i.text == 'Please Contact' or cityCap not in l.text):
                continue
            con.execute("""INSERT INTO SCRAP(PRICE,LOCATION,DESCRIPTION,URL,IMAGES,DATE) VALUES (?, ?, ?, ?, ?, ?);""", (float(i.text.replace('$','').replace(',','')),l.text, j.text, k.get('href'), z.get('src'),time_epoch))
        con.commit()
        con.close()

class Select():
    def select():
        con = sqlite3.connect(db_path)

        # store all the results of the listining inside of the below list to be called after in the return statement
        results = []
        list_old = {}
        list_new = {}

        epoch_timestamp = int(time.time())
        print(f'************> {epoch_timestamp} <************')

        get_from_table_old = con.execute("""
            SELECT PRICE, LOCATION, DESCRIPTION, URL, IMAGES, DATE
            FROM SCRAP
            WHERE DATE BETWEEN (SELECT MAX(DATE) - 3599 FROM SCRAP) AND (SELECT MAX(DATE) - 1800 FROM SCRAP)
            ORDER BY DATE DESC
            LIMIT 10
        """)

        get_from_table_new = con.execute("""
            SELECT PRICE, LOCATION, DESCRIPTION, URL, IMAGES, DATE
            FROM SCRAP
            WHERE DATE = ?
            ORDER BY DATE DESC
            LIMIT 10
        """,(epoch_timestamp,))

        # adding the list of properties in a list
        count_new = 0
        for item in get_from_table_new:            
            PRICE = item[0]
            LOCATION = item[1]
            DESCRIPTION = item[2]
            URL = item[3]
            IMAGES = item[4]
            DATE = item[5]
            
            list_new.update({count_new:{"PRICE": item[0], "LOCATION" : item[1], "DESCRIPTION" : item[2], "URL" : item[3], "IMAGES" : item[4], "DATE" : item[5]}})
            # print(list_new[count_new])
            current_id_new = re.search(r'\d+$', list_new[count_new]["URL"]).group()
            count_new+=1

        # adding the list of properties in a list
        count_old = 0    
        for item1 in get_from_table_old:      
            PRICE = item1[0]
            LOCATION = item1[1]
            DESCRIPTION = item1[2]
            URL = item1[3]
            IMAGES = item1[4]
            DATE = item1[5]
            
            list_old.update({count_old:{"PRICE": item1[0], "LOCATION" : item1[1], "DESCRIPTION" : item1[2], "URL" : item1[3], "IMAGES" : item1[4], "DATE" : item1[5]}})
            count_old+=1
        print(list_old)

        # in this while, will check each ID of list_new with all the IDs from list_old. 
        # if comparing each list_new ID with all the IDs from list_old and the flag still false and reach the end of list_old dict will return(yield) the list_new
        count_dict_new = 0
        while ( count_dict_new < len(list_new) ):
            current_id_new = re.search(r'\d+$', list_new[count_dict_new]["URL"]).group()
            count_dict_old = 0
            flag_equal = False

            if not list_old:
                yield f"Price: {locale.currency(float(list_new[count_dict_new]['PRICE']), grouping=True)}\nLocation: {list_new[count_dict_new]['LOCATION']}\nDescription: {list_new[count_dict_new]['DESCRIPTION']}\nURL: {list_new[count_dict_new]['URL']}\nIMAGES: {list_new[count_dict_new]['IMAGES']}\nDATE: {list_new[count_dict_new]['DATE']}\n"
                # if not list_new:
                #     yield f"No listings found."

            while ( count_dict_old < len(list_old) ):
                current_id_old = re.search(r'\d+$', list_old[count_dict_old]["URL"]).group()
                print(f'---------NEW ID {count_dict_new} --------->{current_id_new}')
                print(f'---------OLD ID {count_dict_old} --------->{current_id_old}')
                
                if ( current_id_new == current_id_old ):
                    flag_equal = True
                    print(f'---------NEW ID {count_dict_new} ---------> {flag_equal} {current_id_new}')
                    print(f'---------OLD ID {count_dict_old} ---------> {flag_equal} {current_id_old}')
                    # print(list_old[count_dict_old])

                    if ( flag_equal == True and count_dict_new == len(list_new) - 1 ):
                        yield f"Currently, there are no new listings."

                elif ( flag_equal == False and count_dict_old == len(list_old) - 1 ):
                    print(f'IDs are differents - print to user - NEW: {current_id_new}, OLD: {current_id_old}')
                    # using "yield" allow me to keeping return values to the caller without finishes the function insteed of using "return" and return only the first value and terminate the function.
                    yield f"Price: {locale.currency(float(list_new[count_dict_new]['PRICE']), grouping=True)}\nLocation: {list_new[count_dict_new]['LOCATION']}\nDescription: {list_new[count_dict_new]['DESCRIPTION']}\nURL: {list_new[count_dict_new]['URL']}\nIMAGES: {list_new[count_dict_new]['IMAGES']}\nDATE: {list_new[count_dict_new]['DATE']}\n"

                count_dict_old+=1
            count_dict_new+=1
        list_old.clear()
        list_new.clear()

        con.close
