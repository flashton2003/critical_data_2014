critical_data_2014
==================

As part of the critical data 2014 hackday I thought I would have a look at some data from a previous event. As I won't use the MIMIC dataset again, I wasn't keen to spend a long time getting the ethics permission to access it, would rather just hack!

This is my code from the first day. It essentially consists of a PatientRecord class which is filled with information from the publically available (and very nicely formatted!) data available here http://physionet.org/challenge/2012/ (also in the git repo). There is longitudinal data on 2000 peoples vital statitistics (blood pressure, urine production etc) over 48 hours in intensive care. There is also outcomes for each of those people (length of hospital stay, death etc). The PatientRecord class slurps up some of this info and then there are some functions to visualise the data using matplotlib. One of the nice things about this is that I could collaborate with someone who hsa MIMIC access to plug some of that data into the same class so the same functions will be able to visualise that data.

Today I will either extend the visualisation stuff and put it in a ipynb or try and do some more analytical stuff looking at blood pressure trajectory and mortality.
