from binance.spot import Spot as Client
import time
from binance.error import ClientError
import binance

from api_database import get_api_k_s
from binance_config import binance_url

def get_oepn_order(a_name,api_name,symbol,url=binance_url):
    index = 0
    while index < 3:
        try:
            get_ks = get_api_k_s(a_name,api_name)
            con = Client(get_ks["k"],get_ks["s"],base_url=url)
            list = []
            response = con.get_open_orders(symbol,recvWindow=6000)
            index = 0
            while index < len(response):
                result = {}
                result['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(response[index]['updateTime'] / 1000))
                result['orderId'] = response[index]['orderId']
                result['symbol'] = response[index]['symbol']
                result['type'] = response[index]['type']
                result['side'] = response[index]['side']
                result['price'] = response[index]['price']
                result['quantity'] = response[index]['origQty']
                result['executed'] = response[index]['executedQty']
                result['stopPrice'] = response[index]['stopPrice']

                list.append(result)
                index = index + 1
                continue
            return list
        except binance.error.ClientError as err:
            if str(err.error_message) == "Timestamp for this request is outside of the recvWindow.":
                index = index + 1
                continue
            else:
                data = {}
                data['status'] = 2
                data['data'] = err.error_message
                return data
#print(get_oepn_order('test1','trade1',"TRXUSDT"))


def finish_order(a_name,api_name,symbol,get_all=None,url=binance_url):
    index = 0
    while index < 3:
        try:
            get_ks = get_api_k_s(a_name,api_name)
            con = Client(get_ks["k"],get_ks["s"],base_url=url)
            if bool(get_all) is True:
                response = con.my_trades(symbol)
                list = []
                index = 0
                while index < len(response):
                    result = {}
                    result['tiem'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(response[index]['time'] / 1000))
                    result['symbol'] = response[index]['symbol']
                    if bool(response[index]['isBuyer']) == False:
                        result['side'] = "SELL"
                    else:
                        result['side'] = "BUY"
                    result['price'] = response[index]['price']
                    result['commission'] = response[index]['commission']
                    result['quoteQty'] = response[index]['quoteQty']
                    list.append(result)
                    index = index + 1
                    continue
                return list
            else:
                response = con.my_trades(symbol,limit="20")
                list = []
                index = 0
                while index < len(response):
                    result = {}
                    result['tiem'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(response[index]['time'] / 1000))
                    result['symbol'] = response[index]['symbol']
                    if bool(response[index]['isBuyer']) == False:
                        result['side'] = "SELL"
                    else:
                        result['side'] = "BUY"
                    result['price'] = response[index]['price']
                    result['commission'] = response[index]['commission']
                    result['quoteQty'] = response[index]['quoteQty']
                    list.append(result)
                    index = index + 1
                    continue
                return list
        except binance.error.ClientError as err:
            if str(err.error_message) == "Timestamp for this request is outside of the recvWindow.":
                index = index + 1
                continue
            else:
                data = {}
                data['status'] = 2
                data['data'] = err.error_message
                return data
#print(finish_order('test1','trade1','TRXUSDT'))