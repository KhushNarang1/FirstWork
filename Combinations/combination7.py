#  bullish --> harami + Engulfing
#  bearish --> harami + Engulfing



import talib
import numpy as np
import pandas as pd

# file directory
dataAll = pd.read_csv('/Users/khushnarang/Desktop/try/nifty_5minute_data.csv')
dataAll['date'] = pd.to_datetime(dataAll['date'])

bullish_engulfing_pattern = 0
bearish_engulfing_pattern = 0
bullish_harami_pattern = 0
bearish_harami_pattern = 0


for j in range(0, 54):
    unique_dates = dataAll['date'].dt.date.unique()
    second_data = unique_dates[j]
    data = dataAll[dataAll['date'].dt.date == second_data]


    # Convert the data to numpy arrays
    open_price = np.array(data['open'])
    high_price = np.array(data['high'])
    low_price = np.array(data['low'])
    close_price = np.array(data['close'])


    engulfing_pattern = talib.CDLENGULFING(open_price, high_price, low_price, close_price)

    harami_pattern = talib.CDLHARAMI(open_price, high_price, low_price, close_price)

    bullish_engulfing_pattern += len([x for x in engulfing_pattern if x == 100])
    bearish_engulfing_pattern += len([x for x in engulfing_pattern if x == -100])
    bullish_harami_pattern += len([x for x in harami_pattern  if x == 100])
    bearish_harami_pattern += len([x for x in harami_pattern  if x == -100])



    my_array = np.zeros(len(data['close']))

    index = 0
    for x in engulfing_pattern:
        if x == 100:
            my_array[index] += 1
        elif x == -100:
            my_array[index] -= 1
        index += 1

    index = 0
    for x in harami_pattern:
        if x == 100:
            my_array[index] += 1
        elif x == -100:
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


    print("Current Investment Value by using pattern: $", outcomeWithPattern)
    # print("\nCurrent Investment Value without using pattern: $", outcomeWithoutPattern)

print("Number of bullish_engulfing Patterns:", bullish_engulfing_pattern)
print("Number of bearish_engulfing Patterns:", bearish_engulfing_pattern)
print("Number of bullish_harami Patterns:", bullish_harami_pattern)
print("Number of bearish_harami Patterns:", bearish_harami_pattern)

