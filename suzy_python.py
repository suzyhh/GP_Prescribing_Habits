#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import pandas as pd
import matplotlib.pyplot as pyplot
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


def readfile(file):
    df=pd.read_csv(file)


# In[3]:


df=pd.read_csv("items for penicillins per 1,000 patients on list.csv")


# In[4]:


df2=df[df["total_list_size"]!=0].copy()


# In[117]:


df2['normalisation']=df2['y_items'] / df2['total_list_size'] *1000


# In[119]:


df2['date'] = pd.to_datetime(df2.date, format = '%d/%m/%Y')


# In[120]:


df_by_date_mean=df2.groupby("date")["normalisation"].mean()


# In[121]:


def plotting(data):
    '''Function for plotting a line graph
    Data should be a table with date as the index and a column of data points'''
    data.plot()
    pyplot.show()

plotting(df_by_date_mean)


# In[122]:


df_by_date_std=df2.groupby("date")["normalisation"].std()


# In[124]:


df_by_date_std=df_by_date_std.rename("std")
df_by_date_mean=df_by_date_mean.rename("mean")


# In[125]:


summary_data = pd.concat([df_by_date_mean,(df_by_date_mean - (df_by_date_std*2)), (df_by_date_mean + (df_by_date_std*2))], axis=1)


# In[126]:


summary_data=summary_data.rename(columns={0:"mean - std",1:"mean + std"})


# In[128]:


plotting(summary_data)


# In[138]:


outliers=df2.groupby("date")["normalisation"]>0


# In[166]:


outlier=df2["normalisation"]>summary_data.iloc[0,2]
    


# In[173]:


if df2.groupby("date")["normalisation"] > df2.groupby("date")["normalisation"].std():
    print("bigger")


# In[203]:


df_by_date_mean['2014-10-01']


# In[ ]:




