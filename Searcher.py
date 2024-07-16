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

howManyResults = 25
printData = True

def dont_print():
    global printData
    printData = False

# DOCS:
# https://whoosh.readthedocs.io/en/latest/searching.html

def base_search(query_terms):
    print("\n--- RICERCA BASE ---\n")
    ix = open_dir(indexPath)

    qp = QueryParser("review", schema=ix.schema, group=syntax.AndGroup)
    tp = QueryParser("title", schema=ix.schema, group=syntax.AndGroup)

    # query_terms = u"best game dota"
    q = qp.parse(query_terms)    
    tq = tp.parse(query_terms)

    with ix.searcher() as searcher:
        # SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)
        title_results = searcher.search(tq, limit=howManyResults)
        
        # COMBINE BOTH
        review_results.upgrade_and_extend(title_results)

        formatted_results = []
        # PRINT
        for rev in review_results:
            if (printData):
                print(str(rev["id"]) + " | " + rev["title"] + ": " + rev["review"] + "\n")
            formatted_results.append(dict(rev))
        return formatted_results

def processed_search(query_terms):
    print("\n--- RICERCA PROCESSATA ---\n")
    ix = open_dir(indexPath)

    processed_query = Preprocessor.process(query_terms, True, True)

    qp = QueryParser("processed_review", schema=ix.schema, group=syntax.AndGroup)
    tp = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup)

    q = qp.parse(" ".join(processed_query))
    tq = tp.parse(" ".join(processed_query))

    print(And([q, tq]))

    with ix.searcher() as searcher:
        # SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)
        title_results = searcher.search(tq, limit=howManyResults)
        
        # COMBINE BOTH
        review_results.upgrade_and_extend(title_results)

        # BOOST A LITTLE THE TITLE
        review_results.upgrade(title_results)

        formatted_results = []
        # PRINT
        for rev in review_results:
            if (printData):
                print(str(rev["id"]) + " | " + rev["title"] + ": " + rev["review"] + "\n")
            formatted_results.append(dict(rev))
        return formatted_results


def processed_and_sentiment_search(query_terms):
    print("\n--- RICERCA PROCESSATA E SENTIMENT ---\n")
    ix = open_dir(indexPath)
    
    processed_query = Preprocessor.process(query_terms, True, True)

    qcontent = MultifieldParser(["processed_review", "processed_title"], schema=ix.schema, group=syntax.OrGroup).parse(" ".join(processed_query))
    qtitle = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup).parse(" ".join(processed_query))
    retrieved_sentiment = Sentiment.classify(query_terms)[0][0]
    # qsentiment = QueryParser("sentiment", schema=ix.schema).parse(retrieved_sentiment["label"])    
    q = And([qcontent, qtitle])

    with ix.searcher() as searcher:
        # SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)
        # GET COEFFICIENT BASED ON SENTIMENT RELATIONSHIP AND REORDER
        combined_results = []
        for (index, rev) in enumerate(review_results):
            res = dict(rev)
            res["score"] = rev.score + Sentiment.getWeight(retrieved_sentiment["label"], rev["sentiment"], rev["sentiment_score"])            
            combined_results.append(res)
        combined_results = sorted(combined_results, key=lambda item: item["score"], reverse=True)

        # PRINT
        formatted_results = []
        
        for rev in combined_results:
            if (printData):
                print(str(rev["score"]) + " | " + rev["title"] + ": " + rev["review"] + " /" + str(rev["sentiment"]) + "\n")
            formatted_results.append(dict(rev))
        return formatted_results

def title_search(query_terms, title):
    print("\n--- RICERCA PER TITOLO ---\n")
    ix = open_dir(indexPath)

    processed_query = Preprocessor.process(query_terms, True, True)
    processed_title = Preprocessor.process(title, False, False)

    qp = QueryParser("processed_review", schema=ix.schema, group=syntax.OrGroup).parse(" ".join(processed_query)) 
    tp = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup).parse(" ".join(processed_title))

    q = And([qp, tp])
    # tq = tp.parse(processed_query)

    with ix.searcher() as searcher:
        # SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)
        # title_results = searcher.search(tp, limit=howManyResults*2)

        # BOOST A LITTLE THE TITLE
        # review_results.upgrade(title_results)

        # PRINT
        if (printData):
            for rev in review_results:
                print(str(rev.score) + " | " + rev["title"] + ": " + rev["review"] + "\n")
        return review_results

