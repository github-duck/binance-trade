from binance.spot import Spot as Client
import hashlib
import os
import time

from api_database import get_api_k_s
from database_info import binance_info
from mysql.connector import errorcode
import mysql.connector


tokens = {}

from api_database import binance_connect

def account_status(a_name,api_name):
    result = get_api_k_s(a_name,api_name)
    status = Client(result["k"],result["s"])
    result_status = status.api_trading_status()
    if result_status["data"]["isLocked"] == False:
        return True
    else:
        return False
#print(account_status("test","trade1"))   ##传账户名和api名进去，测试账户api正常，1分钟测试一次

def generate_token():
    sha1_token = hashlib.sha1(os.urandom(24)).hexdigest()
    s_time = int(time.time())
    save_time = s_time + 34168
    tokens[sha1_token] = save_time
    #data = {}
    #data['message'] = sha1_token
    return sha1_token

def verify_login(a_name,password):
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        ver_name = ("SELECT account_name,account_pw FROM account_info "
                    "WHERE account_name = %s")
        c_cur.execute(ver_name,(a_name,))
        ver_result = c_cur.fetchall()
        if bool(ver_result)  == True:
            list = []
            for (name,pw,) in ver_result:
                if name == a_name and pw == password:
                    dict = {}
                    dict['token'] = generate_token()
                    dict['username'] = a_name
                    return dict
                else:
                    return ("password error")
        else:
            return ("User not found")
        c_cur.close()
        c_data.close()
    except mysql.connector.Error as err:
        return ("database error")
#print(verify_login('adolph','asd1231'))
#print(tokens)
#a = {'test':"fdsfsdfds",'test2':'1657332964'}
#print('test22' in a.keys())
def verify_token(token):
    if (token in tokens.keys()) == True:
        now = int(time.time())
        if int(tokens[token]) > now:
            return True
        else:
            return False
    else:
        return False
#print(verify_token('test2'))