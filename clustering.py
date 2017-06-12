import csv
import dateutil
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


def normalize(data):
    norm_data = np.linalg.norm(data, axis=1)
    return norm_data


def create_report(metadata, labels):
    data = np.array([(d[4], d[5]) for d in metadata])
    times = [dateutil.parser(d[1]) for d in metadata]
    norm_data = normalize(data)
    label_set = set(labels)
    for label in label_set:
        indices = [i for i, x in enumerate(labels) if x == label]
        label_data = np.hstack((data[indices], norm_data[indices]))

        tweet_weights = np.ones_like(label_data)
        best_tweet_num = np.argmax(np.sum(np.multiply(tweet_weights, label_data), axis=0))
        # scoring cluster
        avg = np.mean(label_data, axis=1)
        std = np.std(label_data, axis=1)
        features = np.hstack((avg, std))
        weights = np.ones_like(features)  # here should be actual weights,
                                          # but since we have no data, just dummy
        score = np.sum(np.multiply(weights, features))  # linear model for ranking of clusters

        tweet_url = "https://twitter.com/%s/status/%s" % (metadata[indices[best_tweet_num]][2],
                                                          metadata[indices[best_tweet_num]][0])
        with open("cluster-%i.txt" % label, "wt") as f:
            f.write('%s, "%s", %s, %.2f\n' % (tweet_url, metadata[indices[best_tweet_num]][3],
                                              metadata[indices[best_tweet_num]][1], score))

if __name__ == "__main__":
    tweets = []
    metadata = []
    with open(TWEETS_PATH, 'rb') as csvfile:
        reader = csv.reader(csvfile, quotechar='"')
        for row in reader:
            metadata.append((int(row[0]), row[1], row[2], row[3], row[4], row[5]))
            tweets.append(text_preprocess(row[3]))
    labels = clustering(tweets)


