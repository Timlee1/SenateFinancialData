import numpy as np
import pandas as pd


df = pd.read_csv('raw_data.csv')

df['Report Type'] = df['Report']


for ind in df.index:
    s = df['Report'][ind]
    if (s.find('paper') != -1) or (s.find('Amendment') != -1):
        df.drop(ind, inplace=True)

for ind in df.index:
    s = df['Report'][ind]
    start = s.find("=")
    end = s.find(">", start)
    sub = s[start+1:end]
    df['Report'][ind] = sub
    end_type = s.find("<", end)
    sub_type = s[end+1:end_type]
    df['Report Type'][ind] = sub_type


df['Date'] = pd.to_datetime(df['Date'])


df['Day'] = df['Date'].dt.day
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year
df = df.drop('Office', 1)
df = df.drop('Date', 1)
df['First'] = df['First'].str.upper()
df['Last'] = df['Last'].str.upper()
df.sort_values(["First", "Last", 'Year', 'Month', 'Day'],
               ascending=(True, True, True, True, True))

df.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/search_data.csv',
          index=False, header=True)
