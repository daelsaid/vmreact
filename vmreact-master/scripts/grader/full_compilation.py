import datetime
from glob import glob
import pandas as pd
import os
import numpy as np
from inquisit_grader import grader
from composite_scores import composite_scores
from inquisit_demo_summary import demo_and_summary
from inquisit_demo_summary_newageranges import demo_and_summary_new
from best_vmreact_subj_naming import best_rename_with_subj
from best_vmreact_compilation_merged import restructure_and_regrade_all_data
from extract_csv_into_dict_fxn import extract_data_from_csv_into_dict
from best_vmreact_subj_naming
# os.chdir('/Users/lillyel-said/Desktop/stanford/scripts/projects/vmreact_conda/vmreact-master/scripts/grader')

import collections
import csv
import datetime
from difflib import SequenceMatcher
from math import ceil
from shutil import copy, move

from IPython.display import display

format = "%Y_%m_%d"
current_date = datetime.datetime.today()
date = current_date.strftime(format)

# output_csv_location = '/Users/lillyel-said/Desktop/inquisit_renamed/t1/'
output_csv_location = '/Volumes/wd_daelsaid/inquisit/data'
# for raw in glob(os.path.join(os.path.dirname(scored_dir))):


for raw in glob('/Volumes/wd_daelsaid/inquisit/data/*raw.csv'):
	path = raw.split('/')[-1]
	path = path.split('_')[0:3]
	id = '_'.join(path) + '_inquisit'
	demo = '_'.join(path) + '_demographics_survey.csv'
	summary = '_'.join(path) + '_summary.csv'
	end = '_'.join(path) + '_rey_ant_survey.csv'
	raw_data = raw
	demo_data = raw.replace('raw.csv', 'demographics_survey.csv')
	summary_data = raw.replace('raw.csv', 'summary.csv')
	prefix = 'best_' + path[1] + '_' + path[2] + '_'
	scored = prefix + 'scored_data' + '_' + date + '.csv'
	comp = prefix + 'composite_scores_vakil' + '_' + date + '.csv'

	try:
		grader(raw_data, os.path.join(output_csv_location, prefix + 'parsed_raw_data' + '_' + date + '.csv'),
		os.path.join(output_csv_location, prefix +
		             'scored_data' + '_' + date + '.csv'),
		os.path.join(output_csv_location, prefix + 'word_correlations' + '_' + date + '.csv'), 0)

		grader(raw_data, os.path.join(output_csv_location, prefix + 'parsed_raw_data_primacy' + '_' + date + '.csv'),
		os.path.join(output_csv_location, prefix +
		             'scored_data_primacy' + '_' + date + '.csv'),
		os.path.join(output_csv_location, prefix + 'word_correlations_primacy' + '_' + date + '.csv'), 1)

		grader(raw_data, os.path.join(output_csv_location, prefix + 'parsed_raw_data_recency' + '_' + date + '.csv'),
		os.path.join(output_csv_location, prefix +
		             'scored_data_recency' + '_' + date + '.csv'),
		os.path.join(output_csv_location, prefix + 'word_correlations_recency' + '_' + date + '.csv'), 2)

		demo_and_summary(raw_data, demo_data, summary_data, os.path.join(output_csv_location, prefix + 'frequency_counts' + '_' + date + '.csv'), os.path.join(output_csv_location, prefix + 'age_agerange_gender' +
		                 '_' + date + '.csv'), os.path.join(output_csv_location, prefix + 'sr_responses' + '_' + date + '.csv'), os.path.join(output_csv_location, prefix + 'summary_ant_scores' + '_' + date + '.csv'))

		demo_and_summary_new(raw_data, os.path.join(output_csv_location, demo), os.path.join(
		    output_csv_location, prefix + 'age_agerange_gender_new_age_bins' + '_' + date + '.csv'))
	except:
		   continue


for scored in glob('/Volumes/wd_daelsaid/inquisit/data/*_scored_data_' + date + '.csv'):
	path = os.path.dirname(scored)
	prefix_id = scored.split('/')[-1]
	comp = os.path.join(path, 'best_' + prefix_id.split('_')[1] + '_' + prefix_id.split(
	    '_')[2] + '_composite_scores_vakil' + '_' + date + '.csv')
	try:
		composite_scores(1, scored, comp)
	except:
		continue

