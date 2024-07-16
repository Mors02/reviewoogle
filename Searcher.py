import operator
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, syntax, query, MultifieldParser
from whoosh import scoring
from whoosh.query import And
import os, os.path
import Preprocessor
import Sentiment
from config import indexPath
import Worder

howManyResults = 10
printData = True

def dont_print():
    global printData
    printData = False

#DOCS:
#https://whoosh.readthedocs.io/en/latest/searching.html

def base_search(query_terms):
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

        formatted_results = []
        #PRINT
        for rev in review_results:
            if (printData):
                print(str(rev["id"]) + " | " + rev["title"] + ": " + rev["review"])
            formatted_results.append(dict(rev))
        return formatted_results

def processed_search(query_terms):

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

        formatted_results = []
        #PRINT
        for rev in review_results:
            if (printData):
                print(str(rev["id"]) + " | " + rev["title"] + ": " + rev["review"])
            formatted_results.append(dict(rev))
        return formatted_results


def processed_and_sentiment_search(query_terms):

    print("RICERCA PROCESSATA E SENTIMENT")
    ix = open_dir(indexPath)
    
    processed_query = Preprocessor.process(query_terms, True, True)

    qcontent = MultifieldParser(["processed_review", "processed_title"], schema=ix.schema, group=syntax.OrGroup).parse(" ".join(processed_query))
    qtitle = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup).parse(" ".join(processed_query))
    retrieved_sentiment = Sentiment.classify(query_terms)[0][0]
    #qsentiment = QueryParser("sentiment", schema=ix.schema).parse(retrieved_sentiment["label"])    
    q = And([qcontent, qtitle])

    with ix.searcher() as searcher:
        #SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)
        #GET COEFFICIENT BASED ON SENTIMENT RELATIONSHIP AND REORDER
        combined_results = []
        for (index, rev) in enumerate(review_results):
            res = dict(rev)
            res["score"] = rev.score + Sentiment.getWeight(retrieved_sentiment["label"], rev["sentiment"], rev["sentiment_score"])            
            combined_results.append(res)
        combined_results = sorted(combined_results, key=lambda item: item["score"], reverse=True)

        #PRINT
        formatted_results = []
        
        for rev in combined_results:
            if (printData):
                print(str(rev["score"]) + " | " + rev["title"] + ": " + rev["review"] + " /" + str(rev["sentiment"]))
            formatted_results.append(dict(rev))
        return formatted_results

def title_search(query_terms, title):

    print("RICERCA PER TITOLO")
    ix = open_dir(indexPath)

    processed_query = Preprocessor.process(query_terms, True, True)
    processed_title = Preprocessor.process(title, False, False)

    qp = QueryParser("processed_review", schema=ix.schema, group=syntax.OrGroup).parse(" ".join(processed_query)) 
    tp = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup).parse(" ".join(processed_title))

    q = And([qp, tp])
    #tq = tp.parse(processed_query)

    with ix.searcher() as searcher:
        #SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)
        #title_results = searcher.search(tp, limit=howManyResults*2)
        #BOOST A LITTLE THE TITLE
        #review_results.upgrade(title_results)

        #PRINT
        if (printData):
            for rev in review_results:
                print(str(rev.score) + " | " + rev["title"] + ": " + rev["review"])
        return review_results

def word2vec_and_sentiment_search(query_terms):
    print("RICERCA PROCESSATA, SENTIMENT E WORD2VEC")
    ix = open_dir(indexPath)
    model = Worder.load()
    
    processed_query = Preprocessor.process(query_terms, True, True)
    expanded_query = Worder.expansion(model, processed_query)
    qcontent = MultifieldParser(["processed_review", "processed_title"], schema=ix.schema, group=syntax.OrGroup).parse(expanded_query)
    qtitle = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup).parse(expanded_query)
    retrieved_sentiment = Sentiment.classify(query_terms)[0][0]
    #qsentiment = QueryParser("sentiment", schema=ix.schema).parse(retrieved_sentiment["label"])    
    q = And([qcontent, qtitle])

    with ix.searcher() as searcher:
        #SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)
        #GET COEFFICIENT BASED ON SENTIMENT RELATIONSHIP AND REORDER
        combined_results = []
        for (index, rev) in enumerate(review_results):
            res = dict(rev)
            res["score"] = rev.score + Sentiment.getWeight(retrieved_sentiment["label"], rev["sentiment"], rev["sentiment_score"])            
            combined_results.append(res)
        combined_results = sorted(combined_results, key=lambda item: item["score"], reverse=True)

        #PRINT
        formatted_results = []
        
        for rev in combined_results:
            if (printData):
                print(str(rev["score"]) + " | " + rev["title"] + ": " + rev["review"] + " /" + str(rev["sentiment"]))
            formatted_results.append(dict(rev))
        return formatted_results

def processed_and_word2vec_search(query_terms):
    print("RICERCA PROCESSATA E WORD2VEC")
    model = Worder.load()
    ix = open_dir(indexPath)

    processed_query = Preprocessor.process(query_terms, True, True)
    expanded_query = Worder.expansion(model, processed_query)
    
    qp = QueryParser("processed_review", schema=ix.schema, group=syntax.OrGroup).parse(expanded_query)
    tp = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup).parse(expanded_query)    

    q = And([qp, tp])
    #tq = tp.parse(processed_query)

    with ix.searcher() as searcher:
        #SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)

        #PRINT
        formatted_results = []
        
        for rev in review_results:
            if (printData):
                print(str(rev.score) + " | " + rev["title"] + ": " + rev["review"])  
            formatted_results.append(rev)
        return formatted_results

def advanced_search(query_terms):
    return
''' NON FUNZIONA MOLTO BENE
    ix = open_dir(indexPath)

    processed_query = Preprocessor.process(query_terms, True, True)
    print(processed_query)
    #expanded_query = Worder.expansion(model, processed_query)
    shouldSentiment = input("Ricerca per sentiment - 1. Si     2. No\n> ")
    if (shouldSentiment == "1"):
        retrieved_sentiment = Sentiment.classify(query_terms)[0][0]

    shouldWord2vec = input("Espansione con word2vec - 1. Si     2. No\n> ")
    if (shouldWord2vec == "1"):
        model = Worder.load()
        query_terms = Worder.expansion(model, query_terms.split())
        print(query_terms)
    print(query_terms)
    qp = QueryParser("processed_review", schema=ix.schema).parse(query_terms)
    print(qp)

    #tp = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup).parse(query_terms)    

    with ix.searcher() as searcher:
        #SEARCH THE QUERY
        review_results = searcher.search(qp, limit=howManyResults)

        if (shouldSentiment == "1"):
            combined_results = reorder_results_with_sentiment(review_results, retrieved_sentiment)
            review_results = combined_results

        #PRINT
        if (printData):
            for rev in review_results:
                if (shouldSentiment != "1"):
                    print(str(rev.score) + " | " + rev["title"] + ": " + rev["review"])  
                else:
                    print(str(rev["score"]) + " | " + rev["title"] + ": " + rev["review"] + " /" + rev["sentiment"])
'''

def reorder_results_with_sentiment(review_results, retrieved_sentiment):
    combined_results = []
    for (index, rev) in enumerate(review_results):
        res = dict(rev)
        res["score"] = rev.score * Sentiment.getWeight(retrieved_sentiment["label"], rev["sentiment"], rev["sentiment_score"])            
        combined_results.append(res)
    combined_results = sorted(combined_results, key=lambda item: item["score"], reverse=True)
    return combined_results
