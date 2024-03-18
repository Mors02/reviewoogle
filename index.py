import csv
from Preprocesser import process
from transformers import pipeline

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

filename = './dataset/compact_dataset.csv'

#df = pd.read_csv()

# OPEN THE CSV FILE AND READ EACH LINE
with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        #PREPROCESS
        processed_data = process(row)
        #print(processed_data)
        #CREATE THE SENTIMENT ANALYSIS


        #SAVE THE DOCUMENT