##########

demo_cols = []
clin_raw_cols = []
sum_cols = ['script.startdate', 'script.starttime', 'subject', 'expressions.gad_7_total', 'expressions.phq_total',
    'expressions.pcl_4_total', 'expressions.pcl_total_hybridscore_corrected', 'expressions.pcl_total_hybridscore_uncorrected']
scored_cols = ['subj_id', 'list_type', 'listb', 'trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'trial6', 'trial7', 'listb_#_repeats',
    'trial1_#_repeats', 'trial2_#_repeats', 'trial3_#_repeats', 'trial4_#_repeats', 'trial5_#_repeats', 'trial6_#_repeats', 'trial7_#_repeats']
composite_cols = ['subject', 'total_learning', 'corrected_total_learning', 'learning_rate',
    'proactive_interference', 'retroactive_interference', 'forgetting_and_retention']


subject_with_tp = []
for subj in glob(os.path.join(output_csv_location, '*raw.csv')):
	file = subj.split('/')[-1]
	ids_with_tp = file.split('_')[1] + '_' + file.split('_')[2]
	subject_with_tp.append(ids_with_tp)

	batch = str(subject)
	subjid = 'best_' + batch + '_'

	demo = subjid + 'demographics_survey.csv'
	summary = subjid + 'summary.csv'
	end = subjid + 'rey_ant_survey.csv'
	scored = subjid + 'scored_data' + '_' + date + '.csv'
	comp = subjid + 'composite_scores_vakil' + '_' + date + '.csv'
	try:
		demo = os.path.join(output_csv_location, demo)
		clin_raw = os.path.join(output_csv_location, end)
		sum = os.path.join(output_csv_location, summary)
		scored = os.path.join(output_csv_location, scored)
		composite = os.path.join(output_csv_location, comp)
		demo_df = pd.read_csv(demo, dtype=str)
		demo_cols.extend([x for x in demo_df.columns.tolist() if (
		    'latency' not in x and 'Unnamed' not in x and 'subj_id' not in x)])
		clin_raw_df = pd.read_csv(clin_raw, dtype=str)
		clin_raw_cols.extend([x for x in clin_raw_df.columns.tolist(
		) if 'latency' not in x and 'end' not in x and 'Unnamed' not in x])
		sum_df = pd.read_csv(sum, dtype=str)
		scored_df = pd.read_csv(scored, dtype=str)
		comp_df = pd.read_csv(composite, dtype=str).rename(
		    index=str, columns={'Unnamed: 0': 'subject'})
	except:
		continue
	break

demo_cols = list(set(demo_cols))
demo_cols = demo_df.columns.tolist()
demo_df[demo_cols]
clin_raw_cols = list(set(clin_raw_cols))
demo_df

