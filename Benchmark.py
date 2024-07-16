import Searcher
import math
queries = ["World at War are there custom zombie maps", 
           "What is the best game ever?", 
           "Black ops 2 or Black ops 3", 
           "What is the worst RPG?", 
           "Dragon Age Origins good plot",
           "Resident Evil is it scary?",
           "Should I buy Far Cry Primal?",
           "How fun is Jackbox Party?",
           "Is Terraria worth playing with friends?",
           "No Mans Sky boring"]

Searcher.dont_print()


def calculate_MAP(results):
    relevant_docs = 0
    average_precision = 0
    MAP = 0
    for query in results:
        #find the precision of the current doc
        average_precision = 0
        for idx, result in enumerate(query):
            if (result["relevant"] == "1"):
                relevant_docs += 1
                precision = float(relevant_docs)/(idx+1)
                average_precision += float(precision)
        MAP += (average_precision / len(query))
    MAP = MAP / len(results)
    return MAP

def calculate_DCG(results):
    average_DCG = 0
    for query in results:
        DCG = 0
        for idx, result in enumerate(query):
            if idx == 0:
                DCG += int(result["grade"])
            else:
                DCG += int(result["grade"]) / math.log(int(idx)+1, 2)
        average_DCG += DCG
    average_DCG = average_DCG / len(results)
    return average_DCG

def calculate_precision(results):
    precision = 0
    for query in results:
        relevant_documents = 0
        for result in query:
            if result["relevant"] == "1":
                relevant_documents += 1
        precision += relevant_documents / len(query)
    precision = precision / len(results)
    return precision

base_results = []
processed_results = []
w2v_results = []
sentiment_results = []
w2v_sentiment_results = []

for index, query in enumerate(queries):
    print("\nQUERY: " + query)
    base = Searcher.base_search(query)
    #print(base)
    query_row = []
    for rev_idx, rev in enumerate(base):
        print(rev["review"])
        relevant = input("Rilevante? ")
        grade = input("Voto? ")
        query_row.insert(rev_idx, {"relevant": relevant, "grade": grade})
    base_results.insert(index, query_row)

    processed = Searcher.processed_search(query)
    query_row = []
    for rev_idx, rev in enumerate(processed):
        print(rev["review"])
        relevant = input("Rilevante? ")
        grade = input("Voto? ")
        query_row.insert(rev_idx, {"relevant": relevant, "grade": grade})
    processed_results.insert(index, query_row)

    sentiment = Searcher.processed_and_sentiment_search(query)
    query_row = []
    for rev_idx, rev in enumerate(sentiment):
        print(rev["review"])
        relevant = input("Rilevante? ")
        grade = input("Voto? ")
        query_row.insert(rev_idx, {"relevant": relevant, "grade": grade})
    sentiment_results.insert(index, query_row)

    w2v = Searcher.processed_and_sentiment_search(query)
    query_row = []
    for rev_idx, rev in enumerate(w2v):
        print(rev["review"])
        relevant = input("Rilevante? ")
        grade = input("Voto? ")
        query_row.insert(rev_idx, {"relevant": relevant, "grade": grade})
    w2v_results.insert(index, query_row)

    w2v_sentiment = Searcher.word2vec_and_sentiment_search(query)
    query_row = []
    for rev_idx, rev in enumerate(w2v):
        print(rev["review"])
        relevant = input("Rilevante? ")
        grade = input("Voto? ")
        query_row.insert(rev_idx, {"relevant": relevant, "grade": grade})
    w2v_sentiment_results.insert(index, query_row)
    
with open('results.txt', 'w') as f:
    print("BASE SEARCH:", file=f)
    print(calculate_MAP(base_results), file=f)
    print(calculate_DCG(base_results), file=f)
    print(calculate_precision(base_results), file=f)
    print("\n", file=f)
    print("PROCESSED SEARCH:", file=f)
    print(calculate_MAP(processed_results), file=f)
    print(calculate_DCG(processed_results), file=f)
    print(calculate_precision(processed_results), file=f)
    print("\n", file=f)
    print("W2V SEARCH:", file=f)
    print(calculate_MAP(w2v_results), file=f)
    print(calculate_DCG(w2v_results), file=f)
    print(calculate_precision(w2v_results), file=f)
    print("\n", file=f)
    print("SENTIMENT SEARCH:", file=f)
    print(calculate_MAP(sentiment_results), file=f)
    print(calculate_DCG(sentiment_results), file=f)
    print(calculate_precision(sentiment_results), file=f)
    print("\n", file=f)
    print("W2V AND SENTIMENT SEARCH:", file=f)
    print(calculate_MAP(w2v_sentiment_results), file=f)
    print(calculate_DCG(w2v_sentiment_results), file=f)
    print(calculate_precision(w2v_sentiment_results), file=f)

