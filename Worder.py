from config import word2vecPath, filename
from gensim.models import Word2Vec
from gensim import utils
import csv
import Preprocessor

def load():
    try:
        model = Word2Vec.load(word2vecPath)
        return model
    except:
        print("Modello non inizializzato.")
    

def expansion(model, query):
    expanded_query = []
    #query = utils.simple_preprocess(query)
    for word in query:
        try:
            similar_words = model.wv.most_similar(word, topn=1)
            expanded_query.extend(['(', word, '=', similar_words[0][0], ')'])
        except KeyError:
            # se la parola non è nel vocabolario
            expanded_query.append(word)
    return " ".join(expanded_query)

def store():     
    corpus = ReviewCorpus()
    model = Word2Vec(corpus)
    model.save(word2vecPath)

class ReviewCorpus:
    def __iter__(self):
        #corpus_path = datapath('lee_background.cor')
        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                print(row[2])             
                yield utils.simple_preprocess(row[2])