for subject in subject_with_tp:
	batch_df = pd.DataFrame()
	batch = str(subject)
	subjid = 'best_' + batch + '_'
	print subjid
	demo = subjid + 'demographics_survey.csv'
	summary = subjid + 'summary.csv'
	end = subjid + 'rey_ant_survey.csv'
	scored = subjid + 'scored_data' + '_' + date + '.csv'
	comp = subjid + 'composite_scores_vakil' + '_' + date + '.csv'
	recency = subjid + 'scored_data_recency' + '_' + date + '.csv'
	primacy = subjid + 'scored_data_primacy' + '_' + date + '.csv'
	try:
		demo = os.path.join(output_csv_location, demo)
		clin_raw = os.path.join(output_csv_location, end)
		sum = os.path.join(output_csv_location, summary)
		scored = os.path.join(output_csv_location, scored)
		composite = os.path.join(output_csv_location, comp)

		demo_df = pd.read_csv(demo, dtype=str)
		primacy = os.path.join(output_csv_location, primacy)
		recency = os.path.join(output_csv_location, recency)
		clin_raw_df = pd.read_csv(clin_raw, dtype=str)
		sum_df = pd.read_csv(sum, dtype=str).rename(
		    index=str, columns={'script.subjectid': 'subject'})
		scored_df = pd.read_csv(scored, dtype=str)
		primacy_df = pd.read_csv(primacy, dtype=str)
		recency_df = pd.read_csv(recency, dtype=str)

		extra_measures = primacy_df.merge(recency_df, on='subj_id', left_index=True, how='left', suffixes=(
		    '_primacy', '_recency')).rename(columns={'subj_id': 'subject'})
		comp_df = pd.read_csv(composite, dtype='str').rename(
		    index=str, columns={'subj_id': 'subject'})
		# comp_df['subject'] = comp_df['subject'].apply(int)

		vmreact_df = pd.merge(scored_df, comp_df, left_index=True,
		                      right_on='subject', how='left').drop('subject', axis=1)
		# vmreact_df['subj_id_x'] = vmreact_df['subj_id_x'].astype(str)

		# vmreact_df['subj_id']=vmreact_df['subj_id'].apply(pd.to_numeric)
		# latency_df = pd.read_csv(latency_csv, dtype=str)
		# latency_df = latency_df.drop_duplicates().reset_index()

		# subject_ids = vmreact_df['subj_id_x'].tolist()
		vmreact_df = vmreact_df.merge(
		    extra_measures, left_on='subj_id_x', right_on='subject').drop('subject', axis=1)

		# batch_demo_cols = [x for x in demo_df.columns.tolist() if x in demo_cols]
		# append_demo_cols = [x for x in demo_cols if x not in demo_df.columns.tolist()]
		# demo_df = demo_df[demo_df['subject'].astype(str).isin(subject_ids)][batch_demo_cols]
		# for col in append_demo_cols:
			# demo_df[col] = np.nan
		#     print demo_df
		#     demo_df['subject']=demo_df['subject'].apply(pd.to_numeric)

		batch_clin_cols = [x for x in clin_raw_df.columns.tolist()
		                                                         if x in clin_raw_cols]
		# append_clin_cols = [x for x in clin_raw_cols if x not in clin_raw_df.columns.tolist()]
		# clin_raw_df = clin_raw_df[clin_raw_df['subject'].astype(str).isin(subject_ids)][batch_clin_cols]

		# for col in sorted(append_clin_cols):
			# clin_raw_df[col] = np.nan
		# clin_raw_df['subject']=clin_raw_df['subject'].apply(pd.to_numeric)

		# batch_sum_cols = [x for x in sum_df.columns.tolist() if x in sum_cols]
		# append_sum_cols = [x for x in sum_cols if x not in sum_df.columns.tolist()]
		# sum_df = sum_df[sum_df['subject'].astype(str).isin(subject_ids)][batch_sum_cols]
		# for col in sorted(append_sum_cols):
			# sum_df[col] = np.nan
		# sum_df['subject']=sum_df['subject'].apply(pd.to_numeric)
		sum_df
		demo_df.columns = [demo_cols]
		batch_df = demo_df.merge(sum_df, left_on='subject', right_on='subject').drop(
		    ['script.startdate', 'script.starttime'], axis=1)
		batch_df = batch_df.merge(clin_raw_df, left_on='subject', right_on='subject').drop(
		    ['date_y', 'time_y', 'group_y', 'build_y'], axis=1)
		batch_df = batch_df.merge(
		    vmreact_df, left_on='subject', right_on='subj_id_x').drop('subj_id_x', axis=1)
		batch_df = batch_df.rename(
		    columns={'date_x': 'date', 'time_x': 'time', 'group_x': 'group', 'build_x': 'build'})

		# latency_df['subjid'] = latency_df['subjid'].astype(str)
		# latency_df['date'] = latency_df['date'].astype(int)
		batch_df['date'] = batch_df['date'].astype(int)

		# latency_df = latency_df.loc[(latency_df['subjid'].isin(
		#     batch_df['subject'].astype(str).tolist()))]  # & latency_df['date'].isin(batch_df['date'].tolist()))]
		#
		# # latency_df = latency_df.loc[(
		# 	latency_df['subjid'].isin(batch_df['subject'].astype(str).tolist()) & latency_df['date'].isin(
		# 		batch_df['date'].tolist()))]

		batch_df['subject'] = batch_df['subject'].astype(str)
		# batch_df = batch_df.merge(latency_df, left_on='subject', right_on='subjid')
		batch_df.to_csv(os.path.join(output_csv_location, prefix +
		                'vmreact_compiled_' + date + '.csv'))
	except:
		print subject
	continue


