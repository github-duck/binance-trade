from binance.spot import Spot as Client
import schedule
import mysql.connector



from api_database import binance_connect
from database_info import binance_info
from api_database import get_api_k_s


def input_file(context):
    import datetime
    today = datetime.datetime.now()
    with open("basic.log",'a') as file:
        file.write(str(today) +" "+ str(context)+"\n!")

def get_day(day):
    import datetime
    today_d = datetime.date.today()
    yesterday_d = today_d + datetime.timedelta(days=-1)
    time = "07:59:59"
    today = str(today_d) + " " +time
    yesterday = str(yesterday_d) + " " + time
    result_t = datetime.datetime.strptime(today,'%Y-%m-%d %H:%M:%S')
    result_y = datetime.datetime.strptime(yesterday, '%Y-%m-%d %H:%M:%S')
    if day == "y":
        return result_y
    if day == "t":
        return result_t

def unix_time(day):
    import time
    return int(time.mktime(day.timetuple()) * 1000.0 + day.microsecond / 1000.0)
#print(unix_time(get_day("t")))

def get_account_snapshot(a_name,api_name,startime,endtime):         #(a_name,api_name,startime=unix_time(get_day("y")),endtime=unix_time(get_day("t"))):
    get_ks = get_api_k_s(a_name,api_name)
    con = Client(get_ks["k"],get_ks["s"])
    respone = con.account_snapshot("SPOT",startTime=startime,endTime=endtime)['snapshotVos']
    total_data = []
    y_index = 0
    y_list = []
    y_dict = {}

    if len(respone) > 1:
        while y_index < len(respone[1]['data']['balances']):
            y_data = {}
            y_data['coin'] = respone[1]['data']['balances'][y_index]['asset']
            y_data['free'] = float(respone[1]['data']['balances'][y_index]['free']) + float(respone[0]['data']['balances'][y_index]['locked'])
            y_list.append(y_data)
            y_index = y_index + 1
            continue
        y_dict['y_balance'] = y_list
        total_data.append(y_dict)

    t_index = 0
    t_list = []
    t_dict = {}
    if len(respone) > 1:
        while t_index < len(respone[0]['data']['balances']):
            t_data = {}
            t_data['coin'] = respone[0]['data']['balances'][t_index]['asset']
            t_data['free'] = float(respone[0]['data']['balances'][t_index]['free']) + float(respone[0]['data']['balances'][t_index]['locked'])
            t_list.append(t_data)
            t_index = t_index + 1
            continue
        t_dict['t_balance'] = t_list
        total_data.append(t_dict)
    if bool(total_data) == True:
        return total_data
    else:
        return False
#print(get_account_snapshot("test",'trade1',startime="1656547199000",endtime="1656633599000"))

