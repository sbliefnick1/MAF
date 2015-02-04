
# coding: utf-8

# In[1]:

import csv
import pandas as pd
import os                                                                                                             

user = 'sbliefnick'
folder = 'C:\Users\%s\Desktop\Aggregated Data Exports' % (user)
saveTo = 'C:\Users\%s\Desktop\MAF Test\Standard Items.csv' % (user)

#-------------functions------------------------------------------------------------
def list_files(dir):                                                                                                  
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).next()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file in files:                                                                                        
                r.append(subdir + "/" + file)                                                                         
    return r                                 

def common_core_id_sep(x):
    n = x.split(" ")
    return n[0]

def item_id_sep(x):
    n = x.split("_")
    return n[1]
#--------------------------------------------------------------------------------------


allFiles = list_files(folder)

final_item_df = pd.DataFrame(columns=['Standard', 'Item Type', 'Total Points Possible', 'Item ID', 'Common Core ID'])
for file in allFiles: 
    print(file)
    df = pd.read_csv(file, nrows=4,header=None) 
    
    for x in range (0, 33): #delete the first 33 columns (columns 0-32) 
        del df[x]
    
    newdf = df.transpose()  #transpose shortened dataframe

    newdf.columns = newdf.iloc[0] #set first row as the column header

    newdf = newdf.drop(newdf.index[:1]) #delete that row

    newdf = newdf.dropna() #drop any NaNs

    if '-A1 ' in file:
        newdf.rename(columns={'A1 Points Possible':'Item ID'}, inplace=True) # rename column
    elif '-A2 ' in file:
        newdf.rename(columns={'A2 Points Possible':'Item ID'}, inplace=True)
    elif '-A3 ' in file:
        newdf.rename(columns={'A3 Points Possible':'Item ID'}, inplace=True)
    elif '-A4 ' in file:
        newdf.rename(columns={'A4 Points Possible':'Item ID'}, inplace=True)

    newdf['Common Core ID'] = newdf['Standard'].map(common_core_id_sep)
    newdf['Item ID'] = newdf['Item ID'].map(item_id_sep)

    newdf = newdf.drop_duplicates(subset='Item ID') #drop duplicates within each file to get 

    final_item_df = pd.concat([final_item_df, newdf])
    
final_item_df = final_item_df.drop_duplicates(subset='Item ID') #drop duplicates within each file to get 
#del final_item_df['Standard'] 
#final_item_df


final_item_df.to_csv(saveTo, index=False)


# In[ ]:



