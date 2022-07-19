import mysql.connector

from api_database import binance_connect
from database_info import binance_info

def get_coin_list():
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        get_meth = ("SELECT symbol FROM coin_list")
        c_cur.execute(get_meth)
        results = c_cur.fetchall()
        c_cur.close()
        c_data.close()
        list = []
        for (result,) in results:
            list.append(result)
        return list
    except mysql.connector.Error as err:
        return err
#print(get_coin_list())