def insert_balance(api_name,symbol,y_balance=None,t_balance=None,transfer_out=None,transfer_in=None,recharge=None,withdraw=None):
    import datetime
    today = datetime.date.today()
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        sum_index,sum,sum1 = 0.0,0.0,0.0
        if float(transfer_in) > sum_index and float(transfer_out) == sum_index:
            sum = float(y_balance) + float(transfer_in)
        if float(transfer_in) > sum_index and float(transfer_out) < float(transfer_in):
            sum = float(transfer_in) - float(transfer_out) + float(y_balance)
        if float(transfer_in) > sum_index and float(transfer_out) > float(transfer_in):
            sum = float(y_balance) - float(transfer_in)
        if float(transfer_out) > sum_index  and float(transfer_in) == sum_index:
            sum = float(y_balance)
        if float(transfer_out) ==  sum_index  and float(transfer_in) == sum_index:
            sum = float(y_balance)

        if float(recharge) > sum_index and float(withdraw) == sum_index:
            sum1 = float(recharge)
        if float(recharge) > sum_index and float(withdraw) < float(recharge):
            sum1 = float(recharge) - float(withdraw)
        if float(recharge) > sum_index and float(withdraw) > float(recharge):
            sum1 = float(transfer_in)
        if float(withdraw) > sum_index  and float(recharge) == sum_index:
            sum1 = sum_index
        if float(withdraw) ==  sum_index  and float(recharge) == sum_index:
            sum1 = sum_index
        a = float(sum) + float(sum1)
        b = float(t_balance) - a
        if a > 0:
            c =  b / a
            profit = ("%.2f"%c)
        else:
            profit = 0.0
        add_balance_meth = (
            "INSERT INTO spot_report "
            "(report_time,api_name,symbol,y_balance,t_balance,transfer_out,transfer_in,recharge,withdraw,profit) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        add_balance_data = (today,api_name,symbol,y_balance,t_balance,transfer_out,transfer_in,recharge,withdraw,profit)
        c_cur.execute(add_balance_meth,add_balance_data)
        c_data.commit()
        c_cur.close()
        c_data.close()
    except mysql.connector.Error as err:
        return err
#print(insert_balance('trade1','TRX',100,"10",0.0,0.0,0.0,0.0))

def get_transfer_in(a_name,api_name,symbol,starttime,endtime):
    get_ks = get_api_k_s(a_name,api_name)
    con = Client(get_ks["k"],get_ks["s"])
    UMFUTURE_MAIN = con.user_universal_transfer_history(type="UMFUTURE_MAIN",startTime=starttime,endTime=endtime)
    index = 0
    UMFUTURE_MAIN_sum = 0
    if UMFUTURE_MAIN['total'] > 0:
        while index < len(UMFUTURE_MAIN['rows']):
            if UMFUTURE_MAIN['rows'][index]['asset'] == symbol:
                UMFUTURE_MAIN_sum = UMFUTURE_MAIN['rows'][index]['amount']
                index = index + 1
                continue
            else:
                index = index + 1
                continue
    CMFUTURE_MAIN = con.user_universal_transfer_history(type="CMFUTURE_MAIN", startTime=starttime, endTime=endtime)
    CMFUTURE_MAIN_sum = 0
    index1 = 0
    if CMFUTURE_MAIN['total'] > 0:
        while index1 < len(CMFUTURE_MAIN['rows']):
            if CMFUTURE_MAIN['rows'][index1]['asset'] == symbol:
                CMFUTURE_MAIN_sum = CMFUTURE_MAIN['rows'][index1]['amount']
                index1 = index1 + 1
                continue
            else:
                index1 = index1 + 1
                continue
    MARGIN_MAIN = con.user_universal_transfer_history(type="MARGIN_MAIN", startTime=starttime, endTime=endtime)
    MARGIN_MAIN_sum = 0
    index2 = 0
    if MARGIN_MAIN['total'] > 0:
        while index2 < len(MARGIN_MAIN['rows']):
            if MARGIN_MAIN['rows'][index2]['asset'] == symbol:
                MARGIN_MAIN_sum = MARGIN_MAIN['rows'][index2]['amount']
                index2 = index2 + 1
                continue
            else:
                index2 = index2 + 1
                continue
    FUNDING_MAIN = con.user_universal_transfer_history(type="FUNDING_MAIN", startTime=starttime, endTime=endtime)
    FUNDING_MAIN_sum = 0
    index3 = 0
    if FUNDING_MAIN['total'] > 0:
        while index3 < len(FUNDING_MAIN['rows']):
            if FUNDING_MAIN['rows'][index3]['asset'] == symbol:
                FUNDING_MAIN_sum = FUNDING_MAIN['rows'][index3]['amount']
                index3 = index3 + 1
                continue
            else:
                index3 = index3 + 1
                continue
    in_sum = float(UMFUTURE_MAIN_sum) + float(CMFUTURE_MAIN_sum) + float(MARGIN_MAIN_sum) + float(FUNDING_MAIN_sum)
    return in_sum
#print(get_transfer_in('test','trade1','TRX','1657081150000','1657181150000'))

def get_transfer_out(a_name,api_name,symbol,starttime,endtime):
    get_ks = get_api_k_s(a_name,api_name)
    con = Client(get_ks["k"],get_ks["s"])
    MAIN_UMFUTURE = con.user_universal_transfer_history(type="MAIN_UMFUTURE",startTime=starttime,endTime=endtime)
    index = 0
    MAIN_UMFUTURE_sum = 0
    if MAIN_UMFUTURE['total'] > 0:
        while index < len(MAIN_UMFUTURE['rows']):
            if MAIN_UMFUTURE['rows'][index]['asset'] == symbol:
                MAIN_UMFUTURE_sum = MAIN_UMFUTURE['rows'][index]['amount']
                index = index + 1
                continue
            else:
                index = index + 1
                continue
    MAIN_CMFUTURE = con.user_universal_transfer_history(type="MAIN_CMFUTURE", startTime=starttime, endTime=endtime)
    MAIN_CMFUTURE_sum = 0
    index1 = 0
    if MAIN_CMFUTURE['total'] > 0:
        while index1 < len(MAIN_CMFUTURE['rows']):
            if MAIN_CMFUTURE['rows'][index1]['asset'] == symbol:
                MAIN_CMFUTURE_sum = MAIN_CMFUTURE['rows'][index1]['amount']
                index1 = index1 + 1
                continue
            else:
                index1 = index1 + 1
                continue
    MAIN_MARGIN = con.user_universal_transfer_history(type="MAIN_MARGIN", startTime=starttime, endTime=endtime)
    MAIN_MARGIN_sum = 0
    index2 = 0
    if MAIN_MARGIN['total'] > 0:
        while index2 < len(MAIN_MARGIN['rows']):
            if MAIN_MARGIN['rows'][index2]['asset'] == symbol:
                MAIN_MARGIN_sum = MAIN_MARGIN['rows'][index2]['amount']
                index2 = index2 + 1
                continue
            else:
                index2 = index2 + 1
                continue
    MAIN_FUNDING = con.user_universal_transfer_history(type="MAIN_FUNDING", startTime=starttime, endTime=endtime)
    MAIN_FUNDING_sum = 0
    index3 = 0
    if MAIN_FUNDING['total'] > 0:
        while index3 < len(MAIN_FUNDING['rows']):
            if MAIN_FUNDING['rows'][index3]['asset'] == symbol:
                MAIN_FUNDING_sum = MAIN_FUNDING['rows'][index3]['amount']
                index3 = index3 + 1
                continue
            else:
                index3 = index3 + 1
                continue
    out_sum = float(MAIN_UMFUTURE_sum) + float(MAIN_CMFUTURE_sum) + float(MAIN_MARGIN_sum) + float(MAIN_FUNDING_sum)
    return out_sum
#print(get_transfer_out('test','trade1','TRX','1657081150000','1657181150000'))

def get_deposit(a_name,api_name,symbol,starttime,endtime):
    get_ks = get_api_k_s(a_name,api_name)
    con = Client(get_ks["k"],get_ks["s"])
    deposit_respone = con.deposit_history(coin=symbol, startTime=starttime, endTime=endtime)
    index = 0
    deposit_sum = 0
    if deposit_respone == True:
        while index < len(deposit_respone):
            if deposit_respone[index]['status'] == 1:
                if deposit_respone[index]['coin'] == symbol:
                    deposit_sum = float(deposit_sum) +  float(deposit_respone[index]['amount'])
                    index = index + 1
                else:
                    index = index + 1
            else:
                index = index + 1
    return deposit_sum
#print(get_deposit('test','trade1','TRX','1654788106000','1656086126000'))

def get_withdraw(a_name,api_name,symbol,starttime,endtime):
    get_ks = get_api_k_s(a_name,api_name)
    con = Client(get_ks["k"],get_ks["s"])
    withdraw_respone = con.withdraw_history(coin=symbol, startTime=starttime, endTime=endtime)
    index = 0
    withdraw_sum = 0
    if withdraw_respone == True:
        while index < len(withdraw_respone):
            if withdraw_respone[index]['status'] == 6:
                if withdraw_respone[index]['coin'] == symbol:
                    withdraw_sum = float(withdraw_sum) +  float(withdraw_respone[index]['amount'])
                    index = index + 1
                else:
                    index = index + 1
            else:
                index = index + 1
    return withdraw_sum
#print(get_withdraw('test','trade1','TRX','1654788106000','1656086126000'))

def insert_balance_meth(aname,api_name,startime,endtime):
    a = get_account_snapshot(aname,api_name,startime=startime,endtime=endtime)
    if bool(a) == True:
        index = 0
        while index < len(a[0]['y_balance']):
            coin = a[0]['y_balance'][index]['coin']
            index1 = 0
            while index1 < len(a[0]['y_balance']):
                if a[0]['y_balance'][index1]['coin'] == coin:
                    y_free = a[0]['y_balance'][index1]['free']
                    index2 = 0
                    while index2 < len(a[1]['t_balance']):
                        if a[1]['t_balance'][index2]['coin'] == coin:
                            t_free = a[1]['t_balance'][index2]['free']
                            transfer_out = get_transfer_out(aname,api_name,coin,startime,endtime)
                            transfer_in = get_transfer_in(aname,api_name,coin,startime,endtime)
                            recharge = get_deposit(aname,api_name,coin,startime,endtime)
                            withdraw = get_withdraw(aname,api_name,coin,startime,endtime)
                            insert_balance(api_name,coin,y_free,t_free,transfer_out,transfer_in,recharge,withdraw)
                            index = index + 1
                            break
                        else:
                            index2 = index2 + 1
                            continue
                    break
                else:
                    index1 = index1 + 1
                    continue
    else:
        input_file("account balance is Flase")
        return False

def report_run():
    try:
        c_data = binance_connect(binance_info)
        c_cur = c_data.cursor()
        get_name = ("SELECT DISTINCT account_name FROM api_info ")
        c_cur.execute(get_name)
        a_results = c_cur.fetchall()
        a_list = []
        a_index = 0
        for (result,) in a_results:
            a_list.append(result)
            api_list = []
            while a_index < len(a_list):
                get_a_name = ("SELECT account_name,api_name FROM api_info "
                              "WHERE account_name = %s")
                c_cur.execute(get_a_name,(a_list[a_index],))
                api_results = c_cur.fetchall()
                for (aname,api_result,)in api_results:
                    #api_list.append(api_result)
                    insert_balance_meth(aname,api_result,startime=unix_time(get_day("y")),endtime=unix_time(get_day("t")))
                a_index = a_index + 1
        c_cur.close()
        c_data.close()
    except mysql.connector.Error as err:
        return err

schedule.every().day.at("08:30").do(report_run)
import time
while True:
    schedule.run_pending()



#print(insert_balance_meth("test",'trade1',startime="1656892799000",endtime="1656979199000"))
#print(insert_balance_meth("test",'trade1',startime=unix_time(get_day("y")),endtime=unix_time(get_day("t"))))
#print(insert_balance('trade1','TRX',100,"10",0.0,0.0,0.0,0.0))
#def insert_balance(api_name,symbol,y_balance=None,t_balance=None,transfer_out=None,transfer_in=None,recharge=None,withdraw=None):
#get_transfer_out(a_name,api_name,symbol,starttime,endtime):
#get_deposit(a_name,api_name,symbol,starttime,endtime):
#startime=unix_time(get_day("y")),endtime=unix_time(get_day("t")