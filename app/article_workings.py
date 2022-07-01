from nltk.tokenize import word_tokenize
import re
from newspaper import Config, Article
from nltk.corpus import stopwords


def remove_stopwords_punctuation(text):

    """Function to clean the corpus for future classification"""

    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)

    filtered_text = [t for t in tokens if not t in stopwords.words("english")]
    filtered_text = " ".join(filtered_text)

    return filtered_text


def extractor(link):

    """ Using an user agent, uses newspaper3k library
    to download some articles attributes """

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

    config = Config()
    config.browser_user_agent = user_agent
    article = Article(link, config=config)

    try:

        article.download()
        article.parse()
        article.nlp()

        summary = article.summary
        content = article.text
        image = article.top_image

        return summary, content, image

    except Exception as e:

        print(e)

        return None, None, None


def get_articles_content(df):
    """Assign the content from extractor to the originalpandas dataframe,
    returns the full article content linked to the dataframe"""

    df[['summary', "content", "image"]] = df.apply(lambda x: extractor(x['url']), axis=1, result_type='expand')

    return df


def clean(df, weakly, search):

    """Link parts of the corpus together to future
    post processing
    1: Clean articles that don't mention the keyword 100%
    2: Prepare column for translation+classification
    """

    df.fillna(' ', inplace=True)
    df['corpus_summary'] = df[["title", "summary"]].agg(' '.join, axis=1)
    df['corpus_summary'] = df['corpus_summary'].apply(lambda x: remove_stopwords_punctuation(x))

    df['corpus_full'] = df[["title", "summary", "content"]].agg(' '.join, axis=1)
    df['corpus_full'] = df['corpus_full'].str.lower()
    df['corpus_full'] = df['corpus_full'].apply(lambda x: remove_stopwords_punctuation(x))

    keyword_lower = search.lower()

    if weakly is False:
        df = df[df.corpus_full.str.contains(keyword_lower)]
    else:
        pass

    return df
