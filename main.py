from core import *

thread1 = Thread(target=main)  # telegram bot and sending message (all api and other main def)
thread2 = Thread(target=live_price_of_btc)  # get live price of BTC and send message via telegram
thread3 = Thread(target=price_alert_monitor)  # get alert price if BTC break set price via telegram
thread4 = Thread(target=main_alert_price_all_crypto)  # get alert price of all crypto if price is fast change


thread1.setDaemon(True)
thread1.start()

thread2.setDaemon(True)
thread2.start()

thread3.setDaemon(True)
thread3.start()

thread4.setDaemon(True)
thread4.start()


try:
    while True:
        # this is to keep the program alive
        pass
except KeyboardInterrupt:
    pass
