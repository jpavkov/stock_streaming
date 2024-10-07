import pandas as pd


def transform_data(raw_data):
    # turn raw_data into data.table
    # print(raw_data)

    # convert JSON to data frame
    df_stocks = pd.DataFrame(raw_data['results'])

    # add additional columns
    df_stocks['ticker'] = raw_data['ticker']
    df_stocks['queryCount'] = raw_data['queryCount']
    df_stocks['resultsCount'] = raw_data['resultsCount']
    df_stocks['adjusted'] = raw_data['adjusted']

    # rearrange columns
    df_stocks = df_stocks[['ticker', 'queryCount', 'resultsCount',
                           'adjusted', 'v', 'vw', 'o', 'c', 'h', 'l', 't', 'n']]

    df_stocks.rename(columns={'v': 'volume', 'vw': 'weightedAverage',
                              'o': 'openPrice', 'c': 'closePrice', 'h': 'highPrice', 'l': 'lowPrice',
                              't': 'timeUnixMsec', 'n': 'transactionCount'},
                     inplace=True)

    # print(df_stocks)

    # add date and time column
    df_stocks['dateTime'] = pd.to_datetime(
        df_stocks['timeUnixMsec'], unit='ms')
    df_stocks['date'] = df_stocks['dateTime'].dt.date
    df_stocks['time'] = df_stocks['dateTime'].dt.time

    # print(df_stocks)

    return df_stocks
