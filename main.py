import time

import core
from core import *

# telegram bot and sending message (all api and other main def)
thread1 = Thread(target=coinbase_get_price)
# telegram bot and sending message (all api and other main def)
thread2 = Thread(target=telegram_main)
# get live price of BTC and send message via telegram
thread3 = Thread(target=live_price_of_cryptocurrencies)
# get alert price if BTC break set price via telegram
thread4 = Thread(target=price_alert_monitor)


thread5 = Thread(
    target=runBigDifferencesInPrices.main_alert_price_all_crypto)  # get alert price of all crypto if price if fast
# change


thread1.setDaemon(True)
thread1.start()

thread2.setDaemon(True)
thread2.start()

try:
    while True:
        time.sleep(1)
        if core.count_coinbase_main_1 == 1:
            thread3.setDaemon(True)
            thread3.start()

            thread4.setDaemon(True)
            thread4.start()

            thread5.setDaemon(True)
            thread5.start()
            break
except KeyboardInterrupt:
    pass

try:
    while True:
        # this is to keep the program alive
        pass
except KeyboardInterrupt:
    pass