dataframes_to_concat = []
result = []
for compiled_csv in glob(os.path.join(output_csv_location, '*vmreact*cs v')):
	compiled_df = pd.read_csv(compiled_csv, dtype=str)
	dataframes_to_concat.append(compiled_df)
result = pd.concat(dataframes_to_concat).reindex_axis(compiled_df.columns.tolist(
), axis=1).drop(['Unnamed: 0'], axis=1).dropna(how='all', axis=1).drop_duplicates()

display(result)
result = result.drop_duplicates()
result.to_csv(os.path.join(output_csv_location,
              'vmreact_complete_compilation.csv'), index=False)


def restructure_and_regrade_all_data(scored_dir):

	format = "%Y_%m_%d"
	current_date = datetime.datetime.today()
	date = current_date.strftime(format)

	# demo_cols = []
	# clin_raw_cols = []
	sum_cols = ['script.startdate', 'script.starttime', 'subject', 'computer.platform', 'script.elapsedtime', 'values.demo_completed', 'values.trialcount', 'expressions.overallpercentcorrect', 'expressions.meanRT',
	    'expressions.stdRT', 'expressions.gad_7_total', 'expressions.phq_total', 'expressions.pcl_4_total', 'expressions.pcl_total_hybridscore_corrected', 'expressions.pcl_total_hybridscore_uncorrected']
	scored_cols = ['subj_id', 'list_type', 'listb', 'trial1', 'trial2', 'trial3',
	   'trial4', 'trial5', 'trial6', 'trial7', 'listb_#_repeats', 'trial1_#_repeats', 'trial2_#_repeats',
	   'trial3_#_repeats', 'trial4_#_repeats', 'trial5_#_repeats', 'trial6_#_repeats', 'trial7_#_repeats']
	composite_cols = ['subject', 'total_learning', 'corrected_total_learning', 'learning_rate',
	  'proactive_interference', 'retroactive_interference', 'forgetting_and_retention']

	for raw in glob(os.path.join(os.path.dirname(scored_dir))):
	demo_cols = []
	clin_raw_cols = []
	path = raw.split('/')[-1]
	path = path.split('_')[0:3]
	id = '_'.join(path) + '_inquisit'
	demo = '_'.join(path) + '_demographics_survey.csv'
	summary = '_'.join(path) + '_summary.csv'
	end = '_'.join(path) + '_rey_ant_survey.csv'
	out_dir = scored_dir
	csv_dir = os.path.join(os.path.dirname(scored_dir), 'csv')

	age_range_gender_csv = os.path.join(out_dir, '_'.join(
	    path) + '_subj_age_agerange_gender_new_age_bins_' + date + '.csv')
	scored = os.path.join(out_dir, '_'.join(
	    path) + '_scored_data_' + date + '.csv')
	composite = os.path.join(out_dir, '_'.join(
	    path) + '_composite_scores_vakil_' + date + '.csv')
	primacy = os.path.join(out_dir, '_'.join(
	    path) + '_scored_data_primacy_' + date + '.csv')
	recency = os.path.join(out_dir, '_'.join(
	    path) + '_scored_data_recency_' + date + '.csv')

	demo_df = pd.read_csv(os.path.join(csv_dir, demo), dtype=str)

	demo_cols.extend([x for x in demo_df.columns.tolist()if (
	    'latency' not in x and 'Unnamed' not in x and 'age_textbox' not in x)])
	age_range_df = pd.read_csv(os.path.join(dir, age_range_gender_csv), dtype=str)

	age_range_gender_cols.extend([x for x in age_range_df.columns.tolist() if (
	    'age' not in x and 'subj_id' not in x and 'gender' not in x)])

	clin_raw_df = pd.read_csv(os.path.join(csv_dir, end), dtype=str)

	clin_raw_cols.extend([x for x in clin_raw_df.columns.tolist(
	) if 'latency' not in x and 'end' not in x and 'Unnamed' not in x])

	sumdf = pd.read_csv(os.path.join(csv_dir, summary), dtype=str).rename(
	    index=str, columns={'script.subjectid': 'subject'})
	sum_df = pd.DataFrame(data=sumdf, columns=sum_cols, dtype=str)

	scored_df = pd.read_csv(os.path.join(out_dir, scored), dtype=str)
	comp_df = pd.read_csv(os.path.join(out_dir, composite), dtype=str).rename(
	    index=str, columns={'Unnamed: 0': 'subject'})
	age_range_gender = pd.read_csv(os.path.join(
	    out_dir, age_range_gender_csv), dtype=str)
	primacy_df = pd.read_csv(os.path.join(out_dir, primacy), dtype=str)
	recency_df = pd.read_csv(os.path.join(out_dir, recency), dtype=str)

	demo_cols = list(set(demo_cols))
	clin_raw_cols = list(set(clin_raw_cols))

	extra_measures = primacy_df.merge(recency_df, on='subj_id', left_index=True, how='left', suffixes=(
	    '_primacy', '_recency')).rename(columns={'subj_id': 'subject'})

	comp_df['subject'] = comp_df['subject'].apply(int)

	vmreact_df = pd.merge(scored_df, comp_df, left_index=True,
	                      right_on='subject', how='left').drop('subject', axis=1)
	vmreact_df['subj_id_x'] = vmreact_df['subj_id_x'].astype(str)

	# latency_df = pd.read_csv(latency_csv, dtype=str)
	# latency_df = latency_df.drop_duplicates().reset_index()
	# subject_ids = vmreact_df['subj_id_x'].tolist()
	vmreact_df.rename(columns={'subj_id_x': 'subject'}, inplace=True)
	vmreact_df = vmreact_df.merge(
	    extra_measures, left_on='subject', right_on='subject')

	# batch_clin_cols = [x for x in clin_raw_df.columns.tolist() if x in clin_raw_cols]
	# clin_raw_df = clin_raw_df[clin_raw_df['subject'].astype(str).isin(subject_ids)][batch_clin_cols]

	batch_sum_cols = [x for x in sum_df.columns.tolist() if x in sum_cols]
	# append_sum_cols = [x for x in sum_cols if x not in sum_df.columns.tolist()]
	sum_df = sum_df[sum_df['subject'].astype(str).isin(subject_ids)][batch_sum_cols].drop, axis = 1)

	batch_df=sum_df.merge(demo_df.reset_index(
	), left_on = 'subject', right_on = 'subject', how = 'inner')
	# batch_df = batch_df.rename(columns={'date_x': 'date', 'time_x': 'time', 'group_x': 'group', 'build_x': 'build'})
	batch_df['date']=batch_df['date'].astype(int)
	batch_df['subject']=batch_df['subject'].astype(str)
	print '123'
	batch_df.to_csv(os.path.join(out_dir, '_'.join(
	    path) + '_vmreact_compiled_' + date + '.csv'))

#
scored_dir='/Users/lillyel-said/Desktop/inquisit_renamed/best_1048_tp2_inquisit/out'
restructure_and_regrade_all_data(scored_dir)
# latency_df['subjid'] = latency_df['subjid'].astype(str)
# latency_df['date'] = latency_df['date'].astype(int)

# latency_df = latency_df.loc[(latency_df['subjid'].isin(
	# batch_df['subject'].astype(str).tolist()))]  # & latency_df['date'].isin(batch_df['date'].tolist()))]
#
# latency_df = latency_df.loc[(
#         latency_df['subjid'].isin(batch_df['subject'].astype(str).tolist()) & latency_df['date'].isin(
#     batch_df['date'].tolist()))]

# batch_df = batch_df.merge(latency_df, left_on='subject', right_on='subjid')
