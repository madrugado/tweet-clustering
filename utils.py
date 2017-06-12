import configparser
import os

CONF_PATH = "config.ini"
URL_LIST_PATH = "url_list.txt"
LAST_IDS_JSON = "last_ids.json"
TWEETS_PATH = "tweet.csv"
MODEL_PATH = "wiki.simple.bin"


def get_config():
    conf = configparser.ConfigParser()
    if not os.path.exists(CONF_PATH):
        print("Creating stub config...\n"
              "You need to replace STUB with your actual tokens in file {}".format(CONF_PATH))
        conf["twitter"] = {"consumer_key": "STUB", "consumer_secret": "STUB",
                           "access_key": "STUB", "access_secret": 'STUB'}
        with open(CONF_PATH, 'wt') as configfile:
            conf.write(configfile)
        exit(1)

    conf.read(CONF_PATH)
    return conf
