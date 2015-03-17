
# coding: utf-8

# In[1]:

import csv
import os
import pandas as pd
import numpy as np
import timeit

start = timeit.default_timer()

#-------------------------User Input--------------------------------------------------------------------
user = 'sbliefnick'
kind = 'Current'
#-------------------------User Input--------------------------------------------------------------------

folder = 'C:\Users\%s\Desktop\%s Exports' % (user,kind)
saveTo = 'C:\Users\%s\Desktop\%s MAF\Response Table.csv' % (user,kind)

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
            
#define the function that will help us isolate item IDs from the column headers
def getItemId(headerName):
    """Assumes headerName is a column header string in a data export that contains the 
    item ID along the form (Cycle)_(ItemID)_(ItemPosition)
    Returns just the item ID as an int"""

    headerName = str(headerName.split('_')[1])

    return headerName
#--------------------------------------------------------------------------------------------------------

#read in files

allFiles = list_files(folder)

#master DF to hold all info
responseTable = pd.DataFrame()

fileCount = 0

for file in allFiles:
    fileCount += 1
    print(file)
     # get rid of unnecessary headers
    df = pd.read_csv(file, header=3, na_values=['null', 'N/A'])
    
    # get rid of extra column if necessary
    if 'Unnamed: ' in df.columns[-1]:
        df = df.iloc[:,:-1]
    
    #figure out the number of questions
    numQ = (len(df.columns) - 34) / 2
    
    #trim the column headers to be just item IDs
    for col in df.iloc[0:0,34:]:
        df.rename(columns={col: getItemId(col)}, inplace=True)
        
    #get the item IDs into a list for later
    items = df.iloc[0:0,34:]
    itemIDs = list(set(items.columns.values))
    
    #get the student IDs
    studentIDs = df.iloc[:,6:7]
    
    #put the item scores into a dataframe and insert student IDs
    itemScores = df.iloc[:,34:(34+numQ)]
    itemScores.insert(0, "Student ANET ID", studentIDs)
    
    #melt the item scores, sort by student ID and then item ID, and get rid of duplicates
    itemScoresMelted = pd.melt(itemScores, id_vars=['Student ANET ID'], value_vars=itemIDs)
    itemScoresMelted.sort(columns=['Student ANET ID', 'variable'], inplace=True)
    
    #put the item responses into a dataframe and insert student IDs
    itemResponses = df.iloc[:,(34+numQ):]
    itemResponses.insert(0, "Student ANET ID", studentIDs)
    
    #melt the item Responses, sort by student ID and then item ID, and get rid of duplicates
    itemResponsesMelted = pd.melt(itemResponses, id_vars=['Student ANET ID'], value_vars=itemIDs)
    itemResponsesMelted.sort(columns=['Student ANET ID', 'variable'], inplace=True)
    
    #merge melted data frames
    newdf = pd.merge(itemScoresMelted, itemResponsesMelted,                      left_on=['Student ANET ID', 'variable'],                     right_on=['Student ANET ID', 'variable'])
    
    #rename column headers
    newdf.rename(columns={'variable': 'Item ID', 'value_x': 'Score', 'value_y': 'Response'}, inplace=True)
    
    #add subject column
    if ' ELA ' in file:
        newdf['Subject'] = 'ELA'
    elif ' Math ' in file:
        newdf['Subject'] = 'Math'
        
    #add cycle column
    if '-A1 ' in file:
        cycle = 'A1'
    elif '-A2 ' in file:
        cycle = 'A2'
    elif '-A3 ' in file:
        cycle = 'A3'
    elif '-A4 ' in file:
        cycle = 'A4'
    newdf['Cycle'] = cycle
    
    responseTable = responseTable.append(newdf)

responseTable.to_csv(saveTo, index=False)

stop = timeit.default_timer()

print(str(fileCount) + " files accessed. \n" + str(stop - start) + " seconds to complete.")


# In[ ]:



