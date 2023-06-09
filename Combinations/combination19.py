#  bullish --> Hammer
#  bearish --> marubuzu



import talib
import numpy as np
import pandas as pd

# file directory
dataLarge = pd.read_csv('/Users/khushnarang/Desktop/try/nifty_5minute_data.csv')
data = dataLarge

# Convert the data to numpy arrays
open_price = np.array(data['open'])
high_price = np.array(data['high'])
low_price = np.array(data['low'])
close_price = np.array(data['close'])

hammer_pattern = talib.CDLHAMMER(open_price, high_price, low_price, close_price)

marubuzu_pattern = talib.CDLMARUBOZU(open_price, high_price, low_price, close_price)


hammer_count = len([x for x in hammer_pattern if x == 100])
bearish_marubuzu_pattern = len([x for x in marubuzu_pattern  if x == -100])



my_array = np.zeros(len(data['close']))

index = 0
for x in hammer_pattern:
    if x == 100:
        my_array[index] += 1
    index += 1

index = 0
for x in marubuzu_pattern:
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
    if my_array[i] == 1 and signal == 0:
        signal = 1
        dummy_investment -= data['open'][i]
        recent_buy = data['open'][i]
    elif my_array[i] == -1 and signal == 1:
        signal = 0
        dummy_investment += data['open'][i]

if signal == 1:
    dummy_investment += recent_buy

outcomeWithoutPattern = initial_investment + (data['close'][len(data['close']) - 1] - data['open'][0]) * (initial_investment) / data['open'][0]
outcomeWithPattern = initial_investment + (dummy_investment * initial_investment / data['open'][0])


print("Number of Hammer Patterns:", hammer_count)
print("Number of bearish_marubuzu Patterns:", bearish_marubuzu_pattern)
print("\nCurrent Investment Value by using pattern: $", outcomeWithPattern)
print("\nCurrent Investment Value without using pattern: $", outcomeWithoutPattern)



