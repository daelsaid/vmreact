# coding: utf-8

# In[ ]:

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# In[ ]:

data_dir = '/Users/lillyel-said/Desktop/vmreact/vmreact/2_vmreact/'
all_data = pd.read_csv(os.path.join(data_dir, 'mturk_vmreact_complete_compilation.csv'))
indexed_df = pd.DataFrame(data=all_data.set_index(['gender_response', 'age_range']))

# In[ ]:


indexed_df['time_comp_response'].value_counts()
print indexed_df['online_sr_q2option1_response'].value_counts()
print indexed_df['online_sr_q2option2_response'].value_counts()
print indexed_df['online_sr_q2option3_response'].value_counts()

indexed_df.hist(
	column=['expressions.pcl_total_hybridscore_corrected', 'expressions.phq_total', 'expressions.pcl_4_total',
			'gad_7_q2_response'])
# indexed_df.hist(column=['online_sr_q2option1_response','online_sr_q2option2_response','online_sr_q2option3_response'])


# In[ ]:

for idx, data in indexed_df.groupby(level=[0, 1]):
	print idx
	print data['education_response'].T.value_counts()

#     data.hist(column=['expressions.pcl_total_hybridscore_corrected','expressions.phq_total','expressions.pcl_4_total','gad_7_q2_response'])


# In[ ]:

y = ['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'listb', 'trial6', 'trial7']
colors = ['lightskyblue', 'lightskyblue', 'lightskyblue', 'lightskyblue', 'lightskyblue', '#96D38C', '#E1396C',
		  '#E1396C']

columns = [c for c in y]
bins = range(0, 17)

for idx, val in indexed_df.groupby(level=[0, 1]):
	if len(val[columns]) > 3:
		trials = val.loc[:, 'listb':'trial7']
		fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(14, 12))
		fig = trials.plot.hist(y=y, bins=bins, subplots=True, ax=axes, legend=True, title=idx, xticks=range(0, 16),
							   xlim=(0, 16), fontsize=10, color=colors)
		for (m, n), subplot in np.ndenumerate(axes):
			ymin, ymax = subplot.get_ylim()
			subplot.set_ylim(0, (ymax + 1))
	else:
		print idx, 'n too small'

# In[ ]:

# all_data.rename(columns={'gender_response':'gender','age_textbox_response':'age','date_x':'date'},inplace=True)


# In[ ]:

trial_latency_cols = ['subject', 'date']

trial_latency_cols.extend(
	[col for col in indexed_df.columns.tolist() if 'firstcharlatency' in col or 'response_latency' in col])

first_char_df = pd.DataFrame(data=all_data,
							 columns=[c for c in trial_latency_cols if 'firstchar' in c or 'subject' in c])
recall_df = pd.DataFrame(data=all_data, columns=[r for r in trial_latency_cols if 'response' in r or 'subject' in r])

first_char_df.set_index(['subject']).dropna(inplace=True)
recall_df.set_index(['subject']).dropna(inplace=True)

# In[ ]:

