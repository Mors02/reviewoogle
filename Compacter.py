from config import filename, compact
import csv

def toStringCSV(row):
    if (',' in row[1] and ',' in row[2]):
        return f'{row[0]},\"{row[1]}\",\"{row[2]}\",{row[3]},{row[4]}\n'
    if (',' in row[1]):
        return f'{row[0]},\"{row[1]}\",{row[2]},{row[3]},{row[4]}\n'
    if (',' in row[2]):
        return f'{row[0]},{row[1]},\"{row[2]}\",{row[3]},{row[4]}\n'
    return f'{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}\n'

with open(compact, 'w') as dest:
    maxRecordsPerGame = 500
    currentTitle = None
    i = 1
    
    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if (i < maxRecordsPerGame and currentTitle == row[1] and row[1] != ""):
                i = i + 1
                dest.write(toStringCSV(row))
            elif (currentTitle != row[1] and row[1] != ""):
                i = 1
                currentTitle = row[1]
                dest.write(toStringCSV(row))