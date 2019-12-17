# python

This code is used to investigate the prescribing habits of Manchester CCG GP practices for antibiotics.

The example used is penicillins.

To download data of your choice, please navigate to OpenPrescribing.net and download the data as a csv file, as follows:

Analyse -> see the prescribing of: "drugs or BNF sections" -> type in name of antibiotic (e.g. penicillins) versus: "total list size" highlighting: "a practice or practices" -> "NHS MANCHESTER CCG" -> Show me the data! -> Items for penicillins by practices in NHS MANCHESTER CCG -> Download CSV

The code will ask for the name of the csv file containing the data, and will output some statistic regarding prescribing habits, including plotting outliers on a month-by-month basis, and printing the GP practices with persistently high prescribing habits. 

The practice with the highest prescribing will be plotted against the overall mean for all practices.

The plot_a_practice(GP_practice) function take a string input and will plot the prescribing over time for that GP compared to the overall mean of all GPs. This function will try to make a match using an incomplete or partial string input. e.g. "Enter the GP practice: fallowfield" will plot data from "FALLOWFIELD MEDICAL CENTRE"
