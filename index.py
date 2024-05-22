import Indexer
import Searcher
import Worder
import time
from config import filename, indexPath 

def Timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("RUN TIMER: " + str(end - start))
    return wrapper

#TO INDEX
#Indexer.index(filename, indexPath)

#TO SETUP WORD2VEC
#Worder.store()

#TO SEARCH (DIVIDED BY SEARCH TYPE)
@Timer
def base_search(searchterm):
    Searcher.base_search(searchterm)

@Timer
def processed_search(searchterm):
    Searcher.processed_search(searchterm)

@Timer
def processed_and_sentiment_search(searchterm, sentiment):
    Searcher.processed_and_sentiment_search(searchterm, sentiment)

@Timer
def processed_and_title_search(searchterm, title):
    Searcher.title_search(searchterm, title)

@Timer
def processed_and_word2vec_search(searchterm):
    Searcher.processed_and_word2vec_search(searchterm)

searchterm = "dota 2 good game"
title = "dota 2"
sentiment = "joy"

#base_search(searchterm)
#processed_search(searchterm)
#processed_and_sentiment_search(searchterm, sentiment)
#processed_and_title_search(searchterm, title)
processed_and_word2vec_search(searchterm)

#TEST
#should I play Dota 2? -> base_search gives a lot of other games in the results, processed_search is also faster but first result is not positive
#dota 2 good -> returns a review where it isnt good
