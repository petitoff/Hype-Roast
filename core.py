import json
import urllib
import urllib.request
import requests
import time
from time import sleep
from threading import Thread

from telegram import *
from telegram.ext import *

# here create global variables for coinbase module
lst_of_available_currencies = []
lst_of_currencies_and_price = []
lst_name_of_cryptocurrencies_to_live_price = ["BTC"]

dct_of_alert_name_percentage = {}
dct_of_currencies_and_price_current = {}
dct_of_currencies_and_price_main = {}

sell_price = 1.1
buy_price = 1.1
time_update = 600
time_update_stop = False
name_of_cryptocurrencies_to_live_price = ""

count_coinbase_main_1 = 0

"""
This is place for coinbase part. This is where the availability of cryptocurrencies and their current prices 
are checked.
"""


def get_all_available_crypto():
    global lst_of_available_currencies
    lst_of_available_currencies.clear()

    url = 'https://api.pro.coinbase.com/currencies'
    response = requests.get(url).json()

    for i in range(len(response)):
        if response[i]['details']['type'] == 'crypto':
            lst_of_available_currencies.append(response[i]['id'])


def get_price_of_currency_from_coinbase(name):
    # name is id of crypto
    # you will get name and price of crypto in string type
    url = f"https://api.coinbase.com/v2/prices/{name}-USD/spot"
    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        data = response.read()
        values = json.loads(data)
        a = values["data"]["base"]
        a += " " + values["data"]["amount"]
        if a is not None:
            return a
    except urllib.error.HTTPError:
        pass


def get_currently_price_of_currency(name):
    global dct_of_currencies_and_price_main

    price = dct_of_currencies_and_price_main[name][-1]
    return price


def coinbase_get_price():
    global lst_of_available_currencies, dct_of_currencies_and_price_main, count_coinbase_main_1

    get_all_available_crypto()  # runs a function that gets the names of all available currencies

    while True:
        lst_local_of_currencies_and_price = []
        # creates a list with name and price. This is a temporary list that is needed to create a dictionary

        for i in lst_of_available_currencies:
            try:
                name_price = get_price_of_currency_from_coinbase(i)
                lst_local_of_currencies_and_price.extend(name_price.split(" "))
            except AttributeError:
                pass

        dct_name_price = convert(lst_local_of_currencies_and_price)

        if dct_of_currencies_and_price_main:
            for key, value in dct_name_price.items():
                dct_of_currencies_and_price_main[key].append(round(float(value), 4))
        else:
            for key, value in dct_name_price.items():
                d_let1 = {}
                lst_let1 = [round(float(value), 4)]

                d_let1[key] = lst_let1
                dct_of_currencies_and_price_main.update(d_let1)

        # print(dct_of_currencies_and_price_main)
        count_coinbase_main_1 = 1
        sleep(30)


"""
Here there is a function that checks if the designated "breakpoint" values have not been reached.
Here also takes place to send a live price.
Auxiliary functions such as percent counting.
"""


def live_price_of_cryptocurrencies():
    global time_update, time_update_stop, lst_name_of_cryptocurrencies_to_live_price

    dct_start_price = {}
    d1 = {}
    start_time = time.time()

    while True:
        if time_update_stop is True:
            # This function can be paused if the user so wishes. This line of code makes it possible.
            while True:
                if time_update_stop is False:
                    break
                sleep(10)

        current_time = time.time()
        current_time -= start_time
        if current_time >= 86400:
            start_time = time.time()
            dct_start_price.clear()

        for i in lst_name_of_cryptocurrencies_to_live_price:
            name = i.upper()
            if name not in dct_start_price.keys():
                start_price = get_currently_price_of_currency(name)
                d1[name] = start_price
                dct_start_price.update(d1)

            current_price = get_currently_price_of_currency(name)
            percentage = percentage_calculator(current_price, dct_start_price[name])
            current_price_print = name + " " + str(percentage) + "% | " + str(current_price) + " USD"

            bot.send_message(chat_id=1181399908, text=current_price_print)

        count = 0
        while True:
            count += 1
            if count >= time_update:
                break
            time.sleep(1)


def percentage_calculator(current_price, start_price):
    current_price = float(current_price)
    start_price = float(start_price)
    percentage = ((current_price - start_price) / start_price) * 100
    percentage = round(percentage, 2)
    return percentage


def price_alert_monitor():
    global sell_price, buy_price
    a = True
    sell_price_before = 0
    buy_price_before = 0
    while True:
        current_price = get_currently_price_of_currency("BTC")
        current_price_print = "BTC is " + str(current_price) + " USD"

        if sell_price != 1.1 and buy_price != 1.1:
            if a is True:
                a = price_lvl_alert(current_price, current_price_print, sell_price, buy_price)
                if a == 1:
                    sell_price_before = sell_price
                elif a == 2:
                    buy_price_before = buy_price
        if a == 1:
            if sell_price_before != sell_price:
                a = True
                sell_price_before = 0
        elif a == 2:
            if buy_price_before != buy_price:
                a = True
                buy_price_before = 0

        sleep(30)


def price_on_request(name):
    try:
        a1 = get_price_of_currency_from_coinbase(name)
        current_price = a1.split(" ")
        current_price_print = current_price[0] + " is " + current_price[1] + " USD"
        return current_price_print
    except AttributeError:
        return "You must enter a valid cryptocurrency name"


"""
here is the prices of all cryptocurrencies are checked and warnings are issued if the price of
a cryptocurrency goes up strongly.
"""


def main_alert_price_all_crypto():
    global lst_of_available_currencies, lst_of_currencies_and_price, dct_of_currencies_and_price_current
    get_all_available_crypto()  # only once is needed

    dct_of_currencies_and_price_start = check_all_price()
    start_time = time.time()
    while True:
        current_time = time.time()
        current_time -= start_time
        if current_time >= 86400:
            start_time = time.time()
            dct_of_currencies_and_price_start = check_all_price()

        dct_of_currencies_and_price_current.clear()
        dct_of_currencies_and_price_current = check_all_price()

        a1 = list(dct_of_currencies_and_price_start.values())  # list of values from dct
        b1 = list(dct_of_currencies_and_price_current.values())  # list of values from dct

        for i in range(len(a1)):

            percentage = percentage_calculator(b1[i], a1[i])
            if percentage >= 5:
                check_percentage(percentage, b1, i)
            elif percentage <= -5:
                check_percentage(percentage, b1, i)

        sleep(1)


def check_all_price():
    global lst_of_available_currencies, lst_of_currencies_and_price
    lst_of_currencies_and_price.clear()
    for i in lst_of_available_currencies:
        try:
            a = get_price_of_currency_from_coinbase(i)
            lst_of_currencies_and_price.extend(a.split(" "))
        except AttributeError:
            pass

    dct_of_currencies_and_price = convert(lst_of_currencies_and_price)
    return dct_of_currencies_and_price


def convert(lst):
    # convert list to dictionary
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


def check_percentage(percentage, b1, i):
    global dct_of_currencies_and_price_current, dct_of_alert_name_percentage
    name_crypto = ""
    d1 = {}
    lst = []

    for key, value in dct_of_alert_name_percentage.items():
        if len(value) > 2:
            dct_of_alert_name_percentage[key].pop(0)

    price = round(float(b1[i]), 2)
    for key1, value1 in dct_of_currencies_and_price_current.items():
        if b1[i] == value1:
            name_crypto = key1

    if name_crypto not in dct_of_alert_name_percentage:
        lst.append(int(percentage))
        d1[name_crypto] = lst
        dct_of_alert_name_percentage.update(d1)
        bot.send_message(chat_id=1181399908,
                         text=f"Alert price {name_crypto} {percentage}% | {price}")
    elif name_crypto in dct_of_alert_name_percentage:
        if int(percentage) not in dct_of_alert_name_percentage[name_crypto]:
            dct_of_alert_name_percentage[name_crypto].append(int(percentage))
            bot.send_message(chat_id=1181399908,
                             text=f"Alert price {name_crypto} {percentage}% | {price}")


"""
This is place for telegram bot. Put here api key and other custom stuff.
"""

# here create global variables for telegram module


# bot = Bot("1947691149:AAF9ZqpE_s43XEflZE5HCAQeNn1_4JrNMJU")   # main
bot = Bot("1968009671:AAFyFLX4efJbsjnRlKeXfSRvXYwJo60Udic")  # dev


def start_command(update, context):
    update.message.reply_text("This is premium private bot. You can't use it without permission")
    # json_id = update
    # id_of_chat = json_id["message"]["chat"]["id"]
    # print(id_of_chat)


def help_command(update, context):
    update.message.reply_text("This is not working.")


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = "test is correct"
    update.message.reply_text(response)


def price_command(update, context):
    update.message.reply_text(price_on_request("BTC"))


def change_settings(update, context):
    json_id = update

    if json_id["message"]["chat"]["id"] != 1181399908:
        update.message.reply_text("You don't have permission.")
        return

    global sell_price, buy_price, time_update, time_update_stop, \
        lst_name_of_cryptocurrencies_to_live_price

    text = str(update.message.text).lower()
    if text[:4] == "help":
        update.message.reply_text("You can use:")
        update.message.reply_text("up => e.g. => [up4000] | This is for the upper limit of the price.")
    elif text[:2] == "up":
        if text[2:] == "":
            update.message.reply_text("Enter a value")
        elif float(text[2:]) > buy_price:
            sell_price = float(text[2:])
            update.message.reply_text(f"Price up set to: {sell_price}")
        else:
            update.message.reply_text("Sell price can't be lower than buy price")
    elif text[:4] == "down":
        if text[4:] == "":
            update.message.reply_text("Enter a value")
        elif sell_price == 1.1:
            update.message.reply_text("First, establish the upper limit")
        elif float(text[4:]) < sell_price:
            buy_price = float(text[4:])
            update.message.reply_text(f"Price down set to: {buy_price}")
        else:
            update.message.reply_text("Buy price can't be bigger than sell price")
    elif text[:4] == "time":
        try:
            time_update = int(text[4:])
            time_update = time_update * 60
            update.message.reply_text(f"Time set to: {time_update} seconds")
        except ValueError:
            update.message.reply_text("Can't to be float or empty.")
    elif text[:6] == "tstart":
        time_update_stop = False
        update.message.reply_text("Send message with live price of crypto is start.")
    elif text[:5] == "tstop":
        time_update_stop = True
        update.message.reply_text("Send message with live price of crypto is stop.")
    elif text[:3] == "add":
        lst_name_of_cryptocurrencies_to_live_price.append(text[3:])
        update.message.reply_text(f"{text[3:]} has been added to the live price.")
    elif text[:6] == "remove":
        lst_name_of_cryptocurrencies_to_live_price.remove(text[6:])
        update.message.reply_text(f"{text[6:]} has been remove from live price.")
    elif text[:5] == "price":
        update.message.reply_text(price_on_request(text[5:]))


def alert_price(message_alert):
    bot.send_message(chat_id=1181399908, text=message_alert)


def telegram_main():
    # updater = Updater("1947691149:AAF9ZqpE_s43XEflZE5HCAQeNn1_4JrNMJU", use_context=True) # main
    updater = Updater("1968009671:AAFyFLX4efJbsjnRlKeXfSRvXYwJo60Udic", use_context=True)  # for dev and test
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("price", price_command))

    dp.add_handler(MessageHandler(Filters.text, change_settings))

    updater.start_polling(1)


def price_lvl_alert(price, price_print, up_lvl, down_lvl):
    if float(price) >= up_lvl:
        alert_price(f"Alert price for sell! The price has hit the high end. | {price_print}")
        alert_price(f"Update brake point of price.")
        return 1
    elif float(price) <= down_lvl:
        alert_price(f"Alert price for buy! The price has hit the low end. | {price_print}")
        alert_price(f"Update brake point of price.")
        return 2
    else:
        return True
