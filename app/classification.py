from transformers import pipeline
import pandas as pd
import swifter
from transformers import AutoTokenizer, AutoModelForTokenClassification


def load_classifier():

    classifier = pipeline("zero-shot-classification",
                          model="valhalla/distilbart-mnli-12-3",
                          tokenizer="valhalla/distilbart-mnli-12-3")
    return classifier


def classification(x, classifier, labels):

    candidate_labels = labels

    output = classifier(x, candidate_labels, multi_label=True)

    del output["sequence"]

    labels = output["labels"]
    scores = output["scores"]

    zip_iterator = zip(labels, scores)
    a_dictionary = dict(zip_iterator)

    return a_dictionary


def classifier_processing(df, col_classify, classifier, labels):

    df["output"] = df[col_classify].swifter.progress_bar(False).apply(
        lambda x: classification(x, classifier, labels) if x is not None else None)

    df = pd.concat([df, df['output'].swifter.progress_bar(False).apply(pd.Series)], axis=1)

    df.drop('output', axis=1, inplace=True)

    return df

def load_ner():
    # load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-large-finetuned-conll03-english")
    model = AutoModelForTokenClassification.from_pretrained("xlm-roberta-large-finetuned-conll03-english")

    ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="SIMPLE")

    return ner

def perform_ner(text, ner):

    result = ner(text)

    names = ["PER",
             "ORG",
             "LOC",
             "MISC"]
    d = {}

    for n in names:
        d[n] = []
        for k in result:
            if k["entity_group"] == n and k["score"] > 0.9:
                d[n].append(k["word"])
        d[n] = list(set(d[n]))

    PER = d["PER"]
    ORG = d["ORG"]
    LOC = d["LOC"]
    MISC = d["MISC"]

    return PER, ORG, LOC, MISC
