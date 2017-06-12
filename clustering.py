import csv
import datetime

import subprocess
from nltk.tokenize import wordpunct_tokenize
import fasttext
from sklearn.cluster import DBSCAN
import numpy as np
import re

from utils import TWEETS_PATH, MODEL_PATH

model = fasttext.load_model(MODEL_PATH)
pattern = re.compile('[\W]+')


def text_preprocess(text):
    tokens = wordpunct_tokenize(text)
    filtered = list(filter(lambda x: x, map(lambda y: pattern.sub('', y), tokens)))
    average = np.mean(list(map(lambda x: model[x], filtered)), axis=0)
    return average


def clustering(tweets):
    db = DBSCAN().fit(np.array(tweets))
    return db.labels_


def normalize(rawpoints):
    mins = np.min(rawpoints, axis=0)
    maxs = np.max(rawpoints, axis=0)
    rng = maxs - mins
    return (maxs - rawpoints) / rng


def create_report(metadata, labels):
    data = np.array([(int(d[4]), int(d[5])) for d in metadata])
    times = [datetime.datetime.strptime(d[2], "%Y-%m-%d %H:%M:%S") for d in metadata]
    norm_data = normalize(data)
    label_set = set(labels)
    for label in label_set:
        if label == -1:
            continue
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

        tweet_url = "https://twitter.com/%s/status/%s" % (metadata[indices[best_tweet_num]][1],
                                                          metadata[indices[best_tweet_num]][0])
        with open("clusters/cluster-%i.txt" % label, "wt") as f:
            f.write('%s, "%s", %s, %.2f\n' % (tweet_url, metadata[indices[best_tweet_num]][3],
                                              metadata[indices[best_tweet_num]][2], score))

if __name__ == "__main__":
    tweets = []
    metadata = []
    with open(TWEETS_PATH, 'rt') as csvfile:
        csvfile.readline()
        reader = csv.reader(csvfile, quotechar='"')
        for row in reader:
            metadata.append((int(row[0]), row[1], row[2], row[3], row[4], row[5]))
            tweets.append(text_preprocess(row[3]))
    labels = clustering(tweets)
    subprocess.call(["rm", "-rf", "clusters/*"])
    create_report(metadata, labels)


