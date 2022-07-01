from deep_translator import GoogleTranslator
import swifter


def translate_fn(x, source, target):
    try:
        translated = GoogleTranslator(source=source, target=target).translate(x)

    except Exception as e:
        print(e)
        translated = x

    return translated


def translate_df(df, column, source, target):

    df[column] = df[column].swifter.progress_bar(False).apply(lambda x: translate_fn(x, source, target) if x != '' else x)

    return df
