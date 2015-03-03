
# coding: utf-8

# In[1]:

import csv
import pandas as pd
import numpy as np
import timeit
from datetime import datetime
low_memory = False
start = timeit.default_timer()

#--------------------------------User Input----------------------------------------
user = 'sbliefnick'
kind = 'Current'
includeSummative = False
#--------------------------------User Input----------------------------------------

now = datetime.now()
now = now.strftime('%m.%d.%y')
readFrom = 'C:\\Users\\%s\\Desktop\\%s MAF\\' % (user,kind)
saveTo = 'C:\Users\%s\Desktop\%s MAF\%s MAF %s.csv' % (user,kind,kind,now)

assessmentIDsfile = readFrom + 'Assessment IDs.csv'
confidenceLevelsfile = readFrom + 'Confidence levels.csv'
EBSRinfofile = readFrom + 'EBSR info.csv'
itemsByPassagefile = readFrom + 'Items by Passage.csv'
mappingFilefile = readFrom + 'Mapping File Fixed.csv'
masterRosterfile = readFrom + 'Master Roster.csv'
responseTablefile = readFrom + 'Response Table.csv'
standardItemsfile = readFrom + 'Standard Items.csv'
standardsfile = readFrom + 'Standards.csv'
if includeSummative == True:
    summativefile = readFrom + 'Summative.csv'

assessmentIDs = pd.read_csv(assessmentIDsfile, na_values=['null', 'N/A'])
confidenceLevels = pd.read_csv(confidenceLevelsfile, na_values=['null', 'N/A'])
EBSRinfo = pd.read_csv(EBSRinfofile, na_values=['null', 'N/A'])
itemsByPassage = pd.read_csv(itemsByPassagefile, na_values=['null', 'N/A'])
mappingFile = pd.read_csv(mappingFilefile, na_values=['null', 'N/A'])
masterRoster = pd.read_csv(masterRosterfile, na_values=['null', 'N/A'])
responseTable = pd.read_csv(responseTablefile, na_values=['null', 'N/A'])
standardItems = pd.read_csv(standardItemsfile, na_values=['null', 'N/A'])
standards = pd.read_csv(standardsfile, na_values=['null', 'N/A'])
if includeSummative == True:
    summative = pd.read_csv(summativefile, na_values=['null', 'N/A'])

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

#get rid of duplicates and add a column for true sequence
masterDF.drop_duplicates(subset=['Student ANET ID', 'Item ID'], inplace=True)
#masterDF['True Sequence'] = masterDF['Assessment State'] + " " + masterDF['Sequence']

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
masterDF = pd.merge(masterDF, confidenceLevels, how='left', on=['School ID'], sort=False)

del confidenceLevels

#Merge 9
if includeSummative == True:
    masterDF = pd.merge(masterDF, summative, how='left', on=['School ID'], sort=False)

    del summative


masterDF.to_csv(saveTo, index=False)

stop = timeit.default_timer()

print(str(stop - start) + " seconds to complete.")


# In[ ]:



