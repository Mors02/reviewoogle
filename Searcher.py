import operator
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, syntax, query
import os, os.path

#DOCS:
#https://whoosh.readthedocs.io/en/latest/searching.html

def base_search(indexPath, query_terms):
    ix = open_dir(indexPath)

    qp = QueryParser("review", schema=ix.schema, group=syntax.OrGroup)
    tp = QueryParser("title", schema=ix.schema, group=syntax.OrGroup)

    query_terms = u"dota best game"
    q = qp.parse(query_terms)
    tq = tp.parse(query_terms)
    with ix.searcher() as searcher:
        #SEARCH THE QUERY
        review_results = searcher.search(q)
        title_results = searcher.search(tq)
        
        #COMBINE BOTH
        review_results.upgrade_and_extend(title_results)

        #PRINT
        for rev in review_results:
            print(rev["title"] + ": " + rev["review"] + " | " + rev["review_votes"])

