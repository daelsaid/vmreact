import os

import pandas as pd

data_dir = '/Users/lillyel-said/Desktop/vmreact/vmreact/2_vmreact/'
compiled = '/Users/lillyel-said/Desktop/vmreact/vmreact/2_vmreact/mturk_vmreact_complete_compilation_initiation.csv'
av_typing = '/Users/lillyel-said/Desktop/vmreact/vmreact/2_vmreact/typing_test_averages.csv'
trials = ['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'listb', 'trial6', 'trial7']
cols = ['values.response_latency', 'expressions.trial_recall_word_latency',
		'values.recall_firstcharlatency', 'values.recall_lastcharlatency']
column_titles = ['subjid', 'date']

incorrect = pd.read_csv(os.path.join(data_dir, 'incorrect_response.csv'), dtype=str)
vmreact_df = pd.read_csv(compiled, dtype='str')

avg_typing_df = pd.read_csv(av_typing, dtype='str')

vmreact_df['unique_identifier'] = vmreact_df['subject'] + '_' + vmreact_df['date']
df2 = vmreact_df.merge(avg_typing_df, left_on='unique_identifier', right_on='unique_identifier', how='outer')
new_compiled = pd.DataFrame(data=df2, dtype=str)
new_compiled["total_average_repeats"] = new_compiled.loc[:, 'listb_#_repeats':'trial7_#_repeats'].astype(float).mean(
	axis=1)
new_compiled["total_incorrect"] = new_compiled.loc[:, 'listb':'trial7'].astype(float).subtract(15, axis=0)
new_compiled[['listb_errors', 'trial1_errors', 'trial2_errors', 'trial3_errors', 'trial4_errors', 'trial5_errors',
			  'trial6_errors', 'trial7_errors']] = new_compiled.loc[:, 'listb':'trial7'].astype(float).subtract(15,
																												axis=0).abs()

# for x,y in incorrect.groupby(['subj_id','trial']):
#     print x,y.score.value_counts().T

new_compiled.to_csv('updated_mturk_vmreact_complete_compilation_initiation.csv')
