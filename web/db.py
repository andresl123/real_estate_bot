import sqlite3
import time
# set the US curency in the select method
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
# import module for regular expression
import re

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
        con = sqlite3.connect(".\web\database\database.db")
        # zip function will make all the list the same size
        # getting the values of price, url, image, location, description and images 
        cityCap = self.city.split()[0].capitalize()
        time_epoch = int(time.time())
        for i, l, j, k, z in zip(self.listings_price,self.listings_location,self.listings_description,self.listings_url,self.listings_image):
            # print(f"--------------------->{l.text}<------------------------")
            # print(f"#####################>{cityCap}<#######################")
            # If the value of i.text contains 'Please Contact' or l.text does not contain the value of the variable 'cityCap' will jump to the next iteration
            if (i.text == 'Please Contact' or cityCap not in l.text):
                continue
            con.execute("""INSERT INTO SCRAP(PRICE,LOCATION,DESCRIPTION,URL,IMAGES,DATE) VALUES (?, ?, ?, ?, ?, ?);""", (float(i.text.replace('$','').replace(',','')),l.text, j.text, k.get('href'), z.get('src'),time_epoch))
        con.commit()
        con.close()

class Select():
    def select():
        con = sqlite3.connect(".\web\database\database.db")

        # store all the results of the listining inside of the below list to be called after in the return statement
        results = []
        list_old = {}
        list_new = {}

        epoch_timestamp = int(time.time())
        print(f'************> {epoch_timestamp} <************')

        get_from_table_old = con.execute("""
            SELECT PRICE, LOCATION, DESCRIPTION, URL, IMAGES, DATE
            FROM SCRAP
            WHERE DATE BETWEEN (SELECT MAX(DATE) - 3599 FROM SCRAP) AND (SELECT MAX(DATE) - 1801 FROM SCRAP)
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

        count_dict_new = 0
        while ( count_dict_new < len(list_new) ):
            current_id_new = re.search(r'\d+$', list_new[count_dict_new]["URL"]).group()
            count_dict_old = 0
            flag_equal = False
            while ( count_dict_old < len(list_old) ):
                current_id_old = re.search(r'\d+$', list_old[count_dict_old]["URL"]).group()
                print(f'---------NEW ID {count_dict_new}--------->{current_id_new}')
                print(f'---------OLD ID {count_dict_old}--------->{current_id_old}')
                
                
                if ( current_id_new == current_id_old ):
                    flag_equal = True
                    # print(f'---------NEW ID--------->{current_id_new}')
                    # print(f'---------OLD ID--------->{current_id_old}')
                    # print(list_old[count_dict_old])
                elif ( flag_equal == False and count_dict_old == len(list_old) - 1 ):
                    print(f'IDs equas NEW: {current_id_new}, OLD: {current_id_old}')
                    # using "yield" allow me to keeping return values to the caller without finishes the function insteed of using "return" and return only the first value and terminate the function.
                    yield f"Price: {locale.currency(float(list_new[count_dict_new]['PRICE']), grouping=True)}\nLocation: {list_new[count_dict_new]['LOCATION']}\nDescription: {list_new[count_dict_new]['DESCRIPTION']}\nURL: {list_new[count_dict_new]['URL']}\nIMAGES: {list_new[count_dict_new]['IMAGES']}\nDATE: {list_new[count_dict_new]['DATE']}\n"

                count_dict_old+=1
            count_dict_new+=1
            # current_id_old = re.search(r'\d+$', list_old[count_old]["URL"]).group()
            # print(f'----------> NEW ID <-----------{current_id_new}')
            # print(f'----------> OLD ID <-----------{current_id_old}')
            # if ( current_id_new == current_id_old):
            #     print(list_old[count_old])
            # count_old+=1


            # count = 0
            # while ( count < len(list_old) ):
            #     print(f'------------> OLD <------------- {list_old[count]}')
            #     count+=1
                
            # populating list of old listings
            # if len(list_old) > 5:
            #     count = 0
            #     while ( count < len(list_new) ):
                    # if count == 3:
                    #     current_id_new = re.search(r'\d+$', list_new[3]).group()
                    #     count1 = 0
                    #     while ( count1 < len(list_old) ):
                    #         current_id_old = re.search(r'\d+$', list_old[3]).group()
                    #         if ( current_id_new == current_id_old ):
                    #             print(f'id new {current_id_new} is EQUAL to id old {current_id_old}')
                    #         else:
                    #             print(f'id new {current_id_new} is DIFFERENT to id old {current_id_old}')
                    #             count2 = 0
                    #             while ( count2 < len(list_new) ):
                    #                 print(f'------------> NEW <------------- {list_new[count]}')
                    #                 count2+=1
                    #         count1+=1
                    # count+=1
                    # if ( count == 3 ):
                    #     print(list_new)
                    # print(list_new)
                    # count+=1                

        # reset the list to receive a new list in the new iteration
        list_old.clear()
        list_new.clear()

        # for row in get_from_table_old:
        #     current_id_old = re.search(r'\d+$', row[3]).group()
        #     print(f'............> ID OLD <............ {current_id_old}')
        #     print("------> OLD <------ PRICE = ", row[0])
        #     print("------> OLD <------ LOCATION = ", row[1])
        #     print("------> OLD <------ DESCRIPTION = ",row[2])
        #     print("------> OLD <------ URL = ",row[3])
        #     print("------> OLD <------ IMAGES = ",row[4])
        #     print("------> OLD <------ DATE = ",row[5])
        #     print("")

        # for row1 in get_from_table_new:
        #     current_id_new = re.search(r'\d+$', row1[3]).group()
        #     for row2 in get_from_table_old:
        #         current_id_old = re.search(r'\d+$', row2[3]).group()
        #         if ( current_id_new == current_id_old ):
        #             print(f'{current_id_new} is EQUAL to {current_id_old}')
        #             # print("------> SAME <------ PRICE = ", row2[0])
        #             # print("------> SAME <------ LOCATION = ", row2[1])
        #             # print("------> SAME <------ DESCRIPTION = ",row2[2])
        #             # print("------> SAME <------ URL = ",row2[3])
        #             # print("------> SAME <------ IMAGES = ",row2[4])
        #             # print("------> SAME <------ DATE = ",row2[5])
        #             # print("")
        #         else:
        #             print(f'{current_id_new} is DIFERENTE to {current_id_old}')
        #             # using "yield" allow me to keeping return values to the caller without finishes the function insteed of using "return" and return only the first value and terminate the function.
        #             yield f"Price: {locale.currency(float(row1[0]), grouping=True)}\nLocation: {row1[1]}\nDescription: {row1[2]}\nURL: {row1[3]}\nIMAGES: {row1[4]}\nDATE: {row1[5]}\n"

        # get_from_table = con.execute("SELECT PRICE,LOCATION,DESCRIPTION,URL,IMAGES,DATE from SCRAP ORDER BY DATE desc LIMIT 5")

        # for row in get_from_table:
        #     print("PRICE = ", row[0])
        #     print("LOCATION = ", row[1])
        #     print("DESCRIPTION = ",row[2])
        #     print("URL = ",row[3])
        #     print("IMAGES = ",row[4])
        #     print("DATE = ",row[5])
        #     print("")

        con.close
