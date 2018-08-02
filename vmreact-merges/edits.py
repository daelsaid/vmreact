# coding: utf-8

# In[3]:

import collections
import csv
import datetime
from difflib import SequenceMatcher
from glob import glob
from math import ceil
from shutil import copy, move

import pandas as pd
from IPython.display import display


# #Grading Script
# In[2]:


def grader(all_subj_data_csv, data_output_raw_csv, data_output_scored_csv, word_corr, p_r):
	with open(all_subj_data_csv, 'U') as file:
		input_csv_lines_all_subj = csv.reader(file)
		input_csv_lines_all_subj = map(list, zip(*input_csv_lines_all_subj))
		all_subj_csv_lines = dict((rows[0], rows[1:]) for rows in input_csv_lines_all_subj)

	subj_listtype = []
	for idx, row in enumerate(all_subj_csv_lines['subject']):
		if 'rey_list' in all_subj_csv_lines['trialcode'][idx]:
			subj_listtype.append([all_subj_csv_lines['subject'][idx], all_subj_csv_lines['trialcode'][idx]])

	set_subj_listtype = []
	for subj in subj_listtype:
		if subj not in set_subj_listtype:
			set_subj_listtype.append(subj)

	## count per list type
	index_number_resp = dict()
	for list_type in sorted([x for x in set(all_subj_csv_lines['trialcode']) if 'rey_list' in x]):
		index_number_resp[list_type] = []

	for idx, response in enumerate(all_subj_csv_lines['response']):
		if 'recall_response' in all_subj_csv_lines['trialcode'][idx]:
			if 'listb' not in all_subj_csv_lines['trialcode'][idx]:
				index_number_resp[
					set_subj_listtype[[x[0] for x in set_subj_listtype].index(all_subj_csv_lines['subject'][idx])][
						1]].append(response.lower().strip())
			elif 'listb' in all_subj_csv_lines['trialcode'][idx]:
				index_number_resp[
					set_subj_listtype[[x[0] for x in set_subj_listtype].index(all_subj_csv_lines['subject'][idx])][1][
					:-1] + 'b'].append(response.lower().strip())

	counter_dict = dict()
	for list_type in sorted(index_number_resp.keys()):
		rey_recall_word_count = collections.Counter(index_number_resp[list_type])
		counter_dict[list_type] = rey_recall_word_count

	total_response_for_list = dict()
	for list_type in sorted(index_number_resp.keys()):
		total_response_for_list[list_type] = sorted(set(index_number_resp[list_type]))

	if p_r == 0:
		rey_word_lists = {
			'rey_list_presentation_1a': ['drum', 'curtain', 'bell', 'coffee', 'school', 'parent', 'moon', 'garden',
										 'hat', 'farmer', 'nose', 'turkey', 'color', 'house', 'river'],

			'rey_list_presentation_2a': ['pipe', 'wall', 'alarm', 'sugar', 'student', 'mother', 'star', 'painting',
										 'bag', 'wheat', 'mouth', 'chicken', 'sound', 'door', 'stream'],

			'rey_list_presentation_3a': ['violin', 'tree', 'scarf', 'ham', 'suitcase', 'cousin', 'earth', 'stairs',
										 'dog', 'banana', 'town', 'radio', 'hunter', 'bucket', 'field'],

			'rey_list_presentation_4a': ['doll', 'mirror', 'nail', 'sailor', 'heart', 'desert', 'face', 'letter', 'bed',
										 'machine', 'milk', 'helmet', 'music', 'horse', 'road'],
			'rey_list_presentation_1b': ['desk', 'ranger', 'bird', 'shoe', 'stove', 'mountain', 'glasses', 'towel',
										 'cloud', 'boar', 'lamb', 'gun', 'pencil', 'church', 'fish'],
			'rey_list_presentation_2b': ['bench', 'officer', 'cage', 'sock', 'fridge', 'cliff', 'bottle', 'soap',
										 'sky', 'ship', 'goat', 'bullet', 'paper', 'chapel', 'crab'],
			'rey_list_presentation_3b': ['orange', 'table', 'toad', 'corn', 'bus', 'chin', 'bleach', 'soap', 'hotel',
										 'donkey', 'spider', 'money', 'book', 'soldier', 'padlock'],
			'rey_list_presentation_4b': ['dish', 'jester', 'hill', 'coat', 'tool', 'forest', 'perfume', 'ladder',
										 'girl', 'foot', 'shield', 'pie', 'insect', 'ball', 'car']
		}
	elif p_r == 1:
		rey_word_lists = {'rey_list_presentation_1a': ['drum', 'curtain', 'bell', 'coffee', 'school'],
						  'rey_list_presentation_2a': ['pipe', 'wall', 'alarm', 'sugar', 'student'],
						  'rey_list_presentation_3a': ['violin', 'tree', 'scarf', 'ham', 'suitcase'],
						  'rey_list_presentation_4a': ['doll', 'mirror', 'nail', 'sailor', 'heart'],
						  'rey_list_presentation_1b': ['desk', 'ranger', 'bird', 'shoe', 'stove'],
						  'rey_list_presentation_2b': ['bench', 'officer', 'cage', 'sock', 'fridge'],
						  'rey_list_presentation_3b': ['orange', 'table', 'toad', 'corn', 'bus'],
						  'rey_list_presentation_4b': ['dish', 'jester', 'hill', 'coat', 'tool']
						  }
	elif p_r == 2:
		rey_word_lists = {'rey_list_presentation_1a': ['nose', 'turkey', 'color', 'house', 'river'],
						  'rey_list_presentation_2a': ['mouth', 'chicken', 'sound', 'door', 'stream'],
						  'rey_list_presentation_3a': ['town', 'radio', 'hunter', 'bucket', 'field'],
						  'rey_list_presentation_4a': ['milk', 'helmet', 'music', 'horse', 'road'],
						  'rey_list_presentation_1b': ['lamb', 'gun', 'pencil', 'church', 'fish'],
						  'rey_list_presentation_2b': ['goat', 'bullet', 'paper', 'chapel', 'crab'],
						  'rey_list_presentation_3b': ['spider', 'money', 'book', 'soldier', 'padlock'],
						  'rey_list_presentation_4b': ['shield', 'pie', 'insect', 'ball', 'car']
						  }

	with open(word_corr, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		for word_list in sorted(total_response_for_list.keys()):
			word_corrs = []
			for word in total_response_for_list[word_list]:
				wordcorrs = [round(SequenceMatcher(None, word, x).ratio(), 3) for x in rey_word_lists[word_list]]
				word_corrs.append(wordcorrs)
				writer.writerow([word, max(wordcorrs), rey_word_lists[word_list][wordcorrs.index(max(wordcorrs))]])
	csvfile.close()

	subj_id_list = []
	subj_only = []
	for subj in sorted(set(all_subj_csv_lines['subject'])):
		try:
			subj_list_type = [all_subj_csv_lines['trialcode'][x] for x in range(len(all_subj_csv_lines['subject']))
							  if (all_subj_csv_lines['subject'][x] == subj) and (
									  'rey_list_presentation_' in all_subj_csv_lines['trialcode'][x])][0]
			subj_id_list.append([all_subj_csv_lines['date'][x] + '_' + subj, subj_list_type])
			subj_only.append(subj)
		except:
			print "%s has an error in their data" % subj
			continue

	full_raw_data_responses = [
		[all_subj_csv_lines['date'][x] + '_' + all_subj_csv_lines['subject'][x], all_subj_csv_lines['trialcode'][x],
		 all_subj_csv_lines['response'][x].lower()]
		for x in range(len(all_subj_csv_lines['subject']))
		if 'recall_response' in all_subj_csv_lines['trialcode'][x]]
	all_responses = []
	repeats = []
	list_b_all = []
	list_a_all = []
	with open(data_output_raw_csv, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(('subj_id', 'list_type', 'trial', 'response', 'score'))
		for response in full_raw_data_responses:
			subj = response[0]
			list_to_use = [subj_id_list[x][1] for x in range(len(subj_id_list)) if subj_id_list[x][0] == subj][0]
			list_a_all.append(list_to_use)
			list_b = list_to_use[:-1] + 'b'
			list_b_all.append(list_b)
			if 'listb' in response[1]:
				if response[2] in rey_word_lists[list_b]:
					response.append(1)
				else:
					if any(n > 0.8 for n in
						   [SequenceMatcher(None, response[2], x).ratio() for x in rey_word_lists[list_b]]):
						response.append(1)
					else:
						response.append(0)
				new_row = response[0], list_b, response[1].split('_')[0], response[2], response[3]
			else:
				if response[2] in rey_word_lists[list_to_use]:
					response.append(1)
				else:
					if any(n > 0.8 for n in
						   [SequenceMatcher(None, response[2], x).ratio() for x in rey_word_lists[list_to_use]]):
						response.append(1)
					else:
						response.append(0)
				new_row = response[0], list_to_use, response[1].split('_')[0], response[2], response[3]
			writer.writerow(new_row)
			all_responses.append(response)
			rep = new_row
			repeats.append(rep)
	csvfile.close()

	trial_breaks = []
	trial_lines = [all_responses[y][1] for y in range(0, len(all_responses))]
	trial_breaks = [i for i, x in enumerate(trial_lines[0:])
					if x.split('_')[0] != trial_lines[i - 1].split('_')[0]]

	trial_breaks = trial_breaks + [len(all_responses)]

	subj_scores = []
	final = []
	final_repeats = []
	for idx, val in enumerate(trial_breaks[:-1]):
		score = 0
		word_list = []
		for line in all_responses[trial_breaks[idx]:trial_breaks[idx + 1]]:
			if line[3] == 1:
				score = score + 1
				word_list.append(line[2])
		test = []
		for idx, word in enumerate(word_list):
			test.append([SequenceMatcher(None, word, x).ratio() for x in
						 [y for idx2, y in enumerate(word_list) if idx != idx2]])
		repeats = 0
		for word in test:
			word_thresholded = [ceil(x) for x in word if x > 0.8]
			n = sum(word_thresholded)
			if n != 0:
				repeats = repeats + (((n * (n + 1)) - 1) / (n + 1))
		subj_scores.append([line[0], line[1].split('_')[0], score, repeats])

	with open(data_output_scored_csv, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(
			['subj_id', 'list_type', 'listb', 'trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'trial6', 'trial7',
			 'listb_#_repeats', 'trial1_#_repeats', 'trial2_#_repeats', 'trial3_#_repeats', 'trial4_#_repeats',
			 'trial5_#_repeats', 'trial6_#_repeats', 'trial7_#_repeats'])
		subj_scores = subj_scores + ['placeholder']
		for idx, scores in enumerate(sorted(subj_scores[:-1])):
			scored = str(scores[2] - scores[3])
			repeat_nm = scores[3]
			final.append(scored)
			final_repeats.append(repeat_nm)
			subj_id = [scores[0]]
			for idx2, val in enumerate(subj_id_list):
				if subj_id[0] == subj_id_list[idx2][0]:
					subj_list = subj_id_list[idx2][1].split('_')[3]
			final_row = subj_id + [subj_list] + final + final_repeats
			if scores[0] != sorted(subj_scores)[idx + 1][0]:
				writer.writerow(final_row)
				final_row = []
				subj_id = []
				final = []
				final_repeats = []
	csvfile.close()


# In[63]:

# Getting composite scores from scored


# In[ ]:

import numpy as np
import pandas
import os


def composite_scores(input_csv, output_csv):
	scored_data = pandas.read_csv(input_csv)
	print input_csv
	df_trials = scored_data.loc[:, 'trial1':'trial7']
	print df_trials.columns.tolist()
	composite_scores = pandas.DataFrame()
	tmp = pandas.DataFrame()
	composite_scores['total_learning'] = df_trials[['trial1', 'trial2', 'trial3', 'trial4', 'trial5']].apply(
		lambda row: np.sum(row), axis=1)
	tmp['test'] = df_trials['trial1'].tolist() * 5
	composite_scores['corrected_total_learning'] = composite_scores['total_learning'].subtract(tmp['test'])

	composite_scores['learning_rate'] = df_trials['trial5'].subtract(df_trials['trial1'], axis='rows')
	composite_scores['proactive_interference'] = df_trials['trial1'].subtract(scored_data['listb'], axis='rows')
	composite_scores['retroactive_interference'] = df_trials['trial5'].subtract(df_trials['trial6'], axis='rows')

	composite_scores['forgetting_and_retention'] = df_trials['trial5'].subtract(df_trials['trial7'], axis='rows')

	composite_scores_transposed = composite_scores.transpose()

	composite_scores_transposed.to_csv(output_csv, header=True, index=['measure', 'score'])
	composite_scores.to_csv(output_csv, header=True, index=['measure', 'score'])


for scored in glob('/Users/cdla/Desktop/scratch/vmreact/2_vmreact/*_scored_data.csv'):
	composite_scores(scored, scored.replace('_scored_data.csv', '_composite_scores.csv'))

# In[ ]:

format = "%Y_%m_%d"
current_date = datetime.datetime.today()
date = current_date.strftime(format)

output_csv_location = '/Users/cdla/Desktop/scratch/vmreact/2_vmreact/'

for raw in glob('/Users/cdla/Desktop/scratch/vmreact/1_rawdata/*/*raw.csv'):
	raw_data = raw
	demo_data = raw.replace('raw.csv', 'demo.csv')
	summary_data = raw.replace('raw.csv', 'summary.csv')
	prefix = 'mturk_' + os.path.basename(os.path.dirname(raw_data)).split('_')[1] + '_'
	grader(raw_data, os.path.join(output_csv_location, prefix + 'parsed_raw_data.csv'),
		   os.path.join(output_csv_location, prefix + 'scored_data.csv'),
		   os.path.join(output_csv_location, prefix + 'word_correlations.csv'), 0)
	grader(raw_data, os.path.join(output_csv_location, prefix + 'parsed_raw_data_primacy.csv'),
		   os.path.join(output_csv_location, prefix + 'scored_data_primacy.csv'),
		   os.path.join(output_csv_location, prefix + 'word_correlations_primacy.csv'), 1)
	grader(raw_data, os.path.join(output_csv_location, prefix + 'parsed_raw_data_recency.csv'),
		   os.path.join(output_csv_location, prefix + 'scored_data_recency.csv'),
		   os.path.join(output_csv_location, prefix + 'word_correlations_recency.csv'), 2)
	copy(demo_data, os.path.join(output_csv_location, prefix + 'demo.csv'))
	copy(summary_data, os.path.join(output_csv_location, prefix + 'summary.csv'))

# In[4]:

scored_dir = '/Users/cdla/Desktop/scratch/vmreact/2_vmreact/'
for scored_csv in glob(os.path.join(scored_dir, '*parsed*')):
	with open(scored_csv, 'rb') as source:
		rdr = csv.reader(source)
		with open(os.path.join(scored_dir, 'tmp.csv'), 'wb') as result:
			wtr = csv.writer(result)
			for r in rdr:
				wtr.writerow(r[0:18])
	move(os.path.join(scored_dir, 'tmp.csv'), scored_csv)
	print scored_csv

# In[174]:

scored_dir = '/Users/cdla/Desktop/scratch/vmreact/2_vmreact/'

demo_cols = []
clin_raw_cols = []
sum_cols = ['script.startdate', 'script.starttime', 'subject',
			'expressions.gad_7_total', 'expressions.phq_total', 'expressions.pcl_4_total',
			'expressions.pcl_total_hybridscore_corrected', 'expressions.pcl_total_hybridscore_uncorrected']
scored_cols = ['subj_id', 'list_type', 'listb', 'trial1', 'trial2', 'trial3',
			   'trial4', 'trial5', 'trial6', 'trial7', 'listb_#_repeats', 'trial1_#_repeats', 'trial2_#_repeats',
			   'trial3_#_repeats', 'trial4_#_repeats', 'trial5_#_repeats', 'trial6_#_repeats', 'trial7_#_repeats']
composite_cols = ['subject', 'total_learning', 'corrected_total_learning', 'learning_rate',
				  'proactive_interference', 'retroactive_interference', 'forgetting_and_retention']

for batch in range(1, 9):
	batch = str(batch)
	demo = os.path.join(scored_dir, 'mturk_batch' + batch + '_demo.csv')
	clin_raw = os.path.join(scored_dir, 'mturk_batch' + batch + '_end.csv')
	sum = os.path.join(scored_dir, 'mturk_batch' + batch + '_summary.csv')
	scored = os.path.join(scored_dir, 'mturk_batch' + batch + '_scored_data.csv')
	composite = os.path.join(scored_dir, 'mturk_batch' + batch + '_composite_scores.csv')

	demo_df = pd.read_csv(demo, dtype=str)
	demo_cols.extend([x for x in demo_df.columns.tolist() if (
			'latency' not in x and 'online' not in x and 'Unnamed' not in x and 'time_comp' not in x and 'subj_id' not in x)])
	print batch
	clin_raw_df = pd.read_csv(clin_raw, dtype=str)
	clin_raw_cols.extend(
		[x for x in clin_raw_df.columns.tolist() if 'latency' not in x and 'end' not in x and 'Unnamed' not in x])
	sum_df = pd.read_csv(sum, dtype=str)
	scored_df = pd.read_csv(scored, dtype=str)
	comp_df = pd.read_csv(composite, dtype=str).rename(index=str, columns={'Unnamed: 0': 'subject'})

demo_cols = list(set(demo_cols))
clin_raw_cols = list(set(clin_raw_cols))

print demo_cols
print clin_raw_cols

# need to get latency values,
# use the scored to set the subject ids. 
# append composite to scored_cols since they're in the same order and composite doesn't have subject ids
# summary - use script.subjectid
# demo - use subject
# clin_raw - use subject

# In[281]:

scored_dir = '/Users/cdla/Desktop/scratch/vmreact/2_vmreact/'
latency_csv = os.path.join(scored_dir, 'vmreact_latency_summary.csv')

# for batch in range(1,9):
for batch in [8]:
	batch_df = pd.DataFrame()
	batch = str(batch)
	print 'mturk_batch' + batch

	demo = os.path.join(scored_dir, 'mturk_batch' + batch + '_demo.csv')
	clin_raw = os.path.join(scored_dir, 'mturk_batch' + batch + '_end.csv')
	sum = os.path.join(scored_dir, 'mturk_batch' + batch + '_summary.csv')
	scored = os.path.join(scored_dir, 'mturk_batch' + batch + '_scored_data.csv')
	composite = os.path.join(scored_dir, 'mturk_batch' + batch + '_composite_scores.csv')

	demo_df = pd.read_csv(demo, dtype=str)
	clin_raw_df = pd.read_csv(clin_raw, dtype=str)
	sum_df = pd.read_csv(sum, dtype=str).rename(index=str, columns={'script.subjectid': 'subject'})
	scored_df = pd.read_csv(scored)
	comp_df = pd.read_csv(composite).rename(index=str, columns={'Unnamed: 0': 'subject'})
	comp_df['subject'] = comp_df['subject'].apply(int)
	vmreact_df = pd.merge(scored_df, comp_df, left_index=True, right_on='subject', how='left').drop('subject', axis=1)
	vmreact_df['subj_id'] = vmreact_df['subj_id'].astype(str)
	# vmreact_df['subj_id']=vmreact_df['subj_id'].apply(pd.to_numeric)
	latency_df = pd.read_csv(latency_csv, dtype=str)

	latency_df = latency_df.drop_duplicates().reset_index()

	subject_ids = vmreact_df['subj_id'].tolist()

	batch_demo_cols = [x for x in demo_df.columns.tolist() if x in demo_cols]
	append_demo_cols = [x for x in demo_cols if x not in demo_df.columns.tolist()]
	demo_df = demo_df[demo_df['subject'].astype(str).isin(subject_ids)][batch_demo_cols]
	for col in append_demo_cols:
		demo_df[col] = np.nan
	# print demo_df
	# demo_df['subject']=demo_df['subject'].apply(pd.to_numeric)

	batch_clin_cols = [x for x in clin_raw_df.columns.tolist() if x in clin_raw_cols]
	append_clin_cols = [x for x in clin_raw_cols if x not in clin_raw_df.columns.tolist()]
	clin_raw_df = clin_raw_df[clin_raw_df['subject'].astype(str).isin(subject_ids)][batch_clin_cols]
	for col in sorted(append_clin_cols):
		clin_raw_df[col] = np.nan
	# clin_raw_df['subject']=clin_raw_df['subject'].apply(pd.to_numeric)

	batch_sum_cols = [x for x in sum_df.columns.tolist() if x in sum_cols]
	append_sum_cols = [x for x in sum_cols if x not in sum_df.columns.tolist()]
	sum_df = sum_df[sum_df['subject'].astype(str).isin(subject_ids)][batch_sum_cols]
	for col in sorted(append_sum_cols):
		sum_df[col] = np.nan
	# sum_df['subject']=sum_df['subject'].apply(pd.to_numeric)

	batch_df = demo_df.merge(sum_df, left_on='subject', right_on='subject').drop(
		['script.startdate', 'script.starttime'], axis=1)
	batch_df = batch_df.merge(clin_raw_df, left_on='subject', right_on='subject').drop(
		['date_y', 'time_y', 'group_y', 'build_y'], axis=1)
	batch_df = batch_df.merge(vmreact_df, left_on='subject', right_on='subj_id').drop('subj_id', axis=1)
	batch_df = batch_df.rename(columns={'date_x': 'date', 'time_x': 'time', 'group_x': 'group', 'build_x': 'build'})
	# print batch_df

	print subject_ids
	latency_df['subjid'] = latency_df['subjid'].astype(str)
	latency_df['date'] = latency_df['date'].astype(int)
	batch_df['date'] = batch_df['date'].astype(int)

	latency_df = latency_df.loc[(latency_df['subjid'].isin(
		batch_df['subject'].astype(str).tolist()))]  # & latency_df['date'].isin(batch_df['date'].tolist()))]

	latency_df = latency_df.loc[(
			latency_df['subjid'].isin(batch_df['subject'].astype(str).tolist()) & latency_df['date'].isin(
		batch_df['date'].tolist()))]

	batch_df['subject'] = batch_df['subject'].astype(str)
	batch_df = batch_df.merge(latency_df, left_on='subject', right_on='subjid')

	batch_df.to_csv(os.path.join(scored_dir, 'mturk_batch' + batch + '_compiled.csv'))
	os.system('open /Users/cdla/Desktop/scratch/vmreact/2_vmreact/' + 'mturk_batch' + batch + '_compiled.csv')

# In[318]:

dataframes_to_concat = []
result = []
for compiled_csv in glob(os.path.join(scored_dir, '*compiled.csv')):
	df = pd.read_csv(compiled_csv, dtype=str)
	dataframes_to_concat.append(df)

result = pd.concat(dataframes_to_concat).reindex_axis(df.columns.tolist(), axis=1).drop(
	['index', 'date_y', 'subjid', 'Unnamed: 0'], axis=1).dropna(how='all', axis=1).drop_duplicates()

# print result.subject
result = result[~result.subject.isin(['XXX', 'AVD6HMIO1HLFI', 'A5EU1AQJNC7F2'])]
result.drop_duplicates(['date_x', 'subject'])
display(result)
result.to_csv(os.path.join(scored_dir, 'mturk_vmreact_complete_compilation.csv'), index=False)

# In[ ]:
