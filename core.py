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
lst_of_alert_crypto = []

sell_price = 1.1
buy_price = 1.1
time_update = 600

"""
This is place for coinbase part
"""


def get_all_available_crypto():
    url = 'https://api.pro.coinbase.com/currencies'
    response = requests.get(url).json()

    for i in range(len(response)):
        if response[i]['details']['type'] == 'crypto':
            lst_of_available_currencies.append(response[i]['id'])


def get_price_of_currency(name):
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


"""
This is place for crypto, math and other function. Here you should put functions that will be executed in main.py.
"""


def live_price_of_btc():
    global time_update

    a1 = get_price_of_currency("BTC")
    start_price = a1.split(" ")
    while True:
        a = get_price_of_currency("BTC")
        current_price = a.split(" ")

        percentage = percentage_calculator(current_price[1], start_price[1])
        current_price_print = current_price[0] + " " + str(percentage) + "% | " + current_price[1] + " USD"

        bot.send_message(chat_id=1181399908, text=current_price_print)

        time.sleep(time_update)


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
        a1 = get_price_of_currency("BTC")
        current_price = a1.split(" ")
        current_price_print = current_price[0] + " is " + current_price[1] + " USD"

        if sell_price != 1.1 and buy_price != 1.1:
            if a is True:
                a = price_lvl_alert(float(current_price[1]), current_price_print, sell_price, buy_price)
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

        sleep(60)


def price_on_request():
    a1 = get_price_of_currency("BTC")
    current_price = a1.split(" ")
    current_price_print = current_price[0] + " is " + current_price[1] + " USD"
    return current_price_print


# here the prices of all cryptocurrencies are checked and warnings are issued if the price of
# a cryptocurrency goes up strongly.

def main_alert_price_all_crypto():
    global lst_of_available_currencies, lst_of_currencies_and_price, lst_of_alert_crypto
    get_all_available_crypto()  # only once is needed

    dct_of_currencies_and_price_start = check_all_price()
    start_time = time.time()
    while True:
        current_time = time.time()
        current_time -= start_time
        if current_time >= 86400:
            start_time = time.time()
            dct_of_currencies_and_price_start = check_all_price()

        dct_of_currencies_and_price_current = check_all_price()

        a1 = list(dct_of_currencies_and_price_start.values())  # list of values from dct
        b1 = list(dct_of_currencies_and_price_current.values())  # list of values from dct

        for i in range(len(a1)):
            name_crypto = ""

            percentage = percentage_calculator(b1[i], a1[i])
            if percentage >= 10:
                for key1, value1 in dct_of_currencies_and_price_current.items():
                    if b1[i] == value1:
                        name_crypto = key1
                if name_crypto not in lst_of_alert_crypto:
                    bot.send_message(chat_id=1181399908, text=f"Alert price {name_crypto} {percentage}% | {b1[i]}")
                    lst_of_alert_crypto.append(name_crypto)
            elif percentage <= -10:
                for key1, value1 in dct_of_currencies_and_price_current.items():
                    if b1[i] == value1:
                        name_crypto = key1
                if name_crypto not in lst_of_alert_crypto:
                    bot.send_message(chat_id=1181399908, text=f"Alert price {name_crypto} {percentage}% | {b1[i]}")
                    lst_of_alert_crypto.append(name_crypto)

        sleep(1)


def check_all_price():
    global lst_of_available_currencies, lst_of_currencies_and_price
    lst_of_currencies_and_price.clear()
    for i in lst_of_available_currencies:
        try:
            a = get_price_of_currency(i)
            lst_of_currencies_and_price.extend(a.split(" "))
        except AttributeError:
            pass

    dct_of_currencies_and_price = convert(lst_of_currencies_and_price)
    return dct_of_currencies_and_price


def convert(lst):
    # convert list to dictionary
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


"""
This is place for telegram bot. Put here api key and other custom stuff.
"""

# here create global variables for telegram module


bot = Bot("1947691149:AAF9ZqpE_s43XEflZE5HCAQeNn1_4JrNMJU")   # main
# bot = Bot("1968009671:AAFyFLX4efJbsjnRlKeXfSRvXYwJo60Udic")  # dev


def start_command(update, context):
    update.message.reply_text("This is premium private bot. You can't use it without permission")
    # json_id = update
    # id_of_chat = json_id["message"]["chat"]["id"]
    # print(id_of_chat)


def help_command(update, context):
    update.message.reply_text("Available commands: up, down, time")


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = "test is correct"
    update.message.reply_text(response)


def price_command(update, context):
    update.message.reply_text(price_on_request())


def change_settings(update, context):
    json_id = update

    if json_id["message"]["chat"]["id"] != 1181399908:
        update.message.reply_text("You don't have permission.")
        return

    global sell_price, buy_price, time_update, lst_of_alert_crypto
    text = str(update.message.text).lower()
    if text[:2] == "up":
        if float(text[2:]) > buy_price:
            sell_price = float(text[2:])
            update.message.reply_text(f"Price up set to: {sell_price}")
        else:
            update.message.reply_text("Sell price can't be lower than buy price")
    elif text[:4] == "down":
        if float(text[4:]) < sell_price:
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
            update.message.reply_text("Can't to be float or int.")
    elif text == "clear1":
        update.message.reply_text("The list of alerts has been cleared")
        lst_of_alert_crypto.clear()


def alert_price(message_alert):
    bot.send_message(chat_id=1181399908, text=message_alert)


def main():
    updater = Updater("1947691149:AAF9ZqpE_s43XEflZE5HCAQeNn1_4JrNMJU", use_context=True) # main
    # updater = Updater("1968009671:AAFyFLX4efJbsjnRlKeXfSRvXYwJo60Udic", use_context=True)  # for dev and test
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
