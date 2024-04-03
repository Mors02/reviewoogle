import Indexer
import Searcher
import time

filename = './dataset/compact_dataset.csv'
indexPath = './indexdir'


def Timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("RUN TIMER: " + str(end - start))
    return wrapper

#TO INDEX
#Indexer.index(filename, indexPath)

#TO SEARCH (DIVIDED BY SEARCH TYPE)
@Timer
def base_search():
    Searcher.base_search(indexPath, u"should i play black ops 3?")

@Timer
def processed_search():
    Searcher.processed_search(indexPath, u"should i play black ops 3?")


base_search()
processed_search()

#TEST
#should I play Dota2? -> base_search gives a lot of other games in the results, processed_search is better but slower
#
