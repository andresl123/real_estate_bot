# bot/route.py
from .common import bot
from web.search import search_with_location_and_budget
from .gemini import get_gemini_response
from web.main_scrap import Main
from web.db import Select
import time


# Dictionary to keep track of user state
user_data = {}

# Handle '/start' command
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    welcome_message = (
        "Welcome to the Bot! 🤖\n"
        "I can help you search for information based on your location and budget.\n"
        "Use the /search command to get started. To stop the automatic search use /stop"
    )
    bot.send_message(chat_id, welcome_message)

# Handle '/stop' command
# Decorator will handle the user input command, in this case "stop". This command will stop the while loop (in line 118). 
@bot.message_handler(commands=['stop'])
# The above decorator will call the bellow function
def handle_stop(message):
    chat_id = message.chat.id
    user_info = user_data.get(chat_id)
    bot.send_message(chat_id, "The search was stoped")

    # The while loop will stop because the step value will change to stop.
    user_info['step'] = 'stop'

# Handle '/search' command
# Decorator will handle the user input command, in this case "search"
@bot.message_handler(commands=['search'])
# The above decorator will call the bellow function
def handle_search(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Category menu:\n1. House\n2. Condo\n3. Land\nChoose between 1 and 3")
    
    # Initialize user state to capture menu first
    user_data[chat_id] = {'step': 'email'}

# Handle user responses
# the bot decorator is checking new messages that arrive in the telegram bot.
# lambda function will check if in the "message" has a "chat.id" in dictionary "user_data" 
@bot.message_handler(func=lambda message: message.chat.id in user_data)
# if the decotaror above is True it will call the bellow function an proceed with input messages from the user
def handle_user_input(message):
    chat_id = message.chat.id
    user_info = user_data.get(chat_id)

    if user_info['step'] == 'email':
        bot.send_message(chat_id, "Please provide your email.")
        user_info['email'] = message.text
        try:
            user_info['email'] = message.text
            # Check if the user input is within the valid range
            if (user_data[chat_id]['email'] != ''):
                bot.send_message(chat_id, f"The email will be sent to {user_data[chat_id]['email']}")
                user_info['step'] = 'menu'
            
            else:
                bot.send_message(chat_id, "Email was not provided, you will receive just telegran notifications")
                user_info['step'] = 'menu'

        except ValueError:
            # Prompt again if the input is not a valid Value
            bot.send_message(chat_id, "Invalid input. Please enter a number between 1 and 3 for category:\n1. House\n2. Condo\n3. Land")
            user_info['step'] = 'menu'
        

    elif user_info['step'] == 'menu':
        try:
            user_info['menu'] = int(message.text)
            # Check if the user input is within the valid range
            if (user_data[chat_id]['menu'] < 1 or user_data[chat_id]['menu'] > 3):
                bot.send_message(chat_id, "Invalid Number!!!\nPlease enter a number between 1 and 3:\n1. House\n2. Condo\n3. Land")
                user_info['step'] = 'menu'
            
            else:
                bot.send_message(chat_id, "Enter province name:")
                user_info['step'] = 'location'

        except ValueError:
            # Prompt again if the input is not a valid Value
            bot.send_message(chat_id, "Invalid input. Please enter a number between 1 and 3 for category:\n1. House\n2. Condo\n3. Land")
            user_info['step'] = 'menu'

    elif user_info['step'] == 'location':
        try:
            # Save location and ask for the budget
            user_info['location'] = message.text
            # Check if the user input is within the valid range
            if user_data[chat_id]['location'].replace(" ","").isalpha():
                bot.send_message(chat_id, "Enter your budget:")
                user_info['step'] = 'budget'
            
            else:
                bot.send_message(chat_id, "Invalid input!! Enter province name")
                user_info['step'] = 'location'

        except ValueError:
            # Prompt again if the input is not a valid Value
            bot.send_message(chat_id, "Invalid input!!! Enter province name")
            user_info['step'] = 'location'

    elif user_info['step'] == 'budget':
        try:
            # Save location and ask for the budget
            user_info['budget'] = float(message.text)
            # Check if the user input is within the valid range
            if isinstance(user_data[chat_id]['budget'], (int, float)):
                bot.send_message(chat_id, "Enter your desired city:")
                user_info['step'] = 'city'
            
            else:
                bot.send_message(chat_id, "Enter your budget:")
                user_info['step'] = 'budget'

        except ValueError:
            # Prompt again if the input is not a valid Value
            bot.send_message(chat_id, "Invalid input!!! Enter your budget:")
            user_info['step'] = 'budget'
    
    elif user_info['step'] == 'city':

        try:
            # Save city data
            user_info['city'] = message.text
            # Check if the user input is within the valid range
            if user_data[chat_id]['city'].replace(" ","").isalpha():
                print(user_data)
                
                # This while loop will stop when the key step has the value stop
                while (True):
                    if ( user_info['step'] == 'stop' ):
                        break
                    
                    else:
                        main = Main(user_data[chat_id]['menu'],user_data[chat_id]['location'],user_data[chat_id]['budget'],user_data[chat_id]['city'])
                        main.findList()
                        bot.send_message(chat_id, "Loading...")
                        select = Select
                        for item in select.select():
                            bot.send_message(chat_id, item)
                        time.sleep(1800)
                # when the while finishes will ask again to the user choose between 1 and 3 and change key step to menu, that will receive the user input to do another search
                bot.send_message(chat_id, "Select one of the option for a NEW SEARCH:\nCategory menu:\n1. House\n2. Condo\n3. Land\nChoose between 1 and 3")
                user_info['step'] = 'menu'

            else:
                bot.send_message(chat_id, "Invalid input!! Enter your desired city:")
                user_info['step'] = 'city'

        except ValueError:
            # Prompt again if the input is not a valid Value
            bot.send_message(chat_id, "Invalid input!!! Enter your desired city:")
            user_info['step'] = 'city'






