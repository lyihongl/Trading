from questrade_api import Questrade
from collections import deque
import pickle

q = Questrade()

# q: quest trade instance
# symbol: ticker symbol
# interval: string, see questrade api
# startDate: string, see questrade api
# endDate: ditto startDate
def collect_candles(q, symbol, interval, startDate, endDate): 
    intraDayHours = "00:00:00-05:00"
    symbolId = q.symbols(names=symbol)['symbols'][0]['symbolId']
    startTime = startDate+"T"+intraDayHours
    endTime = endDate+"T"+intraDayHours
    candles = q.markets_candles(symbolId, interval=interval, startTime=startTime, endTime=endTime)
    print("collect candles: success")
    return candles

# pass function handle access_open, access_close to access open and close price from your data
def calculate_rsi(data, access_open, access_close, period):
    rsi_data = []
    data_size = len(data)
    avg_up = 0
    avg_down = 0
    for i in range(1, data_size):
        rs = 0
        move = (access_close(data[i]) - access_close(data[i-1]))
        if(period < i-1):
            avg_down = (avg_down*(period-1) - move*(move < 0))/period

            avg_up = (avg_up*(period-1) + move * (move >= 0))/period

            rs = avg_up / avg_down
            rsi = 100-100/(1+rs)
            rsi_data.append(rsi)
            #if(abs(rsi-50) > 20):
                #print("rs", rs, "rsi", rsi, data[i]['start'], data[i]['open'], data[i]['close'])
        else:
            if(move < 0):
                avg_down -= move
            else:
                avg_up += move

    return rsi_data 

def test_strat(buy_condition, sell_condition, start_capital, commission, buy_options, sell_options):
   pass 

with open('obj/data.pickle', 'rb') as data:
    unserialized = pickle.load(data)

def access_open(data):
    return data['open']

def access_close(data):
    return data['close']

a = calculate_rsi(unserialized['candles'], access_open, access_close, 14)
print(a)
