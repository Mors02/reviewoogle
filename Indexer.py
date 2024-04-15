from whoosh.index import create_in, exists_in, open_dir
from whoosh.fields import *
import os, os.path
import Preprocessor
import csv
import Sentiment

def create_index(path):
    # Colonne della tabella:
    # title
    # processed_title
    # review
    # processed_review
    # sentiment
    # sentiment_score
    # review_score
    # review_votes
    schema = Schema(id=NUMERIC(numtype=int, stored=True),
                    title=TEXT(stored=True), 
                    processed_title=TEXT(stored=True), 
                    review=TEXT(stored=True),
                    processed_review=TEXT(stored=True),
                    sentiment=TEXT(stored=True),
                    sentiment_score=NUMERIC(stored=True, numtype=Decimal, decimal_places=4),
                    review_score=NUMERIC(stored=True, numtype=int),
                    review_votes=NUMERIC(stored=True, numtype=int)
                    )

    if not os.path.exists(path):
        os.mkdir(path)
    ix = create_in(path, schema)

def index(filename, path):
    create_index(path)
    #IF THE II IS CREATED CORRECTLY
    if (exists_in(path)):
        #OPEN THE DIRECTORY
        ix = open_dir(path)
        writer = ix.writer()

        id=0

        # OPEN THE CSV FILE AND READ EACH LINE
        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                #PREPROCESS
                processed_data = Preprocessor.process_document(row)
                #print(processed_data)
                #SENTIMENT ANALYSIS
                sentiment_analysis = Sentiment.classify(row[2])
                print(sentiment_analysis)
                #STORE INSIDE THE WRITER
                writer.add_document(id=id, 
                                    title=row[1], 
                                    processed_title=processed_data[0], 
                                    review=row[2],
                                    processed_review=processed_data[1],
                                    sentiment=sentiment_analysis[0][0]["label"],
                                    sentiment_score=sentiment_analysis[0][0]["score"],
                                    review_score=row[3],
                                    review_votes=row[4]
                                    )
                id = id+1
        writer.commit()
