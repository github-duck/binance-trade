import mysql.connector

from api_database import binance_connect
from basic_logic import *
from database_info import binance_info

def create_account(aname,apw):
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        add_account_meth = (
            "INSERT INTO account_info "
            "(account_name,account_pw,create_time) "
            "VALUES (%s,%s,%s)")
        add_account_data = (aname,apw,time_now)
        c_cur.execute(add_account_meth,add_account_data)
        c_data.commit()
        c_cur.close()
        c_data.close()
    except mysql.connector.Error as err:
        return err
#create_account("test2","testpw2")

def get_account_list():
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        get_meth = ("SELECT account_name FROM account_info ")

        c_cur.execute(get_meth)
        result = c_cur.fetchall()
        c_cur.close()
        c_data.close()
        return result
    except mysql.connector.Error as err:
        return err
#print(get_account_list())

def get_api_account_list():
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        get_meth = ("SELECT account_name,api_name FROM api_info ")

        c_cur.execute(get_meth)
        result = c_cur.fetchall()
        c_cur.close()
        c_data.close()
        return result
    except mysql.connector.Error as err:
        return err



def del_account(aname):
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        del_a = ("DELETE FROM account_info "
                   "WHERE account_name = %s")
        c_cur.execute(del_a,(aname,))
        c_data.commit()
        c_cur.close()
        c_data.close()
        return ("deleted finish")
    except mysql.connector.Error as err:
        return err
#print(del_account("test2"))

def update_accout_pw(aname,apw):
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        update_meth = ("UPDATE account_info SET account_pw = %s "
                     "WHERE account_name = %s")
        update_data = (apw,aname)
        c_cur.execute(update_meth,update_data)
        c_data.commit()
        c_cur.close()
        c_data.close()
    except mysql.connector.Error as err:
        return err
#print(update_accout_pw("test1","asd123"))