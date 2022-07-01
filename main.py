from app.translation import *
from app.news import *
from app.article_workings import *
from app.classification import *

"""Define functions to use in redis queue."""
from rq import get_current_job


def output_news(keywords: list, timeframe: str, translate_title: bool, translate_search: bool, **kwargs):

    """ This src function compiles previous methods to generate
    a dataframe of the news based on the keywords and languages provided,
    if no news are found, it returns an empty dataframe with the right column names

    Parameters ->
    keywords: the list of keywords to search on google news
    timeframe: a string denoting how far the articles can be retrieved (e.g. 7d, 5y, 1d)
    translate_title: Boolean for deciding whether the translation is performed on the title, should be true if labels provided
    translate_labels: Boolean for deciding whether the translation is performed on the labels, should be true if labels provided

    **kwargs ->
    labels: a list of labels enabling classification, should be given in english
    languages: a list of languages for filtering articles, cannot be used along with countries
    countries: a list of countries for filtering articles, cannot be used with languages
    weak: whether we want to perform a hard or loose match on the articles relative to the keyword, default is True
    rank: Boolean, permits the ranking and classification of articles based on the labels, Default is False
    ner: Whether to apply named entity recognition to full_corpus, default is False
    limit: to input a limit to get the first n results based on rank

    """

    input_d = locals()

    job = get_current_job()  ## Get the current job


    COLUMN_NAMES = ["title",
                    "published",
                    "date",
                    "url",
                    "href",
                    "publisher",
                    "language",
                    "keyword",
                    "summary",
                    "content",
                    "images"]

    dfs = []  # Initialize to say there will be multiple dfs for each language

    labels = kwargs.get('labels', None)
    languages = kwargs.get('languages', None)
    countries = kwargs.get('countries', None)
    limit = kwargs.get('limit', None)

    rank = kwargs.get('rank', False)
    ner = kwargs.get('ner', False)
    weak = kwargs.get('weak', True)

    for search in keywords:  #Invariable

        if languages is not None:

            for language in languages:

                if translate_search is True:
                    search = translate_fn(search, source="en", target=language)
                else:
                    pass

                print(language, ",", search)

                try:

                    df = get_news_from_keyword_language(keyword=search, language=language, timeframe=timeframe)

                except Exception as e:
                    print("ok")

                    print(e)

                    continue

                df = get_articles_content(df)

                df = clean(df, weakly=weak, search=search)

                print(len(df), " articles considered")

                if language != "en" and translate_title is True:

                    df = translate_df(df=df,
                                      column="title",
                                      source=language,
                                      target="en")
                else:

                    pass

                dfs.append(df)


        elif countries is not None:

            for country in countries:

                print(country, ",", search)

                try:

                    df = get_news_from_keyword_country(keyword=search, country=country, timeframe=timeframe)

                except Exception as e:

                    print(e)

                    continue

                df = get_articles_content(df)

                df = clean(df, weakly=weak, search=search)

                print(len(df), " articles considered")

                if translate_title is True:

                    df = translate_df(df=df,
                                      column="title",
                                      source="auto",
                                      target="en")
                else:

                    pass

                dfs.append(df)

        else:

            try:

                df = get_news_from_keyword(keyword=search, timeframe=timeframe)

            except Exception as e:

                print(e)

                continue

            df = get_articles_content(df)

            df = clean(df, weakly=weak, search=search)

            print(len(df), " articles considered")

            if translate_title is True:

                df = translate_df(df=df,
                                  column="title",
                                  source="auto",
                                  target="en")
            else:

                pass

            dfs.append(df)


    try:

        df_concat = pd.concat(dfs)

        df_concat.drop_duplicates(subset=['title'], inplace=True)

    except Exception as e:

        print(e)

        df_concat = pd.DataFrame(columns=COLUMN_NAMES)  # create empty dataframe



    if labels is not None and len(df_concat) > 0:  # Apply the classification

        try:

            classifier = load_classifier()

            df_concat = classifier_processing(df=df_concat,
                                              classifier=classifier,
                                              col_classify="title",
                                              labels=labels)

            try:

                if rank is True:

                    df_concat = df_concat.reset_index(drop=True)

                    mask = df_concat[labels]  # Loose... better way of isolating?

                    df_concat['median'] = mask.median(axis=1)

                    df_concat = df_concat.sort_values(by=['median'], ascending=False)

                    bins = ['low', 'medium', 'high', 'very high']

                    df_concat['class'] = pd.qcut(df_concat['median'], q=4, labels=bins)

                    if limit is not None:

                        if isinstance(limit, int):

                            df_concat = df_concat.head(limit)

                        else:

                            raise TypeError("Limit must be an integer")

                    else:

                        pass

                else:

                    pass

            except Exception as e:

                print("Something went wrong: " + str(e))


        except Exception as e:  # no object to concatenate = no news

            print(e)

            column_names = COLUMN_NAMES + labels

            df_concat = pd.DataFrame(columns=column_names)


    if ner is True and len(df_concat) > 0:

        ner = load_ner()


        df_concat = translate_df(df=df_concat,
                                 column="corpus_summary",
                                 source="auto",
                                 target="en")

        df_concat[['PER', "ORG", "LOC", "MISC"]] = df_concat.apply(lambda x: perform_ner(text=x['corpus_summary'], ner=ner), axis=1, result_type='expand')

    else:

        pass

    if len(df_concat) > 0:

        df_concat.drop(["corpus_summary", "corpus_full"], axis=1, inplace=True)

    else:

        pass


    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": input_d,
        "result": df_concat.to_dict(orient="records")
    }
