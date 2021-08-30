import json
import urllib
import urllib.request
import requests
import time
from time import sleep
from threading import Thread

from telegram import *
from telegram.ext import *

from coinbase.wallet.client import Client
from coinbase.wallet.error import AuthenticationError

"""here create global variables for coinbase module"""
lst_of_available_currencies = []
lst_name_of_cryptocurrencies_to_live_price = ["BTC"]
lst_name_cryptocurrencies_breakpoint = []

dct_of_currencies_and_price_main = {}
dct_name_value_breakpoint = {}  # A dictionary that keeps the names and values of cryptocurrencies with levels
# when an alert is to be triggered.

time_update = 600  # Every how many seconds a price update is to be sent. This is the default value and can be
# changed by the user.

time_update_stop = False  # Variable that tells the program whether price updates are to be sent.

count_coinbase_main_1 = 0
# The variable informs the program whether the value has been downloaded from the API once. If so, the program
# starts the rest of the threads.


"""
Here are all the working functions used by the entire program installation down to one section in the code
"""


def percentage_calculator(current_price, start_price):
    current_price = float(current_price)
    start_price = float(start_price)
    percentage = ((current_price - start_price) / start_price) * 100
    percentage = round(percentage, 2)
    return percentage


def convert(lst):
    # convert list to dictionary
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


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

    try:
        price = dct_of_currencies_and_price_main[name.upper()][-1]
        return price
    except KeyError:
        return "Wait a moment and try again. The price has not yet been downloaded from API."


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
        sleep(60)


"""
coinbase convert, buy and sell.
"""


class Coinbase:
    def coinbase_import_api(self):
        with open("key.json", 'r') as f:
            api_keys = json.loads(f.read())
            api_key = api_keys["coinbase"]["apiKey"]
            secret_key = api_keys["coinbase"]["secretKey"]

            return api_key, secret_key

    def coinbase_check_wallet_balance(self, name):
        # get balance for each wallet

        self.json_data_wallet = self.client.get_account(name)

    def coinbase_convert_on_breakpoint(self, name):
        self.coinbase_check_wallet_balance(name)

    def main_coinbase_api(self):
        api_key, secret_key = self.coinbase_import_api()

        self.client = Client(api_key, secret_key)


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


def price_alert_monitor():
    global dct_name_value_breakpoint
    a = True
    sell_price = float
    buy_price = float
    while True:
        for key in dct_name_value_breakpoint.keys():
            current_price = get_currently_price_of_currency(key)
            current_price_print = key + " is " + str(current_price) + " USD"

            try:
                sell_price = dct_name_value_breakpoint[key]["up"][0]
                buy_price = dct_name_value_breakpoint[key]["down"][0]
            except KeyError:
                pass

            try:
                if type(sell_price) is not type and type(buy_price) is not type:
                    if float(current_price) >= sell_price and dct_name_value_breakpoint[key]["up"][1] is False:
                        alert_price(f"Alert price for sell! The price has hit the high end. | {current_price_print}")
                        alert_price(f"Update brake point of price.")
                        dct_name_value_breakpoint[key]["up"][1] = True
                    elif float(current_price) <= buy_price and dct_name_value_breakpoint[key]["down"][1] is False:
                        alert_price(f"Alert price for sell! The price has hit the high end. | {current_price_print}")
                        alert_price(f"Update brake point of price.")
                        dct_name_value_breakpoint[key]["down"][1] = True
            except KeyError:
                pass
        sleep(1)


def price_on_request(name):
    # This function If the user sends a message "Price [Name]" returns the value (price) cryptos.
    try:
        price = get_currently_price_of_currency(name)
        if type(price) is int or type(price) is float:
            current_price_print = name.upper() + " is " + str(price) + " USD"
            return current_price_print
        else:
            return price
    except AttributeError:
        return "You must enter a valid cryptocurrency name"


"""
here is the prices of all cryptocurrencies are checked and warnings are issued if the price of
a cryptocurrency goes up strongly.
"""


class BigDifferencesInPrices:
    def __init__(self):
        self.dct_of_currencies_and_price_current = {}
        self.dct_of_alert_name_percentage = {}

    def main_alert_price_all_crypto(self):
        dct_of_currencies_and_price_start = self.check_all_price()
        start_time = time.time()
        while True:
            current_time = time.time()
            current_time -= start_time
            if current_time >= 86400:
                start_time = time.time()
                dct_of_currencies_and_price_start.clear()
                dct_of_currencies_and_price_start = self.check_all_price()

            self.dct_of_currencies_and_price_current.clear()
            self.dct_of_currencies_and_price_current = self.check_all_price()

            lst_local_start_price = list(dct_of_currencies_and_price_start.values())  # list of values from dct
            lst_local_current_price = list(self.dct_of_currencies_and_price_current.values())  # list of values from dct

            for i in range(len(lst_local_start_price)):
                percentage = percentage_calculator(lst_local_current_price[i], lst_local_start_price[i])
                if percentage >= 4 or percentage <= -4:
                    self.check_percentage(percentage, lst_local_current_price[i])

            sleep(10)

    def check_all_price(self):
        global dct_of_currencies_and_price_main

        dct_local_of_currencies_and_price = {}

        for key, value in dct_of_currencies_and_price_main.items():
            dct_local = {key: value[-1]}
            dct_local_of_currencies_and_price.update(dct_local)

        return dct_local_of_currencies_and_price

    def check_percentage(self, percentage, lst_local_current_price):
        name_crypto = ""

        price = round(lst_local_current_price, 2)
        for key1, value1 in self.dct_of_currencies_and_price_current.items():
            if lst_local_current_price == value1:
                name_crypto = key1

        if name_crypto not in self.dct_of_alert_name_percentage:
            self.dct_of_alert_name_percentage.update({name_crypto: int(percentage)})
            bot.send_message(chat_id=1181399908,
                             text=f"Alert price {name_crypto} {percentage}% | {price}")
        else:
            if int(percentage) != self.dct_of_alert_name_percentage[name_crypto]:
                self.dct_of_alert_name_percentage.update({name_crypto: int(percentage)})
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
    update.message.reply_text("If you want help, type help.")


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = "test is correct"
    update.message.reply_text(response)


def status_command(update, context):
    update.message.reply_text("I'm alive and well.")


def change_settings(update, context):
    json_id = update

    if json_id["message"]["chat"]["id"] != 1181399908:
        update.message.reply_text("You don't have permission.")
        return

    global time_update, time_update_stop, count_coinbase_main_1, \
        lst_name_of_cryptocurrencies_to_live_price, lst_of_available_currencies, dct_name_value_breakpoint

    text = str(update.message.text).lower()
    if text[:4] == "help":
        update.message.reply_text("You can use:")
        update.message.reply_text("up 'name_crypto price => e.g. => [up btc 40000] | "
                                  "This is for the upper limit of the price.")
        update.message.reply_text("down 'name_crypto' 'price' => e.g. => [down btc 35000] | "
                                  "This is for the downer limit of the price.")
        update.message.reply_text("time'minutes' => e.g. => [time10] | "
                                  "Every how many minutes notifications about the price of cryptocurrencies are "
                                  "to be sent.")
        update.message.reply_text("add'name_crypto' => e.g. => [addbtc] | Adding any cryptocurrency to the live price.")
        update.message.reply_text("remove'name_crypto' => e.g. => [removebtc] | "
                                  "Remove any cryptocurrency in the live price.")
        update.message.reply_text("tstart | Running Live Price (enabled by default).")
        update.message.reply_text("tstop | Live price exclusion.")
        update.message.reply_text("price'name_crypto' => e.g. => [pricebtc] | "
                                  "Knowing the price of any cryptocurrency.")
    elif text[:2] == "up":
        if count_coinbase_main_1 == 0:
            update.message.reply_text("Wait for the program to fully start and try again.")
            return

        try:
            lst_local_setting = [i for i, ltr in enumerate(text) if ltr == " "]
            name_crypto = text[3:lst_local_setting[1]].upper()
            sell_price = float(text[lst_local_setting[1] + 1:])

            update.message.reply_text(f"Price up set to: {sell_price}")

            if name_crypto not in dct_name_value_breakpoint:
                dct_name_value_breakpoint.update({name_crypto: {"up": [sell_price, False]}})
            else:
                dct_name_value_breakpoint[name_crypto].update({"up": [sell_price, False]})

        except ValueError:
            update.message.reply_text(
                "Error! Please enter the correct form. If you do not know how, please enter help.")
    elif text[:4] == "down":
        if count_coinbase_main_1 == 0:
            update.message.reply_text("Wait for the program to fully start and try again.")
            return

        try:
            lst_local_setting = [i for i, ltr in enumerate(text) if ltr == " "]
            name_crypto = text[5:lst_local_setting[1]].upper()
            buy_price = float(text[lst_local_setting[1] + 1:])

            update.message.reply_text(f"Price down set to: {buy_price}")

            if name_crypto not in dct_name_value_breakpoint:
                dct_name_value_breakpoint.update({name_crypto: {"down": [buy_price, False]}})
            else:
                dct_name_value_breakpoint[name_crypto].update({"down": [buy_price, False]})
        except ValueError:
            update.message.reply_text("Error! Enter a value")
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
        if text[3:] in lst_of_available_currencies:
            lst_name_of_cryptocurrencies_to_live_price.append(text[3:])
            update.message.reply_text(f"{text[3:]} has been added to the live price.")
        else:
            update.message.reply_text("The given cryptocurrency does not exist or has not been loaded yet. "
                                      "Please try again in a minute!")
    elif text[:6] == "remove":
        try:
            lst_name_of_cryptocurrencies_to_live_price.remove(text[6:])
            update.message.reply_text(f"{text[6:]} has been remove from live price.")
        except ValueError:
            update.message.reply_text("The cryptocurrency with the given name is not on the list.")
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
    dp.add_handler(CommandHandler("status", status_command))

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
