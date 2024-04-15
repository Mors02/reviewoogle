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
#   joy             1.3      1       0.9     0.8     0.7     0.6     0.6
#   
#   surprise        1        1.3     0.8     
#
#   neutral         0.9      0.8     1.3
#
#   anger           0.8      0.8     0.7
#
#   fear            0.7      0.9     0.7
#
#   sadness         0.6      0.7     0.
#   
#   disgust         0.6      0.6