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

        #PRINT
        if (printData):
            for rev in review_results:
                print(str(rev["id"]) + " | " + rev["title"] + ": " + rev["review"])

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

        #PRINT
        if (printData):
            for rev in review_results:
                print(str(rev["id"]) + " | " + rev["title"] + ": " + rev["review"])


def processed_and_sentiment_search(query_terms):

    print("RICERCA PROCESSATA E SENTIMENT")
    ix = open_dir(indexPath)
    '''
    processed_query = Preprocessor.process(query_terms, True, True)

    #customScorer = scoring.FunctionWeighting(custom_scorer)

    processed_query = Preprocessor.process(query_terms, True, True)
    parser = MultifieldParser(["processed_review", "processed_title"], schema=ix.schema, group=syntax.OrGroup)
    #qp = QueryParser("processed_review", schema=ix.schema, group=syntax.OrGroup)
    sp = QueryParser("sentiment", schema=ix.schema)

    #query_terms = u"best game dota"

    q = parser.parse(" ".join(processed_query))    
    tq = sp.parse(sentiment)
    #q = qp.parse(processed_query)    
    #tq = tp.parse(processed_query)

    
    #print(sentiment)
    #custom_scorer = CustomScorer()
    '''
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
        if (printData):
            for rev in combined_results:
                #print(rev)
                print(str(rev["score"]) + " | " + rev["title"] + ": " + rev["review"] + " /" + str(rev["sentiment"]))

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

def processed_and_word2vec_search(query_terms):

    print("RICERCA PER TITOLO")
    model = Worder.load()
    ix = open_dir(indexPath)

    processed_query = Preprocessor.process(query_terms, True, True)
    Worder.expansion(model, processed_query)

    qp = QueryParser("processed_review", schema=ix.schema, group=syntax.OrGroup).parse(" ".join(processed_query))
    tp = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup).parse(" ".join(processed_query))    

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

