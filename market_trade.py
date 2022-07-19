from binance.spot import Spot as Client
from binance.error import ClientError
import binance

from api_database import get_api_k_s
from binance_config import binance_url

def market_params_data(symbol=None,side=None,type=None,quantity=None):
    from spot_main_logic import get_rong
    a = get_rong(symbol)
    q_s = str(quantity)
    q_e = q_s[:a]
    params = {
        "symbol": symbol,
        "side": side,
        "type": type,
        "quantity": float(q_e)
    }
    return params

def market_trade(a_name,api_name,params,url=binance_url):
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
from spot_main_logic import get_coin_price
from limit_trade import percent_meth

from limit_trade import percent_meth,percent_meth1
def market_meth(a_name, api_name, symbol, side, type, quantity=None, percent=None, coin_balance=None):

    if bool(percent) is True:
        if side == "BUY":
            percent_result = percent_meth(a_name,api_name,percent,coin_balance,symbol)
            if percent_result != "get_balance error":
                return market_trade(a_name,api_name,market_params_data(symbol,side,type,quantity=percent_result))
            else:
                data = {}
                data['status'] = 2
                data['data'] = percent_result
                return data
        else:
            percent_result = percent_meth1(a_name,api_name,percent,coin_balance,symbol)
            if percent_result != "get_balance error":
                return market_trade(a_name,api_name,market_params_data(symbol,side,type,quantity=percent_result))
            else:
                data = {}
                data['status'] = 2
                data['data'] = percent_result
                return data

    else:
        return market_trade(a_name,api_name,market_params_data(symbol,side,type,quantity=quantity))


"""
def sell_with_one_click(a_name=None,api_name=None, symbol=None, side=None, type=None, quantity=None, percent=None, coin_balance=None):
    #quantity_result = float(coin_balance) / float(get_coin_price(symbol))
    #market_trade(a_name,api_name,market_params_data(symbol,side="BUY",type="MARKET",quantity=quantity_result))
    percent_result = percent_meth1(a_name=a_name, api_name=api_name, percent="96%", coin_balance=coin_balance,symbol=symbol)
    if percent_result != "get_balance error":
        return market_trade(a_name, api_name, market_params_data(symbol=symbol, side="SELL", type="MARKET", quantity=percent_result))
    else:
        data = {}
        data['status'] = 2
        data['data'] = percent_result
        return data
#print(sell_with_one_click(a_name='test1',api_name='trade1',symbol='TRXUSDT',coin_balance="20"))
"""
def sell_with_one_click(a_name=None,api_name=None, symbol=None, side=None, type=None, quantity=None, percent=None, coin_balance=None):
    index = 0
    while index < 3:
        try:
            get_ks = get_api_k_s(a_name,api_name)
            con = Client(get_ks["k"],get_ks["s"],base_url=binance_url)
            openorder_result = con.get_open_orders()
            print(openorder_result)
            break
        except binance.error.ClientError as err:
            if str(err.error_message) == "Timestamp for this request is outside of the recvWindow.":
                index = index + 1
                continue
            else:
                data = {}
                data['status'] = 2
                data['data'] = err.error_message
                return data
print(sell_with_one_click("adolph","binance1"))
