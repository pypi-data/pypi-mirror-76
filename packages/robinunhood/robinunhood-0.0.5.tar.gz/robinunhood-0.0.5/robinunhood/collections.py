import pandas as pd
import requests
import json
import re

def get_top_movers():
    """
    :return: pandas dataframe of top 20 stocks that are the top movers
    """

    url = 'https://api.robinhood.com/midlands/tags/tag/top-movers/'
    x = requests.get(url)
    y = json.loads(x.text)
    z = y['instruments']

    df = pd.DataFrame()
    for i in range(len(z)):
        d = requests.get(z[i])
        f = json.loads(d.text)
        df_tmp = pd.DataFrame.from_dict(f, orient='index').T
        df = df.append(df_tmp)

    return df


def get_most_popular():
    """
    :return: pandas dataframe of 100 most-popular
    """
    [df] = pd.read_html('https://robinhood.com/collections/100-most-popular')
    return df


def get_collection(collection):
    """
    :param collection: "100-most-popular", "upcoming-earnings", "new-on-robinhood", "technology", "oil-and-gas",
    "finance", "software-service", "energy", "manufacturing", "consumer-products", "etf", "video-games", "social-media",
    "health", "entertainment"
    :return: pandas dataframe of collection stocks
    """
    url = f'https://robinhood.com/collections/{collection}'
    [df] = pd.read_html(url)
    return df


if __name__ == "__main__":

    #df = get_top_movers()
    #print(df.symbol.values)

    #df = get_most_popular()
    #print(df.Symbol.values)

    df = get_collection('etf')
    print(df.Symbol.values)