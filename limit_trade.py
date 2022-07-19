import os

from binance.spot import Spot as Client
from decimal import Decimal
from api_database import get_api_k_s
from binance_config import binance_url
from take_profit_limit import take_meth
from binance.error import ClientError
import binance




def spot_params_data(symbol=None,side=None,type=None,quantity=None,price=None,timeInForce="GTC"):
    from spot_main_logic import get_rong
    a = get_rong(symbol)
    q_s = str(quantity)
    q_e = q_s[:a]
    params = {
        "symbol": symbol,
        "side": side,
        "type": type,
        "timeInForce": timeInForce,
        "quantity": float(q_e),
        "price": float(price)

    }
    return params

from spot_main_logic import get_coin_balance
def percent_meth(a_name,api_name,percent,coin_balance,symbol):
    percent_convert = percent
    percent_result = float(percent_convert.strip('%'))
    price_result = percent_result / 100.00
    balance = get_coin_balance(a_name, api_name, coin_balance)
    if balance != "get_balance error":
        quantity_result = float(balance) * float(price_result) / float(get_coin_price(symbol))
        return quantity_result
    else:
        data = {}
        data['status'] = 2
        data['data'] = balance
        return data


def percent_meth1(a_name,api_name,percent,coin_balance,symbol):
    percent_convert = percent
    percent_result = float(percent_convert.strip('%'))
    price_result = percent_result / 100.00
    balance = get_coin_balance(a_name,api_name,coin_balance)
    if balance != "get_balance error":
        quantity_result = float(balance) * float(price_result)
        return quantity_result
    else:
        return balance

def limit_trade(a_name,api_name,params,url=binance_url):
    index = 0
    while index < 3:
        try:
            get_ks = get_api_k_s(a_name,api_name)
            con = Client(get_ks["k"],get_ks["s"],base_url=url)
            return con.new_order(**params,recvWindow=6000)
        except binance.error.ClientError as err:
            if str(err.error_message) == "Timestamp for this request is outside of the recvWindow.":
                index = index + 1
                continue
            else:
                data = {}
                data['status'] = 2
                data['data'] = err.error_message
                return data
#print(bool(limit_trade("test","trade1",spot_params_data("TRXUSDT","SELL","LIMIT","GTC",180,"0.1",))))
#print(limit_trade("adolph","binance1",spot_params_data("TRXUSDT","SELL","LIMIT",180,"0.08")))
def limit_trade1(a_name,api_name,params,url=binance_url):
    index = 0
    while index < 3:
        try:
            get_ks = get_api_k_s(a_name,api_name)
            con = Client(get_ks["k"],get_ks["s"],base_url=url)
            return con.new_order(**params,recvWindow=6000)['orderId']
        except binance.error.ClientError as err:
            if str(err.error_message) == "Timestamp for this request is outside of the recvWindow.":
                index = index + 1
                continue
            else:
                return ("Refresh page and Re-execute")
#print(limit_trade1("adolph","binance1",spot_params_data("TRXUSDT","SELL","LIMIT",180,"0.08")))
#curl -X 'POST' 'http://127.0.0.1:8000/api/com_trade' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"oid":"123"}'




from spot_main_logic import get_coin_price
def complex_judge_limit_trade(a_name=None,api_name=None,percent=None,coin_balance=None,symbol=None,
                              side=None,type=None,quantity=None,price=None,stopgold=None,stopPrice=None):
    from spot_main_logic import get_price_rong
    price_market = get_coin_price(symbol)
    sum1 = float(stopgold) / float(price_market)
    sum2 = float(stopPrice) / float(price_market)
    sum3 = float(1) - float(sum2)
    sum4 = sum1 / sum3
    sum5 = float(stopPrice) * 0.997
    sum6 = float(stopPrice) * 0.997 * 0.997
    str_sum6 = str(sum6)
    a = get_price_rong(symbol)
    sum7 = str_sum6[:a]
    str_sum5 = str(sum5)
    sum55 = str_sum5[:a]
    oid = limit_trade1(a_name, api_name,
                       spot_params_data(symbol=symbol, side=side, type="LIMIT", timeInForce="GTC", quantity=sum4,
                                        price=price_market))
    if oid != "Refresh page and Re-execute":
        import requests
        url = "http://127.0.0.1:8000/api/com_trade"
        data = {}
        data['a_name'] = a_name
        data['api_name'] = api_name
        data['coin_balance'] = coin_balance
        data['symbol'] = symbol
        data['price'] = sum7
        data['stopPrice'] = sum55
        data['oid'] = oid
        headers = {
            'accept': 'application/json',
            # Already added when you pass json=
            # 'Content-Type': 'application/json',
        }
        requests.post(url,headers=headers,json=data)
    else:
        data = {}
        data['status'] = 2
        data['data'] = oid
        return data
    """
    take_meth(a_name=a_name, api_name=api_name, percent="98%",
              coin_balance=coin_balance, symbol=symbol,
              side="SELL", type="STOP_LOSS_LIMIT",
              price=sum7, stopPrice=sum5)
    """
from binance_config import binance_url
def while_check_oid(a_name=None, api_name=None,coin_balance=None,
                    symbol=None,price=None, stopPrice=None,oid=None):
    index = 0
    while index < 3:
        try:
            get_ks = get_api_k_s(a_name,api_name)
            con = Client(get_ks["k"],get_ks["s"],base_url=binance_url)
            while True:
                respone = con.get_orders(symbol=symbol, orderId=oid,recvWindow=6000)
                if respone[0]['status'] == "FILLED":
                    take_meth(a_name=a_name, api_name=api_name, percent="98%",
                              coin_balance=coin_balance, symbol=symbol,
                              side="SELL", type="STOP_LOSS_LIMIT",
                              price=price, stopPrice=stopPrice)
                    break
                else:
                    import time
                    time.sleep(10)
                    continue
        except binance.error.ClientError as err:
            if str(err.error_message) == "Timestamp for this request is outside of the recvWindow.":
                index = index + 1
                continue
            else:
                return err.error_message





def linmit_trade_meth(a_name=None,api_name=None,percent=None,coin_balance=None,symbol=None,side=None,type=None,quantity=None,price=None):
    if bool(percent) is True:
        if side == "BUY":
            percent_result = percent_meth(a_name,api_name,percent,coin_balance,symbol)
            if percent_result != "get_balance error":
                return limit_trade(a_name,api_name,spot_params_data(symbol,side,type,timeInForce="GTC",quantity=percent_result,price=price))
            else:
                data = {}
                data['status'] = 2
                data['data'] = percent_result
                return data
        else:
            percent_result = percent_meth1(a_name,api_name,percent,coin_balance,symbol)
            if percent_result != "get_balance error":
                return limit_trade(a_name,api_name,spot_params_data(symbol,side,type,timeInForce="GTC",quantity=percent_result,price=price))
            else:
                data = {}
                data['status'] = 2
                data['data'] = percent_result
                return data
    else:
        limit_trade(a_name,api_name,spot_params_data(symbol,side,type,timeInForce="GTC",quantity=quantity,price=price))
#print(linmit_trade_meth('test1','trade1','50%','USDT','BTCUSDT','BUY','LIMIT',price="20000"))
