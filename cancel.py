from binance.spot import Spot as Client

from binance.error import ClientError
import binance
from api_database import get_api_k_s
from binance_config import binance_url

def cancel_order(a_name,api_name,symbol,orderid,url=binance_url):
    index = 0
    while index < 3:
        try:
            get_ks = get_api_k_s(a_name,api_name)
            con = Client(get_ks["k"],get_ks["s"],base_url=url)
            return con.cancel_order(symbol,orderId=orderid)
        except binance.error.ClientError as err:
            if str(err.error_message) == "Timestamp for this request is outside of the recvWindow.":
                index = index + 1
                continue
            else:
                data = {}
                data['status'] = 2
                data['data'] = err.error_message
                return data
#print(cancel_order('test','trade1',"TRXUSDT","1959275046"))

def cancel_open_order(a_name,api_name,symbol,url=binance_url):
    index = 0
    while index < 3:
        try:
            get_ks = get_api_k_s(a_name,api_name)
            con = Client(get_ks["k"],get_ks["s"],base_url=url)
            return con.cancel_open_orders(symbol)
        except binance.error.ClientError as err:
            if str(err.error_message) == "Timestamp for this request is outside of the recvWindow.":
                index = index + 1
                continue
            else:
                data = {}
                data['status'] = 2
                data['data'] = err.error_message
                return data
#print(cancel_open_order('test','trade1',"TRXUSDT"))

