import csv
import pandas as pd
import matplotlib.pyplot as pyplot
get_ipython().run_line_magic('matplotlib', 'inline')

def readfile(file):
    df=pd.read_csv(file)

df=pd.read_csv("items for penicillins per 1,000 patients on list.csv")
df2=df[df["total_list_size"]!=0].copy()
naGPs=df[df["total_list_size"]==0].copy()


df2['normalisation']=df2['y_items'] / df2['total_list_size']
df3=df2.copy()
df3['date'] = pd.to_datetime(df2.date, format = '%d/%m/%Y')

naGPs

df_by_date_mean=df3.groupby("date")["normalisation"].mean()
df_by_date_std=df3.groupby("date")["normalisation"].std()

df_by_date_mean  = df_by_date_mean.rename('mean')

mean_dict = df_by_date_mean.to_dict() 
std_dict = df_by_date_std.to_dict()

df2['std'] = df2['date'].map(std_dict)
df2['mean'] = df2['date'].map(mean_dict)
df2['z'] = (df2['normalisation']-df2['mean'])/df2['std']

outliers1 = df2[(df2['z'] >= 2)].copy() 
outliers2 = df2[(df2['z'] <= -2)].copy()

#need to convert to timeseries
#df2['date'] = pd.to_datetime(df2.date, format = '%d/%m/%Y')
#df_by_date_mean = pd.to_datetime(df2.date, format = '%d/%m/%Y')
outliers1['date'] = pd.to_datetime(df2.date, format = '%d/%m/%Y')
outliers2['date'] = pd.to_datetime(df2.date, format = '%d/%m/%Y')


df_by_date_std=df2.groupby("date")["normalisation"].std()
meanstd_plus=df_by_date_mean + df_by_date_std
meanstd_minus=df_by_date_mean - df_by_date_std


meanstd_minus = meanstd_minus.rename('mean - std')

meanstd_plus = meanstd_plus.rename('mean + std')

summary_data = pd.concat([df_by_date_mean,meanstd_minus, meanstd_plus], axis=1)

#plotting
def plotting(data):
    '''Function for plotting a line graph
    Data should be a table with date as the index and a column of data points'''
    data.plot()
    pyplot.show()

plotting(df_by_date_mean)

plotting(summary_data)
