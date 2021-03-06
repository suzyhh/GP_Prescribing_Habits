#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as pyplot

# get_ipython().run_line_magic('matplotlib', 'inline')

# ask for a file to analyse and raise an exception if the file is not found in the working directory
# for testing, the filename is "items for penicillins per 1,000 patients on list.csv"
prescription_file = input("Enter the filename: ")
try:
    prescriptions_raw = pd.read_csv(prescription_file)
except FileNotFoundError:
    print("File does not exist, please enter a valid filename")

# remove rows that have 0 patients
prescriptions = prescriptions_raw[prescriptions_raw["total_list_size"] != 0].copy()

# assign GPs with no patients to naGPs
GP_no_patients = prescriptions_raw[prescriptions_raw["total_list_size"] == 0].copy()

# normalise the number of items per 1000 patients registered at the practice
prescriptions['normalisation'] = (prescriptions['y_items'] / prescriptions['total_list_size']) * 1000

# find mean and standard deviation for z-score calculation
mean_prescriptions_by_date = prescriptions.groupby("date")["normalisation"].mean()
std_prescriptions_by_date = prescriptions.groupby("date")["normalisation"].std()

# rename column
mean_prescriptions_by_date = mean_prescriptions_by_date.rename('mean')

# create dictionaries for mean and standard deviation so we can refer to values
mean_prescriptions_dict = mean_prescriptions_by_date.to_dict()
std_prescriptions_dict = std_prescriptions_by_date.to_dict()

# referring the dataframe of patients to the associated mean and std based on date
prescriptions['std'] = prescriptions['date'].map(std_prescriptions_dict)
prescriptions['mean'] = prescriptions['date'].map(mean_prescriptions_dict)
# calculating the z score
prescriptions['z'] = (prescriptions['normalisation'] - prescriptions['mean']) / prescriptions['std']

# finding outliers per month that are more than 2x the standard devations away from the mean
outliers_over = prescriptions[(prescriptions['z'] >= 2)].copy()
outliers_under = prescriptions[(prescriptions['z'] <= -2)].copy()

# convert to timeseries
# df2['date'] = pd.to_datetime(df2.date, format = '%d/%m/%Y')
# df_by_date_mean = pd.to_datetime(df2.date, format = '%d/%m/%Y')
outliers_over['date'] = pd.to_datetime(prescriptions.date, format='%d/%m/%Y')
outliers_under['date'] = pd.to_datetime(prescriptions.date, format='%d/%m/%Y')

meanstd_plus = mean_prescriptions_by_date + std_prescriptions_by_date
meanstd_minus = mean_prescriptions_by_date - std_prescriptions_by_date

# create dataframe with the mean and the standard devations
prescription_summary = pd.concat([mean_prescriptions_by_date, meanstd_minus, meanstd_plus], axis=1)

# rename columns with meaningful headings
prescription_summary = prescription_summary.rename(columns={0: "mean - std", 1: "mean + std"})

# convert date index to timeseries
prescription_summary.index = pd.to_datetime(prescription_summary.index, format='%d/%m/%Y')

# sort the timeseries
sorted_summary = prescription_summary.sort_index()

# plotting the mean and standard deviation from summary data and then overlay with the outliers
[mean, plus, minus] = pyplot.plot(sorted_summary)
pyplot.plot_date(outliers_over["date"], outliers_over["normalisation"], c="red", markersize=3)
[outlier] = pyplot.plot_date(outliers_under["date"], outliers_under["normalisation"], c="red", markersize=3)
pyplot.xlabel('Year')
pyplot.tick_params(axis='x', rotation=45)
pyplot.ylabel('Prescriptions (per 1000 patients)')
pyplot.legend([mean, plus, minus, outlier], ["mean", "mean-1 stdev", "mean+1 stdev", "outliers"])
pyplot.show()

# find which GP in which month prescribed the most items
highest_prescription = outliers_over[outliers_over['normalisation'] == outliers_over['normalisation'].max()]
print("The most prescriptions were made by{} who prescribed{} items per 1000 patients in {}"
      .format(highest_prescription["name"].to_string(index=False, header=False), highest_prescription["normalisation"]
              .to_string(index=False, header=False), highest_prescription["date"].to_string(index=False, header=False)))

# find mean for each GP practice over all time
practices = prescriptions.groupby("name")["normalisation"].mean()

# find overall mean and standard deviation to identify outliers
practices_mean = practices.mean()
practices_std = practices.std()

# find GP practices that have a mean prescription level of more than 2 stds above the mean
prac_outliers = practices > (practices_mean + (practices_std * 2))

# which GP practices are outliers?
overall_outliers = prac_outliers[prac_outliers == True]
print(
    "The following surgeries have consistently high prescribing (more than 2 standard deviations above the mean over all time): "
    "\n {}, {}, {}".format(overall_outliers.index[0], overall_outliers.index[1], overall_outliers.index[2]))

# GP practice with the highest mean prescribing
gp_with_highest_mean = practices[practices == practices.max()]
# print gp and month of highest prescribing
print(gp_with_highest_mean.index[0], "has the highest overall mean prescribing of",
      gp_with_highest_mean[0], "per 1,000 patients")

# pull out the month by month data for the GP surgery with the highest mean prescribing
highest_gp_by_date = prescriptions[prescriptions['name'].str.match(gp_with_highest_mean.index[0])]
highest_gp_by_date.date = pd.to_datetime(highest_gp_by_date.date, format='%d/%m/%Y')

# now we have the GP with the highest mean prescribing, plot it compared to the mean/std of all GPs to assess
# if it is an ongoing trend for this GP surgery or driven by a few extreme datapoints
[mean, plus, minus] = pyplot.plot(sorted_summary)
[highest] = pyplot.plot_date(highest_gp_by_date["date"], highest_gp_by_date["normalisation"], linestyle="solid",
                             markersize=0)
pyplot.xlabel('Year', rotation=0)
pyplot.tick_params(axis='x', rotation=45)
pyplot.ylabel('Prescriptions (per 1000 patients)')
pyplot.legend([mean, plus, minus, highest], ["mean", "mean-1 stdev", "mean+1 stdev", gp_with_highest_mean.index[0]])
pyplot.show()


def plot_a_practice(GP_practice):
    """Plotting the prescribing of a single GP surgery compared to the mean/std of all surgerys
    A match will be made from an incomplete input and is case insensitive (e.g. "hawthorn" will match to "HAWTHORN MC")
    """
    practice_details = prescriptions[prescriptions['name'].str.match(pat=".*{}.*".format(GP_input_file), case=False)]
    print("GP surgery selected: ", practice_details.iloc[0, 2])
    practice_details.date = pd.to_datetime(practice_details.date, format='%d/%m/%Y')
    [mean, plus, minus] = pyplot.plot(sorted_summary)
    [highest] = pyplot.plot_date(practice_details["date"], practice_details["normalisation"], linestyle="solid",
                                 markersize=0)
    pyplot.xlabel('Year', rotation=0)
    pyplot.tick_params(axis='x', rotation=45)
    pyplot.ylabel('Prescriptions (per 1000 patients)')
    pyplot.legend([mean, plus, minus, highest], ["mean", "mean-1 stdev", "mean+1 stdev", practice_details.iloc[0, 2]])
    pyplot.show()


def check_gp_lookup(GP_practice):
    """Check valid GP practice is found"""
    practice_details = prescriptions[prescriptions['name'].str.match(pat=".*{}.*".format(GP_input_file), case=False)]
    if len(practice_details) == 0:
        raise NameError
    global uniq_lst
    uniq_lst = []
    for surgery in practice_details["name"]:
        if surgery not in uniq_lst:
            uniq_lst.append(surgery)
    if len(uniq_lst) > 1:
        raise LookupError


GP_input_file = input("Enter the GP practice: ")

while True:
    try:
        check_gp_lookup(GP_input_file)
        plot_a_practice(GP_input_file)
        break
    except LookupError:
        print("more than one GP has been selected, please be more specific:", uniq_lst)
        GP_input_file = input("Enter the GP practice: ")
    except NameError:
        print("GP surgery does not exist, please enter a valid GP")
        GP_input_file = input("Enter the GP practice: ")
