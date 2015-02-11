
# coding: utf-8

# In[2]:

import csv
import os
import pandas as pd
import numpy as np

#-------------------------User Input--------------------------------------------------------------------
user = 'sbliefnick'
kind = 'Math'
#-------------------------User Input--------------------------------------------------------------------

folder = 'C:\Users\%s\Desktop\%s Exports' % (user,kind)
saveTo = 'C:\Users\%s\Desktop\%s MAF\Master Roster.csv' % (user,kind)

#-----------functions-----------------------------------------------------------------------------------
def list_files(dir):
    '''Given a filepath, walks through the directories and appends all filenames to a list.'''
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).next()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file in files:                                                                                        
                r.append(subdir + "/" + file)                                                                         
    return r  
            
def set_column_sequence(dataframe, seq):
    '''Takes a dataframe and a subsequence of its columns, returns dataframe with seq as first columns'''
    cols = seq[:] # copy so we don't mutate seq
    for x in dataframe.columns:
        if x not in cols:
            cols.append(x)
    return dataframe[cols]
#---------------------------------------------------------------------------------------------------------


allFiles = list_files(folder)

#master data frame to contain all scores
masterRoster = pd.DataFrame()

for file in allFiles:
    print(file)
    
    if ' ELA ' in file:
        subject = 'ELA'
    elif ' Math ' in file:
        subject = 'Math'
        
    proficiency = subject + ' Previous State Level'
    period = subject + ' Period'
    teacherFN = subject + ' Teacher First Name'
    teacherLN = subject + ' Teacher Last Name'
    
    
    # get rid of unnecessary headers; only read in relevant columns
    df = pd.read_csv(file, header=3, usecols=['School ANET ID', 'School Name', 'State', 'District', 'Cluster',                                               'Student ANET ID', 'Interim Grade', 'Race', 'Free Reduced Lunch',                                               'Limited English Proficiency', 'Special Education',                                               proficiency, period, teacherFN, teacherLN],                             na_values=['null', 'N/A'])
    
    #add in a column for Subject
    df['Subject'] = subject
    
    #add in a column for Cycle
    if '-A1 ' in file:
        cycle = 'A1'
    elif '-A2 ' in file:
        cycle = 'A2'
    elif '-A3 ' in file:
        cycle = 'A3'
    elif '-A4 ' in file:
        cycle = 'A4'
    df['Cycle'] = cycle
        
    masterRoster = masterRoster.append(df)

#rename some columns
masterRoster.rename(columns={'School ANET ID': 'School ID', 'State': 'Network State', 'Cluster': 'District Cluster'}, inplace=True)
    
#rearrange column order
preferredColumns = ['School ID', 'School Name', 'Network State', 'District', 'District Cluster',                     'Student ANET ID', 'Interim Grade', 'Subject', 'Cycle', 'Race', 'Free Reduced Lunch',                     'Limited English Proficiency', 'Special Education']

masterRoster = set_column_sequence(masterRoster, preferredColumns)


masterRoster.to_csv(saveTo, index=False)


# In[ ]:



