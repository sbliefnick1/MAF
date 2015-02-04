
# coding: utf-8

# In[3]:

import csv
import pandas as pd
import numpy as np
import timeit

low_memory = False

start = timeit.default_timer()

user = 'sbliefnick'
readFrom = 'C:\\Users\\%s\\Desktop\\A2 MAF\\' % (user)
saveTo = 'C:\Users\%s\Desktop\A2 MAF\A2 MAF.csv' % (user)

assessmentIDsfile = readFrom + 'Assessment IDs.csv'
confidenceLevelsfile = readFrom + 'Confidence levels.csv'
EBSRinfofile = readFrom + 'EBSR info.csv'
itemsByPassagefile = readFrom + 'Items by Passage.csv'
mappingFilefile = readFrom + 'Mapping File Fixed.csv'
masterRosterfile = readFrom + 'Master Roster.csv'
responseTablefile = readFrom + 'Response Table.csv'
standardItemsfile = readFrom + 'Standard Items.csv'
standardsfile = readFrom + 'Standards.csv'

assessmentIDs = pd.read_csv(assessmentIDsfile, na_values=['null', 'N/A'])
confidenceLevels = pd.read_csv(confidenceLevelsfile, na_values=['null', 'N/A'])
EBSRinfo = pd.read_csv(EBSRinfofile, na_values=['null', 'N/A'])
itemsByPassage = pd.read_csv(itemsByPassagefile, na_values=['null', 'N/A'])
mappingFile = pd.read_csv(mappingFilefile, na_values=['null', 'N/A'])
masterRoster = pd.read_csv(masterRosterfile, na_values=['null', 'N/A'])
responseTable = pd.read_csv(responseTablefile, na_values=['null', 'N/A'])
standardItems = pd.read_csv(standardItemsfile, na_values=['null', 'N/A'])
standards = pd.read_csv(standardsfile, na_values=['null', 'N/A'])

#Merge 1
masterDF = pd.merge(masterRoster, responseTable, how='inner', on=['Cycle', 'Student ANET ID', 'Subject'], sort=False)

#reset used dfs to clear memory
del masterRoster
del responseTable

#Merge 2
masterDF = pd.merge(masterDF, mappingFile, how='inner', on=['Cycle', 'Interim Grade', 'School ID', 'Subject'], sort=False)

del mappingFile

#Merge 3
masterDF = pd.merge(masterDF, assessmentIDs, how='inner', on=['Assessment ID', 'Cycle', 'Interim Grade', 'Subject'], sort=False)

del assessmentIDs

#Merge 4
itemDF = pd.merge(itemsByPassage, EBSRinfo, how='left', on=['Item ID'], sort=False)

del itemsByPassage
del EBSRinfo

#Merge 5
standardsDF = pd.merge(standardItems, standards, how='left', on=['Common Core ID'], sort=False)

del standardItems
del standards

#Merge 6
subDF = pd.merge(standardsDF, itemDF, how='left', on=['Item ID'], sort=False)

del standardsDF
del itemDF

#Merge 7
masterDF = pd.merge(masterDF, subDF, how='left', on=['Interim Grade', 'Item ID'], sort=False)

del subDF

#Merge 8
masterDF =pd.merge(masterDF, confidenceLevels, how='left', on=['School ID', 'Cycle'], sort=False)

del confidenceLevels

masterDF.to_csv(saveTo, index=False)

stop = timeit.default_timer()

print(stop - start)


# In[ ]:



