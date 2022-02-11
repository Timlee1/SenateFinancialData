import numpy as np
import pandas as pd


def strip_td(s):
    start = s.find(">")
    end = s.find("<", start)
    return s[start+1:end]


def strip_ahref(s):
    start = s.find("=")
    end = s.find("<", start)
    return s[start+1:end]


def data_clean(csv):
    df = pd.read_csv(csv)

    for ind in df.index:
        df['First'][ind] = strip_td(df['First'][ind]).upper()
        df['Last'][ind] = strip_td(df['Last'][ind]).upper()
        df['Office'][ind] = strip_td(df['Office'][ind])
        df['Date'][ind] = strip_td(df['Date'][ind])

    df['Report Type'] = df['Report']
    df['Report Year'] = df['Report']

    for ind in df.index:
        s = df['Report'][ind]
        if (s.find('paper') != -1) or (s.find('Amendment') != -1) or (s.find('Extension') != -1) or (s.find('Blind Trust') != -1):
            df.drop(ind, inplace=True)

    for ind in df.index:
        s = df['Report'][ind]
        start = s.find("search") - 1
        end = s.find("target", start) - 2
        sub = s[start:end]
        df['Report'][ind] = sub

        end_type = s.find("<", end)
        sub_type = s[end+1:end_type]
        df['Report Type'][ind] = sub_type
        indf = sub_type.find('for')
        end = indf-1
        df['Report Type'][ind] = sub_type[0:end]
        extra = df['Report Type'][ind].find(">")
        df['Report Type'][ind] = df['Report Type'][ind][extra+1:]
        if sub_type[end+5:].find('CY') != -1:
            df['Report Year'][ind] = sub_type[end+7:]
        else:
            df['Report Year'][ind] = sub_type[end+11:]

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


data_clean('raw_data.csv')
