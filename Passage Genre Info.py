
# coding: utf-8

# In[3]:

import csv
import os
import pandas as pd
import numpy as np

user = 'sbliefnick'
folder = 'C:\Users\%s\Desktop\Distractor Guides' % (user)
saveTo = 'C:\Users\%s\Desktop\ELA MAF\Items by Passage.csv' % (user)

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
#---------------------------------------------------------------------------------------------------------

allFiles = list_files(folder)

#master data frame to contain all scores
masterDF = pd.DataFrame()

for file in allFiles:
    print(file)
    
    df = pd.read_csv(file, usecols=[1,2,3])
    df.rename(columns={'Item Code for Data Sets': 'Item ID', 'Passage\n(Lexile)': 'Passage'}, inplace=True)
    df['Passage'] = df['Passage'].map(lambda x: x.lstrip('').rstrip('(N/A1234567890 )\n'))
    df['Item ID'] = df['Item ID'].map(lambda x: x.split('_')[1])
    masterDF = masterDF.append(df)
    
masterDF.drop_duplicates(subset=['Item ID'], inplace=True)    
masterDF.to_csv(saveTo, index=False)


# In[ ]:



