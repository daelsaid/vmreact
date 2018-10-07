
import datetime
from glob import glob
from shutil import copy, move

import pandas as pd
from IPython.display import display
from extract_csv_into_dict_fxn import extract_data_from_csv_into_dict


def set_scored_to_df(scored_dir):
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

    age_range_gender_cols = ['age_range']

    for batch in range(1, 9):
        batch = str(batch)
        demo = os.path.join(scored_dir, 'mturk_batch' + batch + '_demo.csv')
        clin_raw = os.path.join(scored_dir, 'mturk_batch' + batch + '_end.csv')
        summ = os.path.join(scored_dir, 'mturk_batch' + batch + '_summary.csv')
        scored = os.path.join(scored_dir, 'mturk_batch' +
                              batch + '_scored_data.csv')
        composite = os.path.join(
            scored_dir, 'mturk_batch' + batch + '_composite_scores.csv')
        age_range_gender_csv = os.path.join(
            scored_dir, 'mturk_batch' + batch + '_age_range_gender.csv')

        demo_df = pd.read_csv(demo, dtype=str)
        #     demo_cols.extend([x for x in demo_df.columns.tolist() if ('latency' not in x and 'online' not in x and 'Unnamed' not in x and 'time_comp' not in x and 'subj_id' not in x)])
        demo_cols.extend([x for x in demo_df.columns.tolist() if
                          ('latency' not in x and 'Unnamed' not in x and 'subj_id' not in x and 'age_textbox')])
        print batch
        age_range_df = pd.read_csv(age_range_gender_csv)
        age_range_gender_cols.extend(
            [x for x in age_range_df.columns.tolist() if ('age' not in x and 'subj_id' not in x and 'gender' not in x)])
        clin_raw_df = pd.read_csv(clin_raw, dtype=str)
        clin_raw_cols.extend(
            [x for x in clin_raw_df.columns.tolist() if 'latency' not in x and 'end' not in x and 'Unnamed' not in x])
        sum_df = pd.read_csv(summ, dtype=str)
        scored_df = pd.read_csv(scored, dtype=str)
        comp_df = pd.read_csv(composite, dtype=str).rename(
            index=str, columns={'Unnamed: 0': 'subject'})
        age_range_gender = pd.read_csv(age_range_gender_csv, dtype=str)

    demo_cols = list(set(demo_cols))
    clin_raw_cols = list(set(clin_raw_cols))

    return demo_cols, clin_raw_cols


# need to get latency values,
# use the scored to set the subject ids.
# append composite to scored_cols since they're in the same order and composite doesn't have subject ids
# summary - use script.subjectid
# demo - use subject
# clin_raw - use subject

# In[ ]:


import numpy as np

scored_dir = '/Users/lillyel-said/Desktop/vmreact/vmreact/2_vmreact/'
latency_csv = os.path.join(scored_dir, 'vmreact_latency_summary.csv')


