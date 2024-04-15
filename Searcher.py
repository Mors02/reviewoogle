import operator
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, syntax, query
import os, os.path
import Preprocessor
import Sentiment

howManyResults = 10
printData = True

#DOCS:
#https://whoosh.readthedocs.io/en/latest/searching.html

def base_search(indexPath, query_terms):
    ix = open_dir(indexPath)

    qp = QueryParser("review", schema=ix.schema, group=syntax.OrGroup)
    tp = QueryParser("title", schema=ix.schema, group=syntax.OrGroup)

    #query_terms = u"best game dota"
    q = qp.parse(query_terms)    
    tq = tp.parse(query_terms)
    with ix.searcher() as searcher:
        #SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)
        title_results = searcher.search(tq, limit=howManyResults)
        
        #COMBINE BOTH
        review_results.upgrade_and_extend(title_results)

        #PRINT
        if (printData):
            for rev in review_results:
                print(str(rev["id"]) + " | " + rev["title"] + ": " + rev["review"])

def processed_search(indexPath, query_terms):

    print("RICERCA PROCESSATA")
    ix = open_dir(indexPath)

    processed_query = Preprocessor.process(query_terms, True, True)

    qp = QueryParser("processed_review", schema=ix.schema, group=syntax.OrGroup)
    tp = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup)

    #query_terms = u"best game dota"

    q = qp.parse(" ".join(processed_query))    
    tq = tp.parse(" ".join(processed_query))
    #q = qp.parse(processed_query)    
    #tq = tp.parse(processed_query)

    with ix.searcher() as searcher:
        #SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)
        title_results = searcher.search(tq, limit=howManyResults)
        
        #COMBINE BOTH
        review_results.upgrade_and_extend(title_results)

        #BOOST A LITTLE THE TITLE
        review_results.upgrade(title_results)

        #PRINT
        if (printData):
            for rev in review_results:
                print(str(rev["id"]) + " | " + rev["title"] + ": " + rev["review"])


def processed_and_sentiment_search(indexPath, query_terms):

    print("RICERCA PROCESSATA E SENTIMENT")
    ix = open_dir(indexPath)

    processed_query = Preprocessor.process(query_terms, True, True)

    qp = QueryParser("processed_review", schema=ix.schema, group=syntax.OrGroup)
    tp = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup)

    q = qp.parse(" ".join(processed_query))    
    tq = tp.parse(" ".join(processed_query))

    sentiment = Sentiment.classify(processed_query)
    print(sentiment)


    with ix.searcher() as searcher:
        #SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)
        title_results = searcher.search(tq, limit=howManyResults)
        
        #COMBINE BOTH
        review_results.upgrade_and_extend(title_results)

        #PRINT
        if (printData):
            for rev in review_results:
                print(str(rev.score) + " | " + rev["title"] + ": " + rev["review"] + " /" + rev["sentiment"])

