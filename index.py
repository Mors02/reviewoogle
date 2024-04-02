import Indexer
import Searcher

filename = './dataset/compact_dataset.csv'
indexPath = './indexdir'


#TO INDEX
#Indexer.index(filename, indexPath)

#TO SEARCH (DIVIDED BY SEARCH TYPE)
Searcher.base_search(indexPath)
