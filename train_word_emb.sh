#!/usr/bin/env bash

echo "Getting enwiki8..."
wget http://mattmahoney.net/dc/enwik8.zip && unzip enwik8

echo "Training the model..."
python3 -m 'import fasttext; fasttext.cbow("enwik8", "model")'