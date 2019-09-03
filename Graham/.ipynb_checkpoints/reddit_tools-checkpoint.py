import pandas as pd
import seaborn as sns
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt

def import_csv_as_df(filename):
    df = pd.read_csv(filename)
    
    # make a new field with easier datetime, remove old field with utc format
    df['OPcreatedAt'] = pd.to_datetime(df['op_created_utc'], unit = 's')
    df = df.drop(columns=['op_created_utc'])
    df['createdAt'] = pd.to_datetime(df['created_utc'], unit = 's')
    df = df.drop(columns=['created_utc'])


    # remove data from before Election (Nov 9, 2016)
    election_date = '2016-11-09 00:00:00'
    df = df[df['createdAt']>election_date]

    # Remove all columns that are all NaN
    return df[df.columns[~pd.isna(df).all()]]
    
    
def get_time_window(df, t_start,t_end):
    
    
    t_start_str = '-'.join(list(map(str, t_start))) + ' 00:00:00'
    t_end_str = '-'.join(list(map(str, t_end))) + ' 00:00:00'    
    
    return df[(df['createdAt']>=t_start_str) & 
              (df['createdAt']<t_end_str)]

    
class OriginalPost:
    def __init__(self, original_post_df):
        self.child_comments = []
        self.timestamp
        

#class Comment:    




