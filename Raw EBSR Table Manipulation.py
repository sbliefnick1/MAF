
# coding: utf-8

# In[2]:

import csv
import pandas as pd
import numpy as np

# read in EBSR file
rawEBSR = pd.read_csv('C:/Users/sbliefnick/Desktop/EBSR_Questions.csv')

partA = rawEBSR.iloc[:,:1]
partB = rawEBSR.iloc[:,1:]
partA['EBSR Part'] = 'Part A'
partB['EBSR Part'] = 'Part B'
partA['EBSR Item Partner'] = partB.iloc[:,:1]
partB['EBSR Item Partner'] = partA.iloc[:,:1]
partA.rename(columns={'part_a_question_id': 'Item ID'}, inplace=True)
partB.rename(columns={'part_b_question_id': 'Item ID'}, inplace=True)
combined = pd.concat([partA, partB])
combined.to_csv("C:\\Users\\sbliefnick\\Desktop\\EBSR Info.csv", index=False)

