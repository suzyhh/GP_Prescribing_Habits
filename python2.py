#!/usr/bin/env python
# coding: utf-8

# In[335]:

import pandas as pd
import matplotlib.pyplot as pyplot

# get_ipython().run_line_magic('matplotlib', 'inline')
fhds jfh sjk

# In[337]:

prescriptions_raw = pd.read_csv("items for penicillins per 1,000 patients on list.csv")

# remove rows that have 0 patients
prescriptions = prescriptions_raw[prescriptions_raw["total_list_size"] != 0].copy()

# assign GPs with no patients to naGPs
GP_no_patients = prescriptions_raw[prescriptions_raw["total_list_size"] == 0].copy()

# In[338]:

# normalise the number of items per 1000 patients registered at the practice
prescriptions['normalisation'] = (prescriptions['y_items'] / prescriptions['total_list_size']) * 1000

# In[339]:

# find mean and standard deviation for z-score calculation
mean_prescriptions_by_date = prescriptions.groupby("date")["normalisation"].mean()
std_prescriptions_by_date = prescriptions.groupby("date")["normalisation"].std()

# In[340]:

# rename column
mean_prescriptions_by_date = mean_prescriptions_by_date.rename('mean')

# In[341]:

# create dictionaries for mean and standard deviation so we can refer to values
mean_prescriptions_dict = mean_prescriptions_by_date.to_dict()
std_prescriptions_dict = std_prescriptions_by_date.to_dict()

# In[342]:

# referring the dataframe of patients to the associated mean and std based on date
prescriptions['std'] = prescriptions['date'].map(std_prescriptions_dict)
prescriptions['mean'] = prescriptions['date'].map(mean_prescriptions_dict)
# calculating the z score
prescriptions['z'] = (prescriptions['normalisation'] - prescriptions['mean']) / prescriptions['std']

# In[343]:


# finding outliers per month that are more than 2x the standard devations away from the mean
outliers_over = prescriptions[(prescriptions['z'] >= 2)].copy()
outliers_under = prescriptions[(prescriptions['z'] <= -2)].copy()

# In[344]:


# need to convert to timeseries
# df2['date'] = pd.to_datetime(df2.date, format = '%d/%m/%Y')
# df_by_date_mean = pd.to_datetime(df2.date, format = '%d/%m/%Y')
outliers_over['date'] = pd.to_datetime(prescriptions.date, format='%d/%m/%Y')
outliers_under['date'] = pd.to_datetime(prescriptions.date, format='%d/%m/%Y')

# In[364]:
meanstd_plus = mean_prescriptions_by_date + std_prescriptions_by_date
meanstd_minus = mean_prescriptions_by_date - std_prescriptions_by_date

# create dataframe with the mean and the standard devations
prescription_summary = pd.concat([mean_prescriptions_by_date, meanstd_minus, meanstd_plus], axis=1)

# In[365]:


# rename columns with meaningful headings
prescription_summary = prescription_summary.rename(columns={0: "mean - std", 1: "mean + std"})

# In[366]:


# convert date index to timeseries
prescription_summary.index = pd.to_datetime(prescription_summary.index, format='%d/%m/%Y')

# In[368]:


# sort the timeseries
sorted_summary = prescription_summary.sort_index()

# In[369]:


# plotting the mean and standard deviation from summary data and then overlay with the outliers
[mean,plus,minus] = pyplot.plot(sorted_summary)
pyplot.plot_date(outliers_over["date"], outliers_over["normalisation"], c="red", markersize=3)
[outlier] = pyplot.plot_date(outliers_under["date"], outliers_under["normalisation"], c="red", markersize=3)
pyplot.xlabel('Year')
pyplot.ylabel('Prescriptions (per 1000 patients)')
pyplot.legend([mean,plus,minus, outlier], ["mean", "mean-1 stdev", "mean+1 stdev", "outliers"])
pyplot.show()

# In[370]:

# find the highest prescription for all months for all GP practices
outliers_over[outliers_over['normalisation'] == outliers_over['normalisation'].max()]

# In[371]:

# find mean for each GP practice over all time
practices = prescriptions.groupby("name")["normalisation"].mean()

# In[310]:

# find overall mean and standard deviation to identify outliers
practices_mean = practices.mean()
practices_std = practices.std()

# In[354]:


# find GP practices that have a mean prescription level of more than 2 stds above the mean
prac_outliers = practices > (practices_mean + (practices_std * 2))

# In[355]:


prac_outliers

# In[ ]:
