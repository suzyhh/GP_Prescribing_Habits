import csv
import pandas as pd
import matplotlib.pyplot as pyplot
%matplotlib inline


def readfile(file):
df=pd.read_csv(file)
    
df=pd.read_csv("items for penicillins per 1,000 patients on list.csv")
df2=df[df["total_list_size"]!=0].copy()

df2['normalisation']=df2['y_items'] / df2['total_list_size']
df2['date'] = pd.to_datetime(df2.date, format = '%d/%m/%Y')
df_by_date_mean=df2.groupby("date")["normalisation"].mean()
def plotting(data):
    '''Function for plotting a line graph
    Data should be a table with date as the index and a column of data points'''
    data.plot()
    pyplot.show()

plotting(df_by_date_mean)

df_by_date_std=df2.groupby("date")["normalisation"].std()
meanstd_plus=df_by_date_mean + df_by_date_std
meanstd_minus=df_by_date_mean - df_by_date_std