trials = ['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'listb', 'trial6', 'trial7']
new = pd.DataFrame()

for t in trials:
	new[t + '_initiation_latency'] = all_data[t + '_values.response_latency'].subtract(
		all_data[t + '_values.recall_firstcharlatency'])

# In[ ]:

pd.concat([all_data, new], axis=1).to_csv(os.path.join(data_dir, 'mturk_vmreact_complete_compilation_initiation.csv'))

# In[ ]:

import os
import numpy as np
import pandas as pd
from glob import glob

# In[ ]:

data_dir = '/Users/lillyel-said/Desktop/vmreact/final_inquisit_launches/launches/broken_up_by_each_launch/0612217_reyravlt_antr_pilot4'
output_dir = '/Users/lillyel-said/Desktop/vmreact/final_inquisit_launches/launches/broken_up_by_each_launch/0612217_reyravlt_antr_pilot4/test'

# In[ ]:

trials = ['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'listb', 'trial6', 'trial7']

cols = ['values.response_latency', 'expressions.trial_recall_word_latency',
		'values.recall_firstcharlatency', 'values.recall_lastcharlatency']

column_titles = ['subjid', 'date']

for trial in trials:
	for meas in cols:
		column_titles.append(trial + "_" + meas)

final_csv = [column_titles]
print cols

# In[ ]:

total_columns = []
for data_file in glob(os.path.join(data_dir, '*raw.csv')):
	data_df = pd.read_csv(data_file, dtype=str)
	data_df.loc[data_df['response'] == ' ', 'trialcode'] = 'trial_confirmation'
	for trial in ['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'trial6', 'trial7', 'trial8', 'listb']:
		data_df.loc[data_df['trialcode'].str.contains(trial), 'trialcode'] = trial

	data_df.rename(columns
				   ={'latency': 'values.response_latency'}, inplace=True)

	for col in data_df.columns.tolist():
		if col not in total_columns:
			total_columns.append(col)
print sorted(total_columns)
for t in trials:
	new[t + '_initiation_latency'] = all_data[t + '_values.response_latency'].subtract(
		all_data[t + '_values.recall_firstcharlatency'])

# In[ ]:

cols = ['typing_test_openended_sentence1', 'typing_speed_next_trial', 'typing_test_openended_sentence2',
		'typing_test_error2', 'typing_test_openended_sentence2', 'typing_speed_next_trial_2',
		'typing_test_openended_sentence3']

for data_file in glob(os.path.join(data_dir, '*raw.csv')):
	df = pd.read_csv(data_file, dtype=str)
	typing_test = df.loc[df['blockcode'] == 'typing_test']

#     for trial in cols:
#
#         typingtest=df.loc[df['trialcode'].str.contains(trial),'trialcode']
#         print df.loc[df['trialcode']==trial]


# In[ ]:

for data_file in glob(os.path.join(data_dir, '*raw.csv')):
	data_df = pd.read_csv(data_file, dtype=str)
	data_df.loc[data_df['response'] == ' ', 'trialcode'] = 'trial_confirmation'

	for trial in ['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'trial6', 'trial7', 'trial8', 'listb']:
		data_df.loc[data_df['trialcode'].str.contains(trial), 'trialcode'] = trial

	data_df.rename(columns={'latency': 'values.response_latency'}, inplace=True)

	subj_list = data_df.loc[data_df['trialcode'] == 'trial8', 'subject'].unique()
	if len(subj_list) > 0:
		data_df.loc[(data_df['trialcode'] == 'trial6') & (data_df['subject'].isin(subj_list)), 'trialcode'] = 'listb'
		data_df.loc[(data_df['trialcode'] == 'trial7') & (data_df['subject'].isin(subj_list)), 'trialcode'] = 'trial6'
		data_df.loc[(data_df['trialcode'] == 'trial8') & (data_df['subject'].isin(subj_list)), 'trialcode'] = 'trial7'

	for subj, subj_df in data_df.groupby(['subject']):
		measures = []
		for trial, trial_df in subj_df.groupby(['trialcode']):
			if trial in ['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'listb', 'trial6', 'trial7']:
				trial_measures = [np.nan] * 4
				for idx, meas in enumerate(cols):
					if 'values.recall' in meas:
						print subj, meas, trial_df['values.recall_lastcharlatency'].astype(float).subtract(
							trial_df['values.recall_firstcharlatency'].astype(float))
					try:
						trial_measures[idx] = round(trial_df[meas].astype('float').mean(), 4)
						#                         print meas,trial_measures[idx]
						#                       subj_df[meas].subtract(subj_df[trial+'_values.recall_firstcharlatency'])
						x = trial_df['values.recall_lastcharlatency'][trial_measures].subtract(
							trial_df['values.recall_firstcharlatency'][trial_measures], axis=1)
					except:
						trial_measures[idx] = np.nan
						continue

				measures.append([trial] + trial_measures)
			elif trial == 'trial_confirmation':
				confirmation_mean = trial_df['values.response_latency'].astype(float).mean()
				confirmation_vals = trial_df['values.response_latency'].astype(float)
		subj_line = [subj, subj_df['date'].unique().astype(str)[0]]
#         for trial in ['trial1','trial2','trial3','trial4','trial5','listb','trial6','trial7']:
#             try:
#                 trial_idx=[meas[0] for meas in measures].index(trial)
#                 subj_line.extend(measures[int(trial_idx)][1:])
#             except:
#                 subj_line.exteend(4*np.nan)
#                 continue

#         print confirmation_mean,confirmation_vals
#         final_csv.append(subj_line)


# In[ ]:


# In[ ]:
