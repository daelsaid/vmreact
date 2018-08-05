import pandas as pd
import os
import sys
from glob import glob
import numpy as np


data_dir='/Users/lillyel-said/Desktop/vmreact/vmreact/2_vmreact/'

cols=['date','subject', 'trial1','trial2','trial3','trial4','trial5','listb','trial6','trial7','total_learning','corrected_total_learning','learning_rate','proactive_interference','retroactive_interference','forgetting_and_retention']
trials=['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'listb', 'trial6', 'trial7']


for compiled_file in glob(os.path.join(data_dir,'mturk_vmreact_complete_compilation_initiation.csv')):
    vmreact_compiled=pd.read_csv(compiled_file,dtype=str,index_col=['gender','age_range'])
    bysubj=pd.read_csv(compiled_file,dtype='str')
    test_df=vmreact_compiled.loc[:,'list_type':'trial7_values.recall_lastcharlatency']
    for t in trials:
        for subj,subj_df in vmreact_compiled.groupby(level=[0,1]):
            if len(subj_df) >3:
                try:
                    response_latency=subj[0], subj[1],t+'_values.response_latency', round(subj_df[t+'_values.response_latency'].astype(float).mean(axis=0),4),round(subj_df[t+'_values.response_latency'].astype(float).std(axis=0),4),subj_df[t+'_values.response_latency'].count()
                    initiation=subj[0],subj[1], t+'_values.recall_firstcharlatency', round(subj_df[t+'_values.recall_firstcharlatency'].astype(float).mean(axis=0),4),round(subj_df[t+'_recency'].astype(float).std(axis=0),4),subj_df[t+'_recency'].count()
                    repeats=subj[0],subj[1],t+'_#_repeats',round(subj_df[t+'_#_repeats'].astype(float).mean(axis=0),4),round(subj_df[t+'_#_repeats'].astype(float).std(axis=0),4),subj_df[t+'_#_repeats'].count()
                    trials=subj[0],subj[1],t,round(subj_df[t].astype(float).mean(axis=0),4),round(subj_df[t].astype(float).std(axis=0),4),subj_df[t].count()
                    primacy=subj[0],subj[1],t+'_primacy',round(subj_df[t+'_primacy'].astype(float).mean(axis=0),4),round(subj_df[t+'_primacy'].astype(float).std(axis=0),4),subj_df[t+'_primacy'].count()
                    recency=subj[0],subj[1],t+'_recency',round(subj_df[t+'_recency'].astype(float).mean(axis=0),4),round(subj_df[t+'_recency'].astype(float).std(axis=0),4),subj_df[t+'_recency'].count()
                    composite=subj_df.loc[:,'total_learning':'forgetting_and_retention'].astype(float)
                    composite_vals=composite.mean(axis=0), composite.std(axis=0),composite.count()
                    comp=composite.mean(axis=0), composite.std(axis=0),composite.count()
                    # # print comp[2].T
                    # print repeats
                    # print response_latency
                    # print initiation
                    # print trials
                    # print primacy
                    # print recency
                except:
                    continue
                    #firstcharaverages
