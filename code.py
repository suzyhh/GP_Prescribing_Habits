import csv
import pandas as pd
import matplotlib.pyplot as pyplot

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

df=df.rename(columns={0:"date",6:"normalisation"})
df['date'] = pd.to_datetime(df.date, format = '%d/%m/%Y')

df_by_date=df.groupby("date")
#df_by_date.get_group("2014-10-01")

df_by_date_mean=df.groupby("date")["normalisation"].mean()
df_by_date_mean['2016-10-01']

df_by_date_mean.plot()
pyplot.show()
#pyplot.plot(df_by_date_mean)
#pyplot.show()
