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

exit = True

def setup():
    #TO INDEX AND SETUP WORD2VEC
    Indexer.index(filename, indexPath)
    Worder.store()

#TO SEARCH (DIVIDED BY SEARCH TYPE)
@Timer
def base_search():
    searchterm = queryInput()
    Searcher.base_search(searchterm)

@Timer
def processed_search():
    searchterm = queryInput()
    Searcher.processed_search(searchterm)

@Timer
def processed_and_sentiment_search():
    searchterm = queryInput()
    Searcher.processed_and_sentiment_search(searchterm)

@Timer
def processed_and_title_search():
    searchterm = queryInput()
    title = input('Inserisci il titolo: ')
    Searcher.title_search(searchterm, title)

@Timer
def processed_and_word2vec_search():
    searchterm = queryInput()
    Searcher.processed_and_word2vec_search(searchterm)

@Timer
def word2vec_and_sentiment_search():
    searchterm = queryInput()
    Searcher.word2vec_and_sentiment_search(searchterm)

@Timer
def advanced_search():
    searchterm = queryInput()
    Searcher.advanced_search()

def exitProgram():
    global exit
    exit = False

def queryInput():
    return input('Inserisci il testo da cercare\n >')

searchterm = "dota 2 good game"
title = "dota 2"
functionMap = {'1': setup, '2': base_search, '3': processed_search, '4': processed_and_sentiment_search, '5': processed_and_title_search, '6': word2vec_and_sentiment_search, '7': exitProgram, '8': advanced_search}
#searchquery = "russia & riki & equipment & place title:(dota 2)"

while(exit):
    selection = input(
'1. Riforma Index e Word2Vec\n\
2. Ricerca base\n\
3. Ricerca processata\n\
4. Ricerca processata con sentiment\n\
5. Ricerca processsata per titolo\n\
6. Ricerca Word2Vec e Sentiment\n\
7. Esci\n')
    functionToCall = functionMap[selection]
    functionToCall()

#base_search(searchterm)
#processed_search(searchterm)
#processed_and_sentiment_search(searchterm, sentiment)
#processed_and_title_search(searchterm, title)
#processed_and_word2vec_search(searchterm)
#word2vec_and_sentiment_search(searchterm)
#advanced_search(searchquery)

#TEST
#should I play Dota 2? -> base_search gives a lot of other games in the results, processed_search is also faster but first result is not positive
#dota 2 good -> returns a review where it isnt good
