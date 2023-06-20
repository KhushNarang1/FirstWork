#  bullish --> piercing + Hammer
#  bearish --> Engulfing + Hanging Man



import talib
import numpy as np
import pandas as pd

# file directory
tradeArray1 = np.array([])
tradeArray2 = np.array([])
tradeArray3 = np.array([])
newData = pd.read_csv('/Users/khushnarang/PycharmProjects/FirstWork/DataRecived/Combination9.csv')
dataAll = pd.read_csv('/Users/khushnarang/Desktop/try/nifty_5minute_data.csv')
dataAll['date'] = pd.to_datetime(dataAll['date'])

hammer_count = 0
hanging_man_count = 0
bullish_piercing_count = 0
bearish_engulfing_pattern = 0

for j in range(0, 54):

    unique_dates = dataAll['date'].dt.date.unique()
    second_data = unique_dates[j]
    data = dataAll[dataAll['date'].dt.date == second_data]
    # Convert the data to numpy arrays
    open_price = np.array(data['open'])
    high_price = np.array(data['high'])
    low_price = np.array(data['low'])
    close_price = np.array(data['close'])

    hammer_pattern = talib.CDLHAMMER(open_price, high_price, low_price, close_price)

    hanging_man_pattern = talib.CDLHANGINGMAN(open_price, high_price, low_price, close_price)

    engulfing_pattern = talib.CDLENGULFING(open_price, high_price, low_price, close_price)

    bullish_piercing_pattern = talib.CDLPIERCING(open_price, high_price, low_price, close_price)


    hammer_count += len([x for x in hammer_pattern if x == 100])
    hanging_man_count += len([x for x in hanging_man_pattern if x == -100])
    bullish_piercing_count += len([x for x in bullish_piercing_pattern  if x == 100])
    bearish_engulfing_pattern += len([x for x in engulfing_pattern  if x == -100])



    my_array = np.zeros(len(data['close']))

    index = 0
    for x in hammer_pattern:
        if x == 100:
            my_array[index] += 1
        index += 1

    index = 0
    for x in bullish_piercing_pattern:
        if x == 100:
            my_array[index] += 1
        index += 1

    index = 0
    for x in hanging_man_pattern:
        if x == -100:
            my_array[index] -= 1
        index += 1

    index = 0
    for x in engulfing_pattern:
        if x == -100:
            my_array[index] -= 1
        index += 1

    # for x in my_array:
    #     if x == 2:
    #         print(x)
    #     elif x == -2:
    #         print(x)


    initial_investment = 100
    dummy_investment = 0
    signal = 0  # will tell about buy time and sell time

    recent_buy = 0
    for i in range(0, len(my_array)):
        if my_array[i] == 2 and signal == 0:
            signal = 1
            dummy_investment -= data['open'][i + (75 * j)]
            recent_buy = data['open'][i + (75 * j)]
        elif my_array[i] == -2 and signal == 1:
            signal = 0
            dummy_investment += data['open'][i + (75 * j)]

    if signal == 1:
        dummy_investment += recent_buy
    outcomeWithoutPattern = initial_investment + (data['close'][75 * j + 74] - data['open'][75 * j]) * (initial_investment) / data['open'][75 * j]
    outcomeWithPattern = initial_investment + (dummy_investment * initial_investment / data['open'][75 * (j)])

    tradeArray1 = np.append(tradeArray1, outcomeWithPattern)
    tradeArray2 = np.append(tradeArray2, outcomeWithoutPattern)
    tradeArray3 = np.append(tradeArray3, initial_investment)
    # print("DAY:- ", second_data, end="  ||  ")
    # print("Current Investment Value by using pattern: $", outcomeWithPattern)
    # print("\nCurrent Investment Value without using pattern: $", outcomeWithoutPattern)

newData['InitialInvestment'] = tradeArray3
newData['InvestmentUsingPattern'] = tradeArray1
newData['InvestmentWithoutPattern'] = tradeArray2
newData.to_csv('/Users/khushnarang/PycharmProjects/FirstWork/DataRecived/Combination9.csv', index=False)

