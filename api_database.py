import mysql.connector
from mysql.connector import errorcode


from database_info import binance_info
from basic_logic import *




def binance_connect(database_data):
    try:
        binance_connect = mysql.connector.connect(**database_data)
        return binance_connect
    except mysql.connector.errors as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return ("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return ("Database does not exist")
        else:
            return (err)
    else:
        binance_connect.close()
def create_api_account(aname,api_name,api_k,api_s): ##create
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        add_api_meth = (
            "INSERT INTO api_info "
            "(account_name,api_name,api_key,api_security,create_time) "
            "VALUES (%s,%s,%s,%s,%s)")
        add_api_data = (aname, api_name, api_k, api_s, time_now)
        c_cur.execute(add_api_meth, add_api_data)
        c_data.commit()
        c_cur.close()
        c_data.close()
    except mysql.connector.Error as err:
        return err
#print(create_api_account("test1","trade4","f3YCoNROKVHQGTJOk8vn01DiTO81INAXtryRYdhLjt4vVFVyTzMRfEach4pF0gUe","O79sIpJwGSkmR9ba2eMUg5hK19jlpSjMIrAHahslHx1jskfEJrCeohdbuU0tHY87"))
def get_api_k_s(aname,api_name):
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        get_k_s = ("SELECT api_key,api_security FROM api_info "
                    "WHERE account_name = %s and api_name = %s")
        c_cur.execute(get_k_s,(aname,api_name))
        result = c_cur.fetchone()
        c_cur.close()
        c_data.close()
        k_s = {}
        k_s["k"],k_s["s"] = result[0],result[1]
        return k_s
    except mysql.connector.Error as err:
        return err
#print(get_api_k_s("test","trade5"))

def del_api_account(api_name):
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        del_api = ("DELETE FROM api_info "
                   "WHERE api_name = %s")
        c_cur.execute(del_api,(api_name,))
        c_data.commit()
        c_cur.close()
        c_data.close()
        return ("deleted finish")
    except mysql.connector.Error as err:
        return err
#print(del_api_account("trade4"))

def update_api(api_name,aname,api_k,api_s):
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        update_meth = ("UPDATE api_info SET account_name = %s,"
                       "api_key = %s,api_security = %s "
                       "WHERE api_name = %s")
        update_data = (aname,api_k,api_s,api_name)
        c_cur.execute(update_meth,update_data)
        c_data.commit()
        c_cur.close()
        c_data.close()
    except mysql.connector.Error as err:
        return err
#print(update_api("trade4","test1","123","222"))


def get_apiname_list(aname):
    try:
        list = []
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        get_a_name = ("SELECT account_name,api_name FROM api_info "
                      "WHERE account_name = %s")
        c_cur.execute(get_a_name,(aname,))
        a_name = c_cur.fetchall()
        for (aname, api_result,) in a_name:
            list.append(api_result)
        return list
    except mysql.connector.Error as err:
        return err
#print(get_apiname_list('test'))