def batch_merge(scored_dir, latency_csv):
    for batch in range(1, 9):
        # for batch in [8]:
        batch_df = pd.DataFrame()
        batch = str(batch)
        print 'mturk_batch' + batch

        demo = os.path.join(scored_dir, 'mturk_batch' + batch + '_demo.csv')
        clin_raw = os.path.join(scored_dir, 'mturk_batch' + batch + '_end.csv')
        sum = os.path.join(scored_dir, 'mturk_batch' + batch + '_summary.csv')
        scored = os.path.join(scored_dir, 'mturk_batch' +
                              batch + '_scored_data.csv')
        primacy = os.path.join(scored_dir, 'mturk_batch' +
                               batch + '_scored_data_primacy.csv')
        recency = os.path.join(scored_dir, 'mturk_batch' +
                               batch + '_scored_data_recency.csv')
        composite = os.path.join(
            scored_dir, 'mturk_batch' + batch + '_composite_scores.csv')

        demo_df = pd.read_csv(demo, dtype=str)
        clin_raw_df = pd.read_csv(clin_raw, dtype=str)
        sum_df = pd.read_csv(sum, dtype=str).rename(
            index=str, columns={'script.subjectid': 'subject'})
        scored_df = pd.read_csv(scored)

        primacy_df = pd.read_csv(primacy, dtype=str)
        recency_df = pd.read_csv(recency, dtype=str)

        extra_measures = primacy_df.merge(recency_df, on='subj_id', left_index=True, how='left',
                                          suffixes=('_primacy', '_recency')).rename(columns={'subj_id': 'subject'})
        comp_df = pd.read_csv(composite).rename(
            index=str, columns={'Unnamed: 0': 'subject'})
        comp_df['subject'] = comp_df['subject'].apply(int)

        vmreact_df = pd.merge(scored_df, comp_df, left_index=True, right_on='subject', how='left').drop('subject',
                                                                                                        axis=1)
        vmreact_df['subj_id'] = vmreact_df['subj_id'].astype(str)

        # vmreact_df['subj_id']=vmreact_df['subj_id'].apply(pd.to_numeric)
        latency_df = pd.read_csv(latency_csv, dtype=str)
        latency_df = latency_df.drop_duplicates().reset_index()

        subject_ids = vmreact_df['subj_id'].tolist()

        vmreact_df = vmreact_df.merge(
            extra_measures, left_on='subj_id', right_on='subject').drop('subject', axis=1)

        batch_demo_cols = [
            x for x in demo_df.columns.tolist() if x in demo_cols]
        append_demo_cols = [
            x for x in demo_cols if x not in demo_df.columns.tolist()]
        demo_df = demo_df[demo_df['subject'].astype(
            str).isin(subject_ids)][batch_demo_cols]

        for col in append_demo_cols:
            demo_df[col] = np.nan
        #     print demo_df
        #     demo_df['subject']=demo_df['subject'].apply(pd.to_numeric)

        batch_clin_cols = [
            x for x in clin_raw_df.columns.tolist() if x in clin_raw_cols]
        append_clin_cols = [
            x for x in clin_raw_cols if x not in clin_raw_df.columns.tolist()]
        clin_raw_df = clin_raw_df[clin_raw_df['subject'].astype(
            str).isin(subject_ids)][batch_clin_cols]
        for col in sorted(append_clin_cols):
            clin_raw_df[col] = np.nan
        # clin_raw_df['subject']=clin_raw_df['subject'].apply(pd.to_numeric)

        batch_sum_cols = [x for x in sum_df.columns.tolist() if x in sum_cols]
        append_sum_cols = [
            x for x in sum_cols if x not in sum_df.columns.tolist()]
        sum_df = sum_df[sum_df['subject'].astype(
            str).isin(subject_ids)][batch_sum_cols]
        for col in sorted(append_sum_cols):
            sum_df[col] = np.nan
        # sum_df['subject']=sum_df['subject'].apply(pd.to_numeric)

        batch_df = demo_df.merge(sum_df, left_on='subject', right_on='subject').drop(
            ['script.startdate', 'script.starttime'], axis=1)
        batch_df = batch_df.merge(clin_raw_df, left_on='subject', right_on='subject').drop(
            ['date_y', 'time_y', 'group_y', 'build_y'], axis=1)
        batch_df = batch_df.merge(
            vmreact_df, left_on='subject', right_on='subj_id').drop('subj_id', axis=1)
        batch_df = batch_df.rename(
            columns={'date_x': 'date', 'time_x': 'time', 'group_x': 'group', 'build_x': 'build'})
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
        batch_df = batch_df.merge(
            latency_df, left_on='subject', right_on='subjid')

        batch_df.to_csv(os.path.join(
            scored_dir, 'mturk_batch' + batch + '_compiled.csv'))
        #     os.system('open /Users/cdla/Desktop/scratch/vmreact/2_vmreact/'+'mturk_batch'+batch+'_compiled.csv')
        return batch_df

# concat all merged df csvs to 1 final compiled csv


def conc_all_merged_df(compiled_csv):
    dataframes_to_concat = []
    result = []
    for compiled_csv in glob(os.path.join(scored_dir, '*compiled.csv')):
        df = pd.read_csv(compiled_csv, dtype=str)
        dataframes_to_concat.append(df)

    result = pd.concat(dataframes_to_concat).reindex_axis(df.columns.tolist(), axis=1).drop(
        ['index', 'date_y', 'subjid', 'Unnamed: 0'], axis=1).dropna(how='all', axis=1).drop_duplicates()

    # print result.subject
    result = result[~result.subject.isin(
        ['XXX', 'AVD6HMIO1HLFI', 'A5EU1AQJNC7F2'])]
    result.drop_duplicates(['date_x', 'subject'], inplace=True)
    display(result)
    result = result.drop_duplicates()
    result.to_csv(os.path.join(
        scored_dir, 'mturk_vmreact_complete_compilation.csv'), index=False)
    return result
