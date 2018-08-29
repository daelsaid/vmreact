from glob import glob
import os
import datetime
import pandas as pd

format = "%Y_%m_%d"
current_date = datetime.datetime.today()
date = current_date.strftime(format)


def best_rename_with_subj(subj_dir):
	files=glob(os.path.join(subj_dir,'*.csv'))

	for file in range(0,len(files)):
		fullpath=files[file]
		fname=os.path.basename(fullpath)
		path=os.path.dirname(fullpath)
		old=os.path.join(path,fname)
		prefix_id=fullpath.split('/')[-3]
		new=os.path.join(path,'best_'+prefix_id.split('_')[1]+'_'+prefix_id.split('_')[2]+'_'+fname)
		try:
			os.rename(old,new)
		except OSError:
			print 'file note found:', old



# def set_scored_to_df(scored_dir,main_dir):
# 	demo_cols = []
# 	clin_raw_cols = []
# 	sum_cols = ['script.startdate', 'script.starttime', 'subject',
# 	'expressions.gad_7_total', 'expressions.phq_total', 'expressions.pcl_4_total',
# 	'expressions.pcl_total_hybridscore_corrected', 'expressions.pcl_total_hybridscore_uncorrected']
# 	scored_cols = ['subj_id', 'list_type', 'listb', 'trial1', 'trial2', 'trial3',
# 	'trial4', 'trial5', 'trial6', 'trial7', 'listb_#_repeats', 'trial1_#_repeats', 'trial2_#_repeats',
# 	'trial3_#_repeats', 'trial4_#_repeats', 'trial5_#_repeats', 'trial6_#_repeats', 'trial7_#_repeats']
# 	composite_cols = ['subject', 'total_learning', 'corrected_total_learning', 'learning_rate',
# 	'proactive_interference', 'retroactive_interference', 'forgetting_and_retention']
#
# 	age_range_gender_cols = ['age_range']
# 	csv_dir=os.path.join(main_dir,'csv')
# 	subj=csv_dir.split('/')[-2]
# 	print subj
#
# 	for f in glob(os.path.join(scored_dir,'*.csv')):
# 		id=f.split('/')[-2]
# 		# subj_id='best_'+id.split('_')[1]+'_'+id.split('_')[2]
# 		subj_id=subj
#
# 		demo = os.path.join(csv_dir,subj_id+'_demographics_survey.csv')
# 		clin_raw = os.path.join(csv_dir,'csv',subj_id+'_rey_ant_survey.csv')
# 		sum = os.path.join(csv_dir,'csv',subj_id+'_summary.csv')
# 		scored = os.path.join(scored_dir, 'scored_data' + '_' + date + '.csv')
# 		primacy = os.path.join(scored_dir,'parsed_raw_data_primacy' + '_' + date + '.csv')
# 		recency = os.path.join(scored_dir,'parsed_raw_data_recency' + '_' + date + '.csv')
# 		composite = os.path.join(scored_dir, 'composite_scores_vakil' + '_' + date + '.csv')
# 		age_range_gender_csv = os.path.join(scored_dir, 'subj_age_agerange_gender_new_age_bins'+date+'.csv')
#
# 		demo_df = pd.read_csv(demo, dtype=str)
# 		demo_cols.extend([x for x in demo_df.columns.tolist() if ('latency' not in x and 'Unnamed' not in x and 'subj_id' not in x and 'age_textbox')])
#
# 		age_range_df = pd.read_csv(age_range_gender_csv)
# 		age_range_gender_cols.extend([x for x in age_range_df.columns.tolist() if ('age' not in x and 'subj_id' not in x and 'gender' not in x)])
# 		clin_raw_df = pd.read_csv(clin_raw, dtype=str)
# 		clin_raw_cols.extend([x for x in clin_raw_df.columns.tolist() if 'latency' not in x and 'end' not in x and 'Unnamed' not in x])
# 		sum_df = pd.read_csv(summ, dtype=str)
# 		scored_df = pd.read_csv(scored, dtype=str)
# 		comp_df = pd.read_csv(composite, dtype=str).rename(index=str, columns={'Unnamed: 0': 'subject'})
# 		age_range_gender = pd.read_csv(age_range_gender_csv, dtype=str)
# 		primacy_df = pd.read_csv(primacy, dtype=str)
# 		recency_df = pd.read_csv(recency, dtype=str)
#
# 		demo_cols = list(set(demo_cols))
# 		clin_raw_cols = list(set(clin_raw_cols))
#
# 		extra_measures = primacy_df.merge(recency_df, on='subj_id', left_index=True, how='left',
# 		suffixes=('_primacy', '_recency')).rename(columns={'subj_id': 'subject'})
# 		comp_df = pd.read_csv(composite).rename(index=str, columns={'Unnamed: 0': 'subject'})
# 		comp_df['subject'] = comp_df['subject'].apply(int)
#
# 		vmreact_df = pd.merge(scored_df, comp_df, left_index=True, right_on='subject', how='left').drop('subject',
# 		axis=1)
# 		vmreact_df['subj_id'] = vmreact_df['subj_id'].astype(str)
#
# 		# vmreact_df['subj_id']=vmreact_df['subj_id'].apply(pd.to_numeric)
# 		latency_df = pd.read_csv(latency_csv, dtype=str)
# 		latency_df = latency_df.drop_duplicates().reset_index()
#
# 		subject_ids = vmreact_df['subj_id'].tolist()
#
# 		vmreact_df = vmreact_df.merge(extra_measures, left_on='subj_id', right_on='subject').drop('subject', axis=1)
#
# 		batch_demo_cols = [x for x in demo_df.columns.tolist() if x in demo_cols]
# 		append_demo_cols = [x for x in demo_cols if x not in demo_df.columns.tolist()]
# 		demo_df = demo_df[demo_df['subject'].astype(str).isin(subject_ids)][batch_demo_cols]
#
# 		for col in append_demo_cols:
# 			demo_df[col] = np.nan
# 			#     print demo_df
# 			#     demo_df['subject']=demo_df['subject'].apply(pd.to_numeric)
#
# 		batch_clin_cols = [x for x in clin_raw_df.columns.tolist() if x in clin_raw_cols]
# 		append_clin_cols = [x for x in clin_raw_cols if x not in clin_raw_df.columns.tolist()]
# 		clin_raw_df = clin_raw_df[clin_raw_df['subject'].astype(str).isin(subject_ids)][batch_clin_cols]
# 		for col in sorted(append_clin_cols):
# 			clin_raw_df[col] = np.nan
# 			# clin_raw_df['subject']=clin_raw_df['subject'].apply(pd.to_numeric)
#
# 		batch_sum_cols = [x for x in sum_df.columns.tolist() if x in sum_cols]
# 		append_sum_cols = [x for x in sum_cols if x not in sum_df.columns.tolist()]
# 		sum_df = sum_df[sum_df['subject'].astype(str).isin(subject_ids)][batch_sum_cols]
# 		for col in sorted(append_sum_cols):
# 			sum_df[col] = np.nan
# 					# sum_df['subject']=sum_df['subject'].apply(pd.to_numeric)
#
# 		batch_df = demo_df.merge(sum_df, left_on='subject', right_on='subject').drop(
# 		['script.startdate', 'script.starttime'], axis=1)
# 		batch_df = batch_df.merge(clin_raw_df, left_on='subject', right_on='subject').drop(
# 		['date_y', 'time_y', 'group_y', 'build_y'], axis=1)
# 		batch_df = batch_df.merge(vmreact_df, left_on='subject', right_on='subj_id').drop('subj_id', axis=1)
# 		batch_df = batch_df.rename(columns={'date_x': 'date', 'time_x': 'time', 'group_x': 'group', 'build_x': 'build'})
# 		# print batch_df
#
# 		print subject_ids
# 					# latency_df['subjid'] = latency_df['subjid'].astype(str)
# 					# latency_df['date'] = latency_df['date'].astype(int)
# 					# batch_df['date'] = batch_df['date'].astype(int)
# 					#
# 					# latency_df = latency_df.loc[(latency_df['subjid'].isin(
# 					# 	batch_df['subject'].astype(str).tolist()))]  # & latency_df['date'].isin(batch_df['date'].tolist()))]
# 					#
# 					# latency_df = latency_df.loc[(
# 					# 		latency_df['subjid'].isin(batch_df['subject'].astype(str).tolist()) & latency_df['date'].isin(
# 					# 	batch_df['date'].tolist()))]
#
# 		batch_df['subject'] = batch_df['subject'].astype(str)
# 		# batch_df = batch_df.merge(latency_df, left_on='subject', right_on='subjid')
#
# 		batch_df.to_csv(os.path.join(scored_dir,subj_id+ '_compiled.csv'))
# 		return batch_df
#
#
# # def compiled_columns(scored_dir,main_dir):
# 	demo_cols = []
# 	clin_raw_cols = []
# 	scored=scored_dir
# 	sum_cols = ['script.startdate', 'script.starttime', 'subject',
# 				'expressions.gad_7_total', 'expressions.phq_total', 'expressions.pcl_4_total',
# 				'expressions.pcl_total_hybridscore_corrected', 'expressions.pcl_total_hybridscore_uncorrected']
# 	scored_cols = ['subj_id', 'list_type', 'listb', 'trial1', 'trial2', 'trial3',
# 				   'trial4', 'trial5', 'trial6', 'trial7', 'listb_#_repeats', 'trial1_#_repeats', 'trial2_#_repeats',
# 				   'trial3_#_repeats', 'trial4_#_repeats', 'trial5_#_repeats', 'trial6_#_repeats', 'trial7_#_repeats']
# 	composite_cols = ['subject', 'total_learning', 'corrected_total_learning', 'learning_rate',
# 					  'proactive_interference', 'retroactive_interference', 'forgetting_and_retention']
# 	age_range_gender_cols = ['age_range']
# 	csv_dir=os.path.join(main_dir,'csv')
#
# 	for f in glob(os.path.join(scored_dir,'*.csv')):
# 		id=f.split('/')[-2]
# 		print id
#
# 		subj_id='best_'+id.split('_')[1]+'_'+id.split('_')[2]
# 		print subj_id
# 		demo_csv=os.path.join(csv_dir,subj_id+'_demographics_survey.csv')
# 		clin_raw_csv=os.path.join(csv_dir,'csv',subj_id+'_rey_ant_survey.csv')
# 		summ=os.path.join(csv_dir,'csv',subj_id+'_summary.csv')
#
# 		demo_df=pd.read_csv(demo_csv,dtype=str)
# 		clin_raw_df=pd.read_csv(clin_raw_csv,dtype=str)
# 		age_range_df = pd.read_csv(os.path.join(scored_dir,id,'out','subj_age_agerange_gender_new_age_bins' + '_' + date + '.csv'),dtype=str)
#
# 		demo_cols.extend([x for x in demo_df.columns.tolist() if ('latency' not in x and 'Unnamed' not in x and 'subj_id' not in x and 'age_textbox')])
#
# 		age_range_gender_cols.extend([x for x in age_range_df.columns.tolist() if ('age' not in x and 'subj_id' not in x and 'gender' not in x)])
#
# 		clin_raw_cols.extend([x for x in clin_raw_df.columns.tolist() if 'latency' not in x and 'end' not in x and 'Unnamed' not in x])
	# 	sum_df=pd.read_csv(summ,dtype=str).rename(index=str, columns={'script.subjectid': 'subject'})
	# 	scored_df= pd.read_csv(os.path.join(scored_dir, 'scored_data' + '_' + date + '.csv'),dtype=str)
	# 	composite_df = pd.read_csv(os.path.join(scored_dir, 'composite_scores_vakil' + '_' + date + '.csv'),dtype=str)
	# 	primacy_df= pd.read_csv(os.path.join(scored_dir, 'parsed_raw_data_primacy' + '_' + date + '.csv'),dtype=str)
	# 	recency_df=pd.read_csv(os.path.join(scored_dir,'parsed_raw_data_recency' + '_' + date + '.csv'),dtype=str)
	#
	#
	# demo_cols = list(set(demo_cols))
	# clin_raw_cols = list(set(clin_raw_cols))
	# # return demo_df,sum_df,scored_df,primacy_df,recency_df,composite_df,subj_id,id,age_range_df,clin_raw_df,subj_id,id
	#
	# def batch_merge(scored,demo_df,sum_df,scored_df,primacy_df,recency_df,composite_df,subj_id,id,age_range_df,clin_raw_df):
	# 	batch_df = pd.DataFrame()
	# 	extra_measures = primacy_df.merge(recency_df, on='subj_id', left_index=True, how='left',suffixes=('_primacy', '_recency')).rename(columns={'subj_id': 'subject'})
	# 	comp_df = pd.read_csv(composite).rename(index=str, columns={'Unnamed: 0': 'subject'})
	# 	comp_df['subject'] = comp_df['subject'].apply(int)
	# 	vmreact_df = pd.merge(scored_df, comp_df, left_index=True, right_on='subject', how='left').drop('subject',axis=1)
	# 	vmreact_df['subj_id'] = vmreact_df['subj_id'].astype(str)
	# 	vmreact_df['subj_id']=vmreact_df['subj_id'].apply(pd.to_numeric)
	# 	# latency_df = pd.read_csv(latency_csv, dtype=str)
	# 	# latency_df = latency_df.drop_duplicates().reset_index()
	# 	subject_ids = vmreact_df['subj_id'].tolist()
	#
	# 	vmreact_df = vmreact_df.merge(extra_measures, left_on='subj_id', right_on='subject').drop('subject', axis=1)
	#
	# 	batch_demo_cols = [x for x in demo_df.columns.tolist() if x in demo_cols]
	# 	append_demo_cols = [x for x in demo_cols if x not in demo_df.columns.tolist()]
	# 	demo_df = demo_df[demo_df['subject'].astype(str).isin(subject_ids)][batch_demo_cols]
	#
	# 	print demo_df.head()
	#
	# 	# demo_df['subject']=demo_df['subject'].apply(pd.to_numeric)
	#
	# 	for col in append_demo_cols:
	# 		demo_df[col] = np.nan
	#
	# 	batch_clin_cols = [x for x in clin_raw_df.columns.tolist() if x in clin_raw_cols]
	# 	append_clin_cols = [x for x in clin_raw_cols if x not in clin_raw_df.columns.tolist()]
	# 	clin_raw_df = clin_raw_df[clin_raw_df['subject'].astype(str).isin(subject_ids)][batch_clin_cols]
	#
	# 	for col in sorted(append_clin_cols):
	# 		clin_raw_df[col] = np.nan
	# 	# clin_raw_df['subject']=clin_raw_df['subject'].apply(pd.to_numeric)
	#
	# 	batch_sum_cols = [x for x in sum_df.columns.tolist() if x in sum_cols]
	# 	append_sum_cols = [x for x in sum_cols if x not in sum_df.columns.tolist()]
	# 	sum_df = sum_df[sum_df['subject'].astype(str).isin(subject_ids)][batch_sum_cols]
	#
	# 	for col in sorted(append_sum_cols):
	# 		sum_df[col] = np.nan
	# 	# sum_df['subject']=sum_df['subject'].apply(pd.to_numeric)
	#
	# 	batch_df = demo_df.merge(sum_df, left_on='subject', right_on='subject').drop(['script.startdate', 'script.starttime'], axis=1)
	# 	batch_df = batch_df.merge(clin_raw_df, left_on='subject', right_on='subject').drop(['date_y', 'time_y', 'group_y', 'build_y'], axis=1)
	# 	batch_df = batch_df.merge(vmreact_df, left_on='subject', right_on='subj_id').drop('subj_id', axis=1)
	# 	batch_df = batch_df.rename(columns={'date_x': 'date', 'time_x': 'time', 'group_x': 'group', 'build_x': 'build'})
	#
	# 	batch_df['subject'] = batch_df['subject'].astype(str)
	#
	# 	batch_df.to_csv(os.path.join(scored_dir,id,subj_id+'_compiled.csv'))
	# 	os.system('open os.path.join(/Users/lillyel-said/Desktop/inquisit_renamed/',id,subj_id+'_compiled.csv')
	# 	return batch_df
	#
	# batch_merge(scored,demo_df,sum_df,scored_df,primacy_df,recency_df,composite_df,subj_id,id,age_range_df,clin_raw_df)
# def organize_columns_merge_csvs(scored_dir,csv_dir):
	# global demo_df,sum_df,scored_df,primacy_df,recency_df,composite_df,subj_id,id,age_range_df,clin_raw_df,subj_id,id
	# f1=compiled_columns(scored_dir,csv_dir)
	# f2=batch_merge(scored_dir,csv_dir)
	# return f2#

# organize_columns_merge_csvs(scored_dir,csv_dir)

	# batch_df = batch_df.merge(latency_df, left_on='subject', right_on='subjid')
	# print batch_df

	# latency_df['subjid'] = latency_df['subjid'].astype(str)
	# latency_df['date'] = latency_df['date'].astype(int)
	# batch_df['date'] = batch_df['date'].astype(int)

	# latency_df = latency_df.loc[(latency_df['subjid'].isin(
	# 	batch_df['subject'].astype(str).tolist()))]  # & latency_df['date'].isin(batch_df['date'].tolist()))]
	#
	# latency_df = latency_df.loc[(
	# 		latency_df['subjid'].isin(batch_df['subject'].astype(str).tolist()) & latency_df['date'].isin(
	# 	batch_df['date'].tolist()))]
