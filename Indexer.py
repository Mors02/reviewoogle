from whoosh.index import create_in, exists_in, open_dir
from whoosh.fields import *
import os, os.path
from transformers import pipeline
import Preprocessor
import csv

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None, truncation=True)

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
    schema = Schema(title=TEXT(stored=True), 
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

        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                #PREPROCESS
                processed_data = Preprocessor.process_document(row)
                print(processed_data)
                #SENTIMENT ANALYSIS
                sentiment_analysis = classifier(row[2])
                #STORE INSIDE THE WRITER
                #writer.add_document(title=u"First document", path=u"/a", content=u"This is the first documents we've added!")
        #writer.commit()
