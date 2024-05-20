from transformers import pipeline

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None, truncation=True)

def classify(content):
    return classifier(content)


#SENTIMENT GRAPH
#                     j       s       n       a       f       s       d       
#                     o       u       e       n       e       a       i
#                     y       r       u       g       a       d       s
#                             p       t       e       r       n       g
#                             r       r       r               e       u
#                             i       a                       s       s
#                             s       l                       s       t
#                             e
#--------------------------------------------------------
#
#   joy             1.3      1       0.6     0.8     0.7     0.6     0.6
#   
#   surprise        1        1.3     0.7     0.8     0.9     0.7     0.6
#
#   neutral         0.6      0.7     1.3     0.6     0.6     0.6     0.5
#
#   anger           0.8      0.8     0.6     1.3     0.6     0.7     0.9
#
#   fear            0.7      0.9     0.6     0.6     1.3     0.8     0.7
#
#   sadness         0.6      0.7     0.5     0.7     0.8     1.3     0.7
#   
#   disgust         0.6      0.6     0.6     0.9     0.7     0.7     1.3

sentiment_relationships = {
                            "joy":      {"joy": 1.3, "surprise": 1, "neutral": 0.9, "anger": 0.8, "fear": 0.7, "sadness": 0.6, "disgust": 0.6},
                            "surprise": {"joy": 1, "surprise": 1.3, "neutral": 0.8, "anger": 0.8, "fear": 0.9, "sadness": 0.7, "disgust": 0.6},
                            "neutral":  {"joy": 0.8, "surprise": 0.6, "neutral": 1.3, "anger": 0.7, "fear": 0.7, "sadness": 0.7, "disgust": 0.6},
                            "anger":    {"joy": 0.8, "surprise": 0.8, "neutral": 0.7, "anger": 1.3, "fear": 0.6, "sadness": 0.7, "disgust": 0.9},
                            "fear":     {"joy": 0.7, "surprise": 0.9, "neutral": 0.7, "anger": 0.6, "fear": 1.3, "sadness": 0.8, "disgust": 0.7},
                            "sadness":  {"joy": 0.6, "surprise": 0.7, "neutral": 0.6, "anger": 0.7, "fear": 0.8, "sadness": 1.3, "disgust": 0.7},
                            "disgust":  {"joy": 0.6, "surprise": 0.6, "neutral": 0.6, "anger": 0.9, "fear": 0.7, "sadness": 0.7, "disgust": 1.3},
                        }

def getWeight(emotion1, emotion2, score):
    return sentiment_relationships[emotion1][emotion2] * score