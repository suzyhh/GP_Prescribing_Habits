#!/usr/bin/env python
# coding: utf-8

# In[87]:


import csv
import pandas as pd
import matplotlib.pyplot as pyplot
get_ipython().run_line_magic('matplotlib', 'inline')


# In[88]:


def readfile(file):
    df=pd.read_csv(file)


# In[89]:


df=pd.read_csv("items for penicillins per 1,000 patients on list.csv")

#remove rows that have 0 patients
df_patients=df[df["total_list_size"]!=0].copy()

#assign GPs with no patients to naGPs
naGPs=df[df["total_list_size"]==0].copy()


# In[90]:


df_patients['normalisation']=df_patients['y_items'] / df_patients['total_list_size']
#df_timeseries=df_patients.copy()
#df_timeseries['date'] = pd.to_datetime(df_patients.date, format = '%d/%m/%Y')


# In[106]:


df_by_date_mean=df_patients.groupby("date")["normalisation"].mean()
df_by_date_std=df_patients.groupby("date")["normalisation"].std()


# In[107]:


df_by_date_mean  = df_by_date_mean.rename('mean')


# In[109]:


mean_dict = df_by_date_mean.to_dict() 
std_dict = df_by_date_std.to_dict()


# In[110]:


df_patients['std'] = df_patients['date'].map(std_dict)
df_patients['mean'] = df_patients['date'].map(mean_dict)
df_patients['z'] = (df_patients['normalisation']-df_patients['mean'])/df_patients['std']


# In[112]:


outliers1 = df_patients[(df_patients['z'] >= 2)].copy() 
outliers2 = df_patients[(df_patients['z'] <= -2)].copy()


# In[113]:


#need to convert to timeseries
#df2['date'] = pd.to_datetime(df2.date, format = '%d/%m/%Y')
#df_by_date_mean = pd.to_datetime(df2.date, format = '%d/%m/%Y')
outliers1['date'] = pd.to_datetime(df_patients.date, format = '%d/%m/%Y')
outliers2['date'] = pd.to_datetime(df_patients.date, format = '%d/%m/%Y')


# In[99]:


df_by_date_std=df_patients.groupby("date")["normalisation"].std()
meanstd_plus=df_by_date_mean + df_by_date_std
meanstd_minus=df_by_date_mean - df_by_date_std


# In[128]:


summary_data = pd.concat([df_by_date_mean,meanstd_minus, meanstd_plus], axis=1)


# In[129]:


summary_data=summary_data.rename(columns={0:"mean - std",1:"mean + std"})


# In[133]:


summary_data.index=pd.to_datetime(summary_data.index,format='%d/%m/%Y')


# In[149]:


#outliers1.plot(kind="scatter",x="date",y='z',color='red')


# In[182]:



pyplot.plot_date(summary_data.index,summary_data["mean"],c="blue")
pyplot.plot_date(summary_data.index,summary_data["mean + std"],c="green")
pyplot.plot_date(summary_data.index,summary_data["mean - std"],c="green")
pyplot.plot_date(outliers1["date"],outliers1["normalisation"],c="red")
pyplot.plot_date(outliers2["date"],outliers2["normalisation"],c="red")


# In[176]:


pyplot.plot(summary_data)


# In[167]:


summary_data


# In[ ]:




