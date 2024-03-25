import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def process_document(document):
        processed_reviews = process(document[2], True, True)
        processed_title = process(document[1])

        return [processed_title, processed_reviews]


        #CREATE THE TOKEN LIST FOR THE NAMES
        name_tokens = nltk.word_tokenize(document[1])
        #REMOVE PUNCTUATION
        name_tokens = [word.lower() for word in name_tokens if word.isalpha()]

        #CREATE THE TOKEN LIST FOR THE TEXT
        review_tokens = nltk.word_tokenize(document[2])
        review_tokens = [word.lower() for word in review_tokens if word.isalpha()]

        #REMOVE STOPWORDS
        stop_words = set(stopwords.words("english"))
        review_tokens = [parola for parola in review_tokens if parola.lower() not in stop_words]
        #print(review_tokens)

        #STEMMING
        stemmer = PorterStemmer()
        processed_reviews = [stemmer.stem(token) for token in review_tokens]
        #print(processed_reviews)
        return [name_tokens, review_tokens]

def process(text, removeStopwords=False, withStemming=False):
        #CREATE THE TOKEN LIST FOR THE TEXT
        tokens = nltk.word_tokenize(text)
        #REMOVE PUNCTUATION
        tokens = [word.lower() for word in tokens if word.isalpha()]

        #REMOVE STOPWORDS
        if (removeStopwords):
                stop_words = set(stopwords.words("english"))
                tokens = [parola for parola in tokens if parola.lower() not in stop_words]

        #STEMMING
        if (withStemming):
                stemmer = PorterStemmer()
                tokens = [stemmer.stem(token) for token in tokens]

        return tokens