def word2vec_and_sentiment_search(query_terms):
    print("\n--- RICERCA PROCESSATA, SENTIMENT E WORD2VEC ---\n")
    ix = open_dir(indexPath)
    model = Worder.load()
    
    processed_query = Preprocessor.process(query_terms, True, True)
    expanded_query = Worder.expansion(model, processed_query)

    qcontent = MultifieldParser(["processed_review", "processed_title"], schema=ix.schema, group=syntax.OrGroup).parse(expanded_query)
    qtitle = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup).parse(expanded_query)
    retrieved_sentiment = Sentiment.classify(query_terms)[0][0]
    # qsentiment = QueryParser("sentiment", schema=ix.schema).parse(retrieved_sentiment["label"])    
    q = And([qcontent, qtitle])

    with ix.searcher() as searcher:
        # SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)
        # GET COEFFICIENT BASED ON SENTIMENT RELATIONSHIP AND REORDER
        combined_results = []
        for (index, rev) in enumerate(review_results):
            res = dict(rev)
            res["score"] = rev.score + Sentiment.getWeight(retrieved_sentiment["label"], rev["sentiment"], rev["sentiment_score"])            
            combined_results.append(res)
        combined_results = sorted(combined_results, key=lambda item: item["score"], reverse=True)

        # PRINT
        formatted_results = []
        
        for rev in combined_results:
            if (printData):
                print(str(rev["score"]) + " | " + rev["title"] + ": " + rev["review"] + " /" + str(rev["sentiment"]) + "\n")
            formatted_results.append(dict(rev))
        return formatted_results

def processed_and_word2vec_search(query_terms):
    print("\n--- RICERCA PROCESSATA E WORD2VEC ---\n")
    model = Worder.load()
    ix = open_dir(indexPath)

    processed_query = Preprocessor.process(query_terms, True, True)
    expanded_query = Worder.expansion(model, processed_query)
    
    qp = QueryParser("processed_review", schema=ix.schema, group=syntax.AndGroup).parse(expanded_query)
    tp = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup).parse(expanded_query)    

    q = And([qp, tp])
    # tq = tp.parse(processed_query)

    with ix.searcher() as searcher:
        # SEARCH THE QUERY
        review_results = searcher.search(q, limit=howManyResults)

        # PRINT
        formatted_results = []
        
        for rev in review_results:
            if (printData):
                print(str(rev.score) + " | " + rev["title"] + ": " + rev["review"] + "\n")  
            formatted_results.append(rev)
        return formatted_results

def advanced_search(query_terms):
    query_obj = {}
    terms = query_terms.split("; ")
    for term in terms:
        term_array = term.split(": ")        
        query_obj[term_array[0]] = term_array[1]
    ix = open_dir(indexPath)
    processed_query = ''    

    if 'content' in query_obj:
        processed_query = query_obj['content']

    if 'processed' in query_obj and (query_obj['processed'] == 'yes' or query_obj['processed'] == 'yes;') and 'content' in query_obj:
        processed_query = Preprocessor.process(query_obj['content'], True, True)
        processed_query = " ".join(processed_query)
    #expanded_query = Worder.expansion(model, processed_query)
    if ('sentiment' in query_obj and (query_obj['sentiment'] == 'yes' or query_obj['sentiment'] == 'yes;') and 'content' in query_obj):
        retrieved_sentiment = Sentiment.classify(query_obj['content'])[0][0]
    processed_query = processed_query.replace("|", "OR")
    processed_query = processed_query.replace("&", "AND")

    if 'processed' in query_obj and (query_obj['processed'] == 'yes' or query_obj['processed'] == 'yes;') and 'content' in query_obj:
        q = QueryParser("processed_review", schema=ix.schema).parse(processed_query)
    else:
        q = QueryParser("review", schema=ix.schema).parse(processed_query)

    if 'title' in query_obj:
        tq = QueryParser('title', schema=ix.schema).parse(query_obj['title'])
        if 'content' in query_obj:
            q = And([q, tq])
        else:
            q = tq
    print(q)


    #tp = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup).parse(query_terms)    

    with ix.searcher() as searcher:
        #SEARCH THE QUERY
        res_num = howManyResults
        if 'num_results' in query_obj:
            res_num = int(query_obj['num_results'])
        review_results = searcher.search(q, limit=res_num)

        if ('sentiment' in query_obj and (query_obj['sentiment'] == 'yes' or query_obj['sentiment'] == 'yes;')):
            combined_results = reorder_results_with_sentiment(review_results, retrieved_sentiment)
            review_results = combined_results

        #PRINT
        if (printData):
            for rev in review_results:
                if ('sentiment' in query_obj and (query_obj['sentiment'] == 'yes' or query_obj['sentiment'] == 'yes;')):
                    print(str(rev["score"]) + " | " + rev["title"] + ": " + rev["review"] + " /" + rev["sentiment"])                   
                else:
                    print(str(rev.score) + " | " + rev["title"] + ": " + rev["review"])  
                    

def reorder_results_with_sentiment(review_results, retrieved_sentiment):
    combined_results = []
    for (index, rev) in enumerate(review_results):
        res = dict(rev)
        res["score"] = rev.score * Sentiment.getWeight(retrieved_sentiment["label"], rev["sentiment"], rev["sentiment_score"])            
        combined_results.append(res)
    combined_results = sorted(combined_results, key=lambda item: item["score"], reverse=True)
    return combined_results
