# Tweet Clustering

## Setup
Run ```./setup.sh```

## Demo
To get new tweets run ```python3 getter.py```.

To get clustering of existing data run ```python3 clusting.py```

## Periodic run
You can add ```getter.py``` and ```clustering.py``` to cron like this:
```bash
crontab -e

# inside crontab
*/10 * * * * python3 `pwd`/getter.py && python3 `pwd`/clustering.py 
```