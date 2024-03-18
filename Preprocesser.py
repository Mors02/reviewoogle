def process(document):
        import nltk
        from nltk.corpus import stopwords
        from nltk.stem import PorterStemmer
        #CREATE THE TOKEN LIST FOR THE NAMES
        name_tokens = nltk.word_tokenize(document[1])

        #CREATE THE TOKEN LIST FOR THE TEXT
        review_tokens = nltk.word_tokenize(document[2])

        #REMOVE STOPWORDS
        stop_words = set(stopwords.words("english"))
        review_tokens = [parola for parola in review_tokens if parola.lower() not in stop_words]
        #print(review_tokens)

        #STEMMING
        stemmer = PorterStemmer()
        processed_reviews = [stemmer.stem(token) for token in review_tokens]
        #print(processed_reviews)
        return [name_tokens, review_tokens]