from binance.spot import Spot as Client
from binance.error import ClientError
import binance
from api_database import get_api_k_s
from binance_config import binance_url

def take_profit_data(symbol=None,side=None,type=None,timeInForce="GTC",quantity=None,price=None,stopPrice=None):
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
        "price": float(price),
        "stopPrice" : float(stopPrice)
    }
    return params

def take_trade(a_name,api_name,params,url=binance_url):
    index = 0
    while index < 3:
        try:
            get_ks = get_api_k_s(a_name,api_name)
            con = Client(get_ks["k"],get_ks["s"],base_url=url)
            return con.new_order(**params)
        except binance.error.ClientError as err:
            if str(err.error_message) == "Timestamp for this request is outside of the recvWindow.":
                index = index + 1
                continue
            else:
                data = {}
                data['status'] = 2
                data['data'] = err.error_message
                return data



def take_meth(a_name=None,api_name=None,symbol=None,side=None,type=None,quantity=None,price=None,stopPrice=None,percent=None,coin_balance=None):
    from limit_trade import percent_meth, percent_meth1
    if bool(percent) is True:
        if side == "BUY":
            percent_result = percent_meth(a_name,api_name,percent,coin_balance,symbol)
            if percent_result != "get_balance error":
                return take_trade(a_name,api_name,take_profit_data(symbol,side,type,timeInForce="GTC",quantity=percent_result,price=price,stopPrice=stopPrice))
            else:
                data = {}
                data['status'] = 2
                data['data'] = percent_result
                return data
        else:
            percent_result = percent_meth1(a_name,api_name,percent,coin_balance,symbol)
            if percent_result != "get_balance error":
                return take_trade(a_name,api_name,take_profit_data(symbol,side,type,timeInForce="GTC",quantity=percent_result,price=price,stopPrice=stopPrice))
            else:
                data = {}
                data['status'] = 2
                data['data'] = percent_result
                return data
    else:
        take_trade(a_name,api_name,take_profit_data(symbol,side,type=type,timeInForce="GTC",quantity=quantity,price=price,stopPrice=stopPrice))

#take_meth('test','trade1','TRXUSDT','SELL','TAKE_PROFIT_LIMIT',150,'0.09','0.1')