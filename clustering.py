import csv
from nltk.tokenize import word_tokenize
import fasttext
from sklearn.cluster import DBSCAN
import numpy as np


from utils import TWEETS_PATH, MODEL_PATH

model = fasttext.load_model(MODEL_PATH)


def text_preprocess(text):
    tokens = word_tokenize(text)
    average = sum(list(map(lambda x: model[x], tokens))) / len(tokens)
    return average


def clustering(tweets):
    db = DBSCAN(eps=0.3, min_samples=10).fit(np.array(tweets))
    return db.labels_


if __name__ == "__main__":
    tweets = []
    metadata = []
    with open(TWEETS_PATH, 'rb') as csvfile:
        reader = csv.reader(csvfile, quotechar='"')
        for row in reader:
            metadata.append((int(row[0]), row[1]))
            tweets.append(text_preprocess(row[2]))


