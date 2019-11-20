import csv
import pandas as pd

with open("items for penicillins per 1,000 patients on list.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    normalisation = []
    fourteen=[]
    table=[]
    for row in readCSV:
        if row[3] == 'y_items' or row[5] == '0':
            continue
        else:
            row.append(int(row[3])/int(row[5]))
            table.append(row)
df=pd.DataFrame(table)
print(df)
