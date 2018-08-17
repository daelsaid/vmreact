# coding: utf-8

# In[ ]:

# import os
# import numpy as np
# import pandas as pd
# import csv
# from glob import glob


# In[ ]:

# data_dir='/Users/lillyel-said/Desktop/vmreact/vmreact/1_rawdata/data/'
# output_dir='/Users/lillyel-said/Desktop/vmreact/vmreact/1_rawdata/data/'


# In[ ]:

# trials=['trial1','trial2','trial3','trial4','trial5','listb','trial6','trial7']

# cols=['values.response_latency', 'expressions.trial_recall_word_latency',
#       'values.recall_firstcharlatency', 'values.recall_lastcharlatency']

# column_titles=['subjid','date']

# for trial in trials:
#     for meas in cols:
#         column_titles.append(trial+"_"+meas)

# final_csv=[column_titles]


# In[ ]:

# total_columns=[]
# for data_file in glob(os.path.join(data_dir,'*')):

#     data_df=pd.read_csv(data_file,dtype=str)
#     data_df.loc[data_df['response']==' ','trialcode'] = 'trial_confirmation'

#     for trial in ['trial1','trial2','trial3','trial4','trial5','trial6','trial7','trial8','listb']:
#         data_df.loc[data_df['trialcode'].str.contains(trial),'trialcode']=trial

#     data_df.rename(columns
#                    ={'latency':'values.response_latency'},inplace=True)

#     for col in data_df.columns.tolist():
#         if col not in total_columns:
#             total_columns.append(col)
# print sorted(total_columns)


# In[ ]:

# for data_file in glob(os.path.join(data_dir,'*.csv')):

#     data_df=pd.read_csv(data_file,dtype=str)
#     data_df.loc[data_df['response']==' ','trialcode'] = 'trial_confirmation'

#     for trial in ['trial1','trial2','trial3','trial4','trial5','trial6','trial7','trial8','listb']:
#         data_df.loc[data_df['trialcode'].str.contains(trial),'trialcode']=trial

#     data_df.rename(columns={'latency':'values.response_latency'},inplace=True)

#     subj_list=data_df.loc[data_df['trialcode'] == 'trial8','subject'].unique()
#     if len(subj_list) > 0: 
#         data_df.loc[(data_df['trialcode'] == 'trial6') & (data_df['subject'].isin(subj_list)),'trialcode']='listb'
#         data_df.loc[(data_df['trialcode'] == 'trial7') & (data_df['subject'].isin(subj_list)),'trialcode']='trial6'
#         data_df.loc[(data_df['trialcode'] == 'trial8') & (data_df['subject'].isin(subj_list)),'trialcode']='trial7'

#     for subj,subj_df in data_df.groupby(['subject']):
#         measures=[]
#         for trial,trial_df in subj_df.groupby(['trialcode']):
#             if trial in ['trial1','trial2','trial3','trial4','trial5','listb','trial6','trial7']:
#                 trial_measures=[np.nan]*4
#                 for idx,meas in enumerate(cols):
#                     try:
#                         trial_measures[idx]=round(trial_df[meas].astype('float').mean(),4)
#                         xnew[trial+'_'+meas]=trial_df['values.response_latency']

# for t in trials:
#     [t+'_initiation_latency']=all_data[t+'_values.response_latency'].subtract(all_data[t+'_values.recall_firstcharlatency'])

#                     except:
#                         trial_measures[idx]=np.nan
#                         continue
#         break
#                 measures.append([trial] + trial_measures)
#             elif trial == 'trial_confirmation':
#                 confirmation_mean=trial_df['values.response_latency'].astype(float).mean()
#                 confirmation_vals=trial_df['values.response_latency'].astype(float)
#         subj_line=[subj,subj_df['date'].unique().astype(str)[0]]

#         for trial in ['trial1','trial2','trial3','trial4','trial5','listb','trial6','trial7']:
#             try:
#                 trial_idx=[meas[0] for meas in measures].index(trial)
#                 subj_line.extend(measures[int(trial_idx)][1:])
#             except:
#                 subj_line.exteend(4*np.nan)
#                 continue

#         print confirmation_mean,confirmation_vals
#         final_csv.append(subj_line)
