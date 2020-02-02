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
    for i in range(0, data_size):
        rs = 0
        move = (access_close(data[i]) - access_close(data[i-1]))
        if(period < i+1):
            avg_down = (avg_down*(period-1) - move*(move < 0))/period

            avg_up = (avg_up*(period-1) + move * (move >= 0))/period

            rs = avg_up / avg_down
            rsi = 100-100/(1+rs)
            rsi_data.append(rsi)
        else:
            if(move < 0):
                avg_down -= move
            else:
                avg_up += move

    return rsi_data 

def test_strat(data, buy_condition, sell_condition, start_capital, commission, buy_options, sell_options):
    shares = 0
    cap = start_capital
    for i, v in enumerate(data):
        if buy_options['rsi_period'] < i:
            buy_amount, buy_price = buy_condition(data, cap, i-buy_options['rsi_period'], buy_options) 
            #print(buy_amount, buy_price, i-buy_options['rsi_period'])
            shares += buy_amount
            cap -= buy_price*buy_amount-commission
            if(buy_amount != 0 and buy_price != 0):
                print("buying", buy_amount, buy_price, shares, cap)
            
            #sell_amount, sell_price = sell_condition(data, shares, i, sell_options)
            #shares -= sell_amount
            #cap += buy_price*buy_amount-commission
        #print(shares, cap)

with open('obj/data.pickle', 'rb') as data:
    unserialized = pickle.load(data)

def access_open(data):
    return data['open']

def access_close(data):
    return data['close']


def buy(data, cap, i, buy_options={}):
    #print("i:", i)
    if rsi[i] < 25 and rsi[i-1] < 25 and rsi [i-2] < 25:
        return int(cap*0.1/data[i]['close']), data[i]['close']
    else:
        return 0, 0


rsi = calculate_rsi(unserialized['candles'], access_open, access_close, 14)

print(len(rsi), len(unserialized['candles']))

buy_options = {'rsi': rsi, 'rsi_period': 14}
sell_options = {'rsi': rsi, 'rsi_period': 14}

#def test_strat(data, buy_condition, sell_condition, start_capital, commission, buy_options, sell_options):
test_strat(unserialized['candles'], buy, buy, 5000, 5, buy_options, sell_options)

#print(buy(unserialized['candles'], 5000, 1, buy_options))
