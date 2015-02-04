
# coding: utf-8

# In[17]:

import csv
import pandas as pd
import numpy as np

user = 'sbliefnick'

file = 'C:\Users\%s\Desktop\MAF test\Mapping File.csv' % (user)
mappingFileInitial = pd.read_csv(file, usecols = ['School id', 'Interim Grade', 'Course', 'Assessment Id', 'Cycle'])
mappingFileInitial.rename(columns={'School id': 'School ID', 'Course': 'Subject', 'Assessment Id': 'Assessment ID'}, inplace=True)
mappingFileInitial.replace(to_replace='MATH', value='Math', inplace=True)

saveTo = 'C:\Users\%s\Desktop\MAF test\Mapping File Fixed.csv' % (user)
mappingFileInitial.to_csv(saveTo, index=False)

