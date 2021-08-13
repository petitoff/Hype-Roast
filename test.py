# from core import *
#
#
# # get_all_available_crypto()
# #
# # for i in lst_of_available_currencies:
# #     try:
# #         a = get_price_of_currency(i)
# #         lst_of_currencies_and_price.extend(a.split(" "))
# #     except AttributeError:
# #         pass
# #
# # dct_of_currencies_and_price = convert(lst_of_currencies_and_price)
# # print(dct_of_currencies_and_price["BTC"])
#
#
# def live_price_of_btc():
#     while True:
#         a = get_price_of_currency("BTC")
#         print(a)
#         time.sleep(time_update)
#
#
# thread1 = Thread(target=live_price_of_btc)
# thread1.daemon = True
# thread1.start()
#
# while True:
#     try:
#         pass
#     except KeyboardInterrupt:
#         break
a = {'ALGO': '0.9411', 'DASH': '187.908', 'OXT': '0.3965', 'ATOM': '14.876', 'KNC': '1.8305', 'MIR': '3.657',
     'REP': '28.47', 'ICP': '66.721', 'CGLD': '3.0988', 'COMP': '477.97', 'NMR': '41.889', 'ACH': '0.089806',
     'BAND': '8.1964', 'XLM': '0.35769', 'EOS': '4.996', 'ZRX': '1.035428', 'BAT': '0.76047988570208', 'UNI': '29.6851',
     'YFI': '40451.37', 'LRC': '0.3061', 'CVC': '0.33606666582919', 'DNT': '0.19082970143021',
     'MANA': '0.82913875067247', 'REN': '0.508', 'LINK': '26.69957', 'BTC': '46654.17', 'BAL': '26.73805',
     'LTC': '181.17', 'ETH': '3240.05', 'BCH': '641.22', 'ETC': '62.726', 'USDC': '1.0', 'ZEC': '140.11',
     'RLC': '4.066', 'DAI': '1.000968', 'WBTC': '46704.08', 'NU': '0.291', 'FIL': '71.2093', 'AAVE': '417.547',
     'SNX': '11.7854', 'BNT': '4.1829', 'GRT': '0.91', 'SUSHI': '12.182', 'MLN': '95.197', 'ANKR': '0.10027',
     'CRV': '2.1875', 'STORJ': '1.2267', 'SKL': '0.3135', 'AMP': '0.06147', '1INCH': '3.021', 'ENJ': '1.655',
     'NKN': '0.4174', 'OGN': '0.989', 'FORTH': '18.25', 'GTC': '8.78', 'TRB': '49.411', 'XTZ': '3.5701',
     'CTSI': '0.7148', 'MKR': '3629.8335', 'UMA': '11.452', 'DOGE': '0.2789', 'ADA': '2.04', 'USDT': '1.0003',
     'DOT': '21.987', 'CHZ': '0.3772', 'SOL': '44.157', 'BOND': '26.66', 'LPT': '19.03', 'QNT': '157.93',
     'KEEP': '0.4055', 'CLV': '1.55', 'MASK': '6.51', 'MATIC': '1.4233', 'OMG': '5.5431', 'POLY': '0.3045',
     'FARM': '289.09', 'FET': '0.5221', 'PAX': '1.0', 'RLY': '0.542', 'PLA': '0.9981', 'RAI': '3.0191',
     'IOTX': '0.10777', 'ORN': '9.23', 'AXS': '71.06', 'QUICK': '881.55', 'TRIBE': '0.6883', 'UST': '1.003',
     'REQ': '0.32726', 'TRU': '0.752', 'WLUNA': '17.43'}
b = {'ALGO': '0.9409', 'DASH': '187.908', 'OXT': '0.3965', 'ATOM': '14.886', 'KNC': '1.8305', 'MIR': '3.657',
     'REP': '28.47', 'ICP': '66.683', 'CGLD': '3.1007', 'COMP': '477.99', 'NMR': '41.889', 'ACH': '0.089805',
     'BAND': '8.1964', 'XLM': '0.357557', 'EOS': '4.996', 'ZRX': '1.035775', 'BAT': '0.76060170876451', 'UNI': '29.716',
     'YFI': '40446.9', 'LRC': '0.3065', 'CVC': '0.33653993252627', 'DNT': '0.18949326710089', 'MANA': '0.8284640169686',
     'REN': '0.508', 'LINK': '26.69198', 'BTC': '46683.1', 'BAL': '26.75837', 'LTC': '181.42', 'ETH': '3241.83',
     'BCH': '641.22', 'ETC': '62.771', 'USDC': '1.0', 'ZEC': '140.11', 'RLC': '4.067', 'DAI': '1.00097',
     'WBTC': '46704.08', 'NU': '0.291', 'FIL': '71.2093', 'AAVE': '417.547', 'SNX': '11.7877', 'BNT': '4.1829',
     'GRT': '0.9098', 'SUSHI': '12.183', 'MLN': '95.863', 'ANKR': '0.1003', 'CRV': '2.1864', 'STORJ': '1.2251',
     'SKL': '0.3135', 'AMP': '0.06147', '1INCH': '3.021', 'ENJ': '1.655', 'NKN': '0.4162', 'OGN': '0.991',
     'FORTH': '18.29', 'GTC': '8.78', 'TRB': '49.411', 'XTZ': '3.5711', 'CTSI': '0.7148', 'MKR': '3629.8335',
     'UMA': '11.45', 'DOGE': '0.2789', 'ADA': '2.0408', 'USDT': '1.0003', 'DOT': '21.987', 'CHZ': '0.3772',
     'SOL': '44.157', 'BOND': '26.66', 'LPT': '19.03', 'QNT': '157.93', 'KEEP': '0.4063', 'CLV': '1.55', 'MASK': '6.51',
     'MATIC': '1.4233', 'OMG': '5.5439', 'POLY': '0.3045', 'FARM': '289.09', 'FET': '0.5224', 'PAX': '1.0',
     'RLY': '0.542', 'PLA': '0.9981', 'RAI': '3.0191', 'IOTX': '0.10756', 'ORN': '9.23', 'AXS': '71.06',
     'QUICK': '881.55', 'TRIBE': '0.6883', 'UST': '1.003', 'REQ': '0.32662', 'TRU': '0.7511', 'WLUNA': '17.43'}

# res = list(a.values())[0]
# print(res)

a1 = list(a.values())
b1 = list(b.values())

print(a1)
print(b1)

for i in range(len(a1)):
    if a1[i] == b1[i]:
        print("tak")
