
import datetime
from glob import glob
import pandas as pd
import os
import numpy as np


# scored_dir='/Users/lillyel-said/Desktop/inquisit_renamed/t1/best_1094_tp1_inquisit/out'

def restructure_and_regrade_all_data(scored_dir):
    format = "%Y_%m_%d"
    current_date = datetime.datetime.today()
    date = current_date.strftime(format)

    demo_cols = ['subject', 'time', 'build', 'date', 'education_response', 'educationother_response', 'ethnicity_response', 'gender_response', 'genderother_response', 'group', 'handedness_response', 'native_english_response', 'online_sr_q1option1_response', 'online_sr_q1option2_response', 'online_sr_q1option3_reponse', 'online_sr_q1option4_response', 'online_sr_q1option5_response', 'online_sr_q1option6_response', 'online_sr_q1option7_response','online_sr_q2option1_response', 'online_sr_q2option2_response', 'online_sr_q2option3_response', 'online_sr_q3_response',online_sr_q4option1_response','online_sr_q4option2_response','online_sr_q4option3_response','online_sr_q4option4_response', 'online_sr_q4option5_response','online_sr_q4option6_response', 'online_sr_q4option7_response','online_sr_q4other_response', 'online_sr_q5_response','raceoriginoption1_response', 'raceoriginoption2_response','raceoriginoption3_response', 'raceoriginoption4_response','raceoriginoption5_response', 'raceoriginoption6_response','region_response', 'regionother_response', 'task_location_response','task_locationother_response', 'time_comp_response', 'veteran_response']

    clin_raw_cols = []
    sum_cols = ['script.startdate', 'script.starttime', 'subject',
                'expressions.gad_7_total', 'expressions.phq_total', 'expressions.pcl_4_total',
                'expressions.pcl_total_hybridscore_corrected', 'expressions.pcl_total_hybridscore_uncorrected']

    scored_cols = ['subj_id', 'list_type', 'listb', 'trial1', 'trial2', 'trial3',
                   'trial4', 'trial5', 'trial6', 'trial7', 'listb_#_repeats', 'trial1_#_repeats', 'trial2_#_repeats',
                   'trial3_#_repeats', 'trial4_#_repeats', 'trial5_#_repeats', 'trial6_#_repeats', 'trial7_#_repeats']

    composite_cols = ['subject', 'total_learning', 'corrected_total_learning', 'learning_rate',
                      'proactive_interference', 'retroactive_interference', 'forgetting_and_retention']

    df = pd.DataFrame(dtype=str, columns=demo_cols)
    for raw in glob('/Users/lillyel-said/Desktop/inquisit_renamed/t1/*raw.csv'):
        # for raw in glob(os.path.join(os.path.dirname(scored_dir))):
        print raw
        path = raw.split('/')[-1]
        path = path.split('_')[0:3]
        id = '_'.join(path) + '_inquisit'
        demo = '_'.join(path) + '_demographics_survey.csv'
        summary = '_'.join(path) + '_summary.csv'
        end = '_'.join(path) + '_rey_ant_survey.csv'
        print path, id  # out_dir = scored_dir
        # print out_dir
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

        demodf = pd.read_csv(os.path.join(csv_dir, demo), dtype=str)

        # demo_cols.extend([x for x in demo_df.columns.tolist() if ('latency' not in x and 'Unnamed' not in x and  'age_textbox' not in x )])

        age_range_df = pd.read_csv(os.path.join(
            dir, age_range_gender_csv), dtype=str)

        clin_raw_df = pd.read_csv(os.path.join(csv_dir, end), dtype=str)

        clin_raw_cols.extend([x for x in clin_raw_df.columns.tolist(
        ) if 'latency' not in x and 'end' not in x and 'Unnamed' not in x])

        sum_df = pd.read_csv(os.path.join(csv_dir, summary), dtype=str).rename(
            index=str, columns={'script.subjectid': 'subject'})
        scored_df = pd.read_csv(os.path.join(out_dir, scored), dtype=str)
        comp_df = pd.read_csv(os.path.join(out_dir, composite), dtype=str).rename(
            index=str, columns={'Unnamed: 0': 'subject'})
        age_range_gender = pd.read_csv(os.path.join(
            out_dir, age_range_gender_csv), dtype=str)
        primacy_df = pd.read_csv(os.path.join(out_dir, primacy), dtype=str)
        recency_df = pd.read_csv(os.path.join(out_dir, recency), dtype=str)

        demo_cols = list(set(demo_cols))
        clin_raw_cols = list(set(clin_raw_cols))

        df = primacy_df.merge(recency_df, on='subj_id', left_index=True, how='left', suffixes=(
            '_primacy', '_recency')).rename(columns={'subj_id': 'subject'})
        comp_df['subject'] = comp_df['subject'].apply(int)

        vmreact_df = pd.merge(scored_df, comp_df, left_index=True,
                              right_on='subject', how='left').drop('subject', axis=1)
        vmreact_df['subj_id_x'] = vmreact_df['subj_id_x'].astype(str)

        # latency_df = pd.read_csv(latency_csv, dtype=str)
        # latency_df = latency_df.drop_duplicates().reset_index()
        subject_ids = vmreact_df['subj_id_x'].tolist()
        vmreact_df.merge(df, left_on='subj_id_x', right_on='subject')
        vmreact_df = vmreact_df.merge(
            extra_measures, left_on='subj_id_x', right_on='subject').drop('subject', axis=1)
        # print vmreact_df

        vmreact_df = demo_df.merge(vmreact_df.astype(
            str), left_on='subject', right_on='subj_id_x', how='left')
        print vmreact_df.astype(str)
        batch_clin_cols = [
            x for x in clin_raw_df.columns.tolist() if x in clin_raw_cols]
        clin_raw_df = clin_raw_df[clin_raw_df['subject'].astype(
            str).isin(subject_ids)][batch_clin_cols]

        batch_sum_cols = [x for x in sum_df.columns.tolist() if x in sum_cols]
        # append_sum_cols = [x for x in sum_cols if x not in sum_df.columns.tolist()]
        # sum_df = sum_df[sum_df['subject'].astype(str).isin(subject_ids)][batch_sum_cols].drop(['script.startdate', 'script.starttime'], axis=1)
        vmreact_df.merge(sum_df, left_on='subject', right_on='subject', how='left').to_csv(
            os.path.join(out_dir, '_'.join(path) + '_vmreact_compiled_' + date + '.csv'))
        # batch_df = batch_df.rename(columns={'date_x': 'date', 'time_x': 'time', 'group_x': 'group', 'build_x': 'build'})
        batch_df['date'] = batch_df['date'].astype(int)
        batch_df['subject'] = batch_df['subject'].astype(str)
        print '123'
        batch_df

#
# scored_dir='/Users/lillyel-said/Desktop/inquisit_renamed/t1/best_1048_tp2_inquisit/out'
# restructure_and_regrade_all_data(scored_dir)
# latency_df['subjid'] = latency_df['subjid'].astype(str)
# latency_df['date'] = latency_df['date'].astype(int)

# latency_df = latency_df.loc[(latency_df['subjid'].isin(
    # batch_df['subject'].astype(str).tolist()))]  # & latency_df['date'].isin(batch_df['date'].tolist()))]
#
# latency_df = latency_df.loc[(
#         latency_df['subjid'].isin(batch_df['subject'].astype(str).tolist()) & latency_df['date'].isin(
#     batch_df['date'].tolist()))]

# batch_df = batch_df.merge(latency_df, left_on='subject', right_on='subjid')
