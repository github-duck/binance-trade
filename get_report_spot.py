import mysql.connector

from api_database import binance_connect
from database_info import binance_info

def get_spot_report(time,api_name):
    try:
        big_list = []
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        get_data = ("SELECT report_time,api_name,symbol,y_balance,t_balance,transfer_out,transfer_in,recharge,withdraw,profit FROM spot_report "
                    "WHERE report_time = %s and api_name = %s")
        c_cur.execute(get_data,(time,api_name))
        get_results = c_cur.fetchall()
        for (a,s,d,f,g,h,j,k,l,z,) in get_results:
            list = []
            list.append(a)
            list.append(s)
            list.append(d)
            list.append(f)
            list.append(g)
            list.append(h)
            list.append(j)
            list.append(k)
            list.append(l)
            list.append(z)
            big_list.append(list)
        c_cur.close()
        c_data.close()
        return big_list
    except mysql.connector.Error as err:
        return err
#print(get_spot_report('2022-7-8',"trade1"))