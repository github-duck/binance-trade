from binance.spot import Spot as Client

import binance
from binance.error import ClientError


from api_database import get_api_k_s
from binance_config import binance_url


def get_balances(a_name,api_name,l_symbol,r_symbol,url=binance_url):
    index = 0
    while index < 3:
        try:
            result = get_api_k_s(a_name,api_name)
            coin = Client(result["k"],result["s"],base_url=url)
            balances_coin = coin.account(recvWindow=6000)["balances"]
            symbol_total = {}
            def get_l_symbol(l_symbol):
                index = 0
                while index < len(balances_coin):
                    if balances_coin[index]["asset"] != l_symbol:
                        index = index + 1
                        continue
                    else:
                        symbol_total["l_symbol"] = balances_coin[index]["free"]
                        break
            get_l_symbol(l_symbol)
            def get_r_symbol(r_symbol):
                index = 0
                while index < len(balances_coin):
                    if balances_coin[index]["asset"] != r_symbol:
                        index = index + 1
                        continue
                    else:
                        symbol_total["r_symbol"] = balances_coin[index]["free"]
                        break
            get_r_symbol(r_symbol)
            return symbol_total
        except binance.error.ClientError as err:
            if str(err.error_message) == "Timestamp for this request is outside of the recvWindow.":
                index = index + 1
                continue
            else:
                return str(err.error_message)

#print(get_balances("test1","trade1","TRX","USDT"))
#Timestamp for this request is outside of the recvWindow.
def get_coin_balance(a_name,api_name,symbol,url=binance_url):
    index = 0
    while index < 3:
        try:
            result = get_api_k_s(a_name,api_name)
            coin = Client(result["k"],result["s"],base_url=url)
            balances_coin = coin.account(recvWindow=6000)["balances"]
            index = 0
            while index < len(balances_coin):
                if balances_coin[index]["asset"] != symbol:
                    index = index + 1
                    continue
                else:
                    return balances_coin[index]["free"]
        except binance.error.ClientError as err:
            if str(err.error_message) == "Timestamp for this request is outside of the recvWindow.":
                index = index + 1
                continue
            else:
                data = {}
                data['status'] = 2
                data['data'] = "get_balance error"
                return data
#print(get_coin_balance('test1','trade1','TRX'))

def get_coin_price(symbol):
    result = Client(base_url=binance_url)
    return result.ticker_price(symbol,)["price"]
#print(get_coin_price("TRXUSDT"))


def get_rong(symbol,url=binance_url):
    coin = Client(base_url=url)
    result = coin.exchange_info(symbol)
    a = result['symbols'][0]['filters'][2]['stepSize']
    index1 = 1
    for i in a:
        if i == "1":
            return len(a[:index1])
        else:
            index1 = index1+1
#print(get_rong("TRXUSDT"))

def get_price_rong(symbol,url=binance_url):
    coin = Client(base_url=url)
    result = coin.exchange_info(symbol)
    a = result['symbols'][0]['filters'][0]['tickSize']
    index1 = 1
    for i in a:
        if i == "1":
            return len(a[:index1])
        else:
            index1 = index1+1
#print(get_price_rong("TRXUSDT"))