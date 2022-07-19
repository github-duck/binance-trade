from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main_logic import verify_login,verify_token
from origins import origins



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/login")
def login_api(data: dict):
    return verify_login(data['username'],data['password'])


from coin_list import get_coin_list
@app.post("/api/coin_list")
def coin_list_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return get_coin_list()
    else:
        result = {}
        result['status'] = 1
        return result

from api_database import get_apiname_list
@app.post("/api/account_list")
def account_list_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return get_apiname_list(data['username'])
    else:
        result = {}
        result['status'] = 1
        return result

from spot_main_logic import get_balances
@app.post("/api/coin_balance")
def coin_balance_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return get_balances(data['username'],data['api_name'],
                            data['l_symbol'],data['r_symbol'])
    else:
        result = {}
        result['status'] = 1
        return result

from limit_trade import linmit_trade_meth,complex_judge_limit_trade
@app.post("/api/complex_judge_limit")
def complex_judge_limit_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        mult = data['mult']
        return complex_judge_limit_trade(a_name=data['a_name'],api_name=data['api_name'],
                                symbol=data['symbol'],side=data['side'],
                                        stopPrice=data['stopPrice'],stopgold=data['stopgold'],coin_balance=data['coin_balance'])


@app.post("/api/limit_trade")
def limit_trade_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        mult = data['mult']
        if ('percent' in data.keys()) == True:
            return linmit_trade_meth(a_name=data['a_name'], api_name=data['api_name'], percent=data['percent'],
                                             coin_balance=data['coin_balance'],symbol=data['symbol'],
                                             side=data['side'],type=data['type'],
                                             price=data['price'])
        else:
            sum = data['quantity'] * mult
            return linmit_trade_meth(a_name=data['a_name'],api_name=data['api_name'],symbol=data['symbol'],
                                             side=data['side'],type=data['type'],quantity=sum,price=data['price'])
    else:
        result = {}
        result['status'] = 1
        return result

from market_trade import market_meth
@app.post("/api/market_trade")
def market_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        mult = data['mult']
        if ('percent' in data.keys()) == True:
            return market_meth(a_name=data['a_name'], api_name=data['api_name'], percent=data['percent'],
                                             coin_balance=data['coin_balance'],symbol=data['symbol'],
                                             side=data['side'],type=data['type'])
        else:
            sum = data['quantity'] * mult
            return market_meth(a_name=data['a_name'],api_name=data['api_name'],
                                             symbol=data['symbol'],side=data['side'],type=data['type'],quantity=sum)
    else:
        result = {}
        result['status'] = 1
        return result

from take_profit_limit import take_meth
@app.post("/api/take_meth")
def take_meth_api(data: dict):
    a = verify_token(data['token'])

    if a == True:
        mult = data['mult']
        if ('percent' in data.keys()) == True:
            return take_meth(a_name=data['a_name'], api_name=data['api_name'], percent=data['percent'],
                                             coin_balance=data['coin_balance'],symbol=data['symbol'],
                                             side=data['side'],type=data['type'],
                                             price=data['price'],stopPrice=data['stopPrice'])
        else:
            sum = data['quantity'] * mult
            return take_meth(a_name=data['a_name'],api_name=data['api_name'],symbol=data['symbol'],stopPrice=data['stopPrice'],
                                             side=data['side'],type=data['type'],quantity=sum,price=data['price'])
    else:
        result = {}
        result['status'] = 1
        return result

from market_trade import sell_with_one_click
@app.post("/api/sell_with_one_click")
def sell_all_api(data: dict):
    a = verify_token(data['token'])
    mult = data['mult']
    if a == True:
        cancel_open_order(a_name=data['a_name'], api_name=data['api_name'],
                          symbol=data['symbol'])
        return sell_with_one_click(a_name=data['a_name'], api_name=data['api_name'],
                                             coin_balance=data['coin_balance'],symbol=data['symbol'])
    else:
        result = {}
        result['status'] = 1
        return result




from bill import get_oepn_order
@app.post("/api/oepn_order")
def oepn_order_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return get_oepn_order(a_name=data['a_name'],api_name=data['api_name'],
                              symbol=data['symbol'])
    else:
        result = {}
        result['status'] = 1
        return result

from bill import finish_order
@app.post("/api/finish_order")
def finish_order_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        if ('get_all' in data.keys()) == True:
            return finish_order(a_name=data['a_name'],api_name=data['api_name'],
                              symbol=data['symbol'],get_all=data['get_all'])
        else:
            return finish_order(a_name=data['a_name'], api_name=data['api_name'],
                                symbol=data['symbol'])
    else:
        result = {}
        result['status'] = 1
        return result

from cancel import cancel_order
@app.post("/api/cancel_order")
def cancel_order_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return cancel_order(a_name=data['a_name'],api_name=data['api_name'],
                              symbol=data['symbol'],orderid=data['orderid'])
    else:
        result = {}
        result['status'] = 1
        return result

from cancel import cancel_open_order
@app.post("/api/cancel_open_order")
def cancel_open_order_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return cancel_open_order(a_name=data['a_name'],api_name=data['api_name'],
                              symbol=data['symbol'])
    else:
        result = {}
        result['status'] = 1
        return result

from account import create_account,get_account_list,del_account,update_accout_pw
@app.post("/api/create_account")
def create_account_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return create_account(aname=data['a_name'],apw=data['password'])

    else:
        result = {}
        result['status'] = 1
        return result


@app.post("/api/del_account")
def del_account_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return del_account(aname=data['a_name'])

    else:
        result = {}
        result['status'] = 1
        return result


@app.post("/api/update_accout_pw")
def update_accout_pw_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return update_accout_pw(aname=data['a_name'], apw=data['password'])
    else:
        result = {}
        result['status'] = 1
        return result

@app.post("/api/get_account_list")
def get_account_list_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return get_account_list()
    else:
        result = {}
        result['status'] = 1
        return result


from account import get_api_account_list
@app.post("/api/get_api_account_list")
def get_api_list_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return get_api_account_list()
    else:
        result = {}
        result['status'] = 1
        return result

from api_database import create_api_account,del_api_account,update_api
@app.post("/api/create_api_account")
def create_api_account_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return create_api_account(aname=data['a_name'],api_name=data['api_name'],
                                  api_k=data['api_k'],api_s=data['api_s'])
    else:
        result = {}
        result['status'] = 1
        return result


@app.post("/api/del_api_account")
def del_api_account_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return del_api_account(api_name=data['api_name'])
    else:
        result = {}
        result['status'] = 1
        return result

@app.post("/api/update_api_account")
def update_api_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return update_api(aname=data['a_name'],api_name=data['api_name'],
                                  api_k=data['api_k'],api_s=data['api_s'])
    else:
        result = {}
        result['status'] = 1
        return result

from get_report_spot import get_spot_report
@app.post("/api/get_spot_report")
def get_spot_report_api(data: dict):
    a = verify_token(data['token'])
    if a == True:
        return get_spot_report(time=data['time'],api_name=data['api_name'])
    else:
        result = {}
        result['status'] = 1
        return result
from  limit_trade import while_check_oid
@app.post("/api/com_trade")
def com_trade_api(data: dict):
    while_check_oid(a_name=data['a_name'],api_name=data['api_name'],
                    coin_balance=data['coin_balance'],symbol=data['symbol'],
                    price=data['price'],stopPrice=data['stopPrice'],
                    oid=data['oid'])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="10.0.2.15",port=8000)

