import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def process_document(document):
        processed_reviews = process(document[2], True, True)
        processed_title = process(document[1])

        return [processed_title, processed_reviews]

def process(text, removeStopwords=False, withStemming=False):
        #CREATE THE TOKEN LIST FOR THE TEXT
        tokens = nltk.word_tokenize(text)
        #REMOVE PUNCTUATION
        tokens = [word.lower() for word in tokens]
        custom_tokens = []
        for token in tokens:
                if token.isalpha() or token in ['&', '|']:
                        custom_tokens.append(token.lower())

        #REMOVE STOPWORDS
        if (removeStopwords):
                stop_words = set(stopwords.words("english"))
                custom_tokens = [parola for parola in tokens if parola.lower() not in stop_words]

        #STEMMING
        if (withStemming):
                stemmer = PorterStemmer()
                custom_tokens = [stemmer.stem(token) for token in tokens]

        return custom_tokens