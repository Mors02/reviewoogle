import operator
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, syntax, query
import os, os.path
import Preprocessor

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
        review_results = searcher.search(q, limit=50)
        title_results = searcher.search(tq, limit=50)
        
        #COMBINE BOTH
        review_results.upgrade_and_extend(title_results)

        #PRINT
        #for rev in review_results:
          #  print(str(rev["id"]) + " | " + rev["title"] + ": " + rev["review"])

def processed_search(indexPath, query_terms):

    print("RICERCA PROCESSATA")
    ix = open_dir(indexPath)

    processed_query = Preprocessor.process(query_terms, True, True)

    qp = QueryParser("processed_review", schema=ix.schema, group=syntax.OrGroup)
    tp = QueryParser("processed_title", schema=ix.schema, group=syntax.OrGroup)

    #query_terms = u"best game dota"

    q = qp.parse(" ".join(processed_query))    
    tq = tp.parse(" ".join(processed_query))
    with ix.searcher() as searcher:
        #SEARCH THE QUERY
        review_results = searcher.search(q, limit=50)
        title_results = searcher.search(tq, limit=50)
        
        #COMBINE BOTH
        review_results.upgrade_and_extend(title_results)

        #PRINT
        #for rev in review_results:
         #   print(str(rev["id"]) + " | " + rev["title"] + ": " + rev["review"])

