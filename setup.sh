#!/usr/bin/env bash

echo "Downloading word2vec model..."
wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.simple.zip && unzip wiki.simple.zip

echo "Installing requirements..."
pip3 install -r requirements.txt