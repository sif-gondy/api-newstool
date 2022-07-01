from gnews import GNews
import pandas as pd


def get_news_from_keyword(keyword, timeframe):

    """This function takes a keyword in argument and returns the
    output of news from the keyword according to the language from GoogleNews"""

    googlenews = GNews(period=timeframe, country=None, language=None)

    json_resp = googlenews.get_news(keyword)

    df = pd.json_normalize(json_resp)

    df.columns = df.columns.map(lambda x: x.split(".")[-1])
    df.columns = [*df.columns[:-1], 'publisher']

    df['keyword'] = keyword
    df['timeframe'] = timeframe


    df = df.drop("description", axis=1)

    return df


def get_news_from_keyword_language(keyword, language, timeframe):

    """This function takes a keyword in argument and returns the
    output of news from the keyword according to the language from GoogleNews"""

    googlenews = GNews(period=timeframe, language=language, country=None)

    json_resp = googlenews.get_news(keyword)

    df = pd.json_normalize(json_resp)

    df.columns = df.columns.map(lambda x: x.split(".")[-1])
    df.columns = [*df.columns[:-1], 'publisher']

    df['language'] = language
    df['keyword'] = keyword

    df = df.drop("description", axis=1)

    return df


def get_news_from_keyword_country(keyword, country, timeframe):

    """This function takes a keyword in argument and returns the
    output of news from the keyword according to the country from GoogleNews"""

    googlenews = GNews(period=timeframe, country=country, language=None)

    json_resp = googlenews.get_news(keyword)

    df = pd.json_normalize(json_resp)

    df.columns = df.columns.map(lambda x: x.split(".")[-1])
    df.columns = [*df.columns[:-1], 'publisher']

    df['country'] = country
    df['keyword'] = keyword

    df = df.drop("description", axis=1)

    return df
