#!/usr/bin/env python2

import os
from glob import glob
from shutil import copy, move
import pandas as pd
import numpy as np
from IPython.display import display
from extract_csv_into_dict_fxn import extract_data_from_csv_into_dict

def list_all_output_csv_files(scored_dir):
    list_of_data_files = [f for f in scored_dir if os.path.isfile(
        f) and 'word_correlations' not in os.path.basename(f) and 'parsed' not in os.path.basename(f)]
    return list_of_data_files

# data_files = list_all_output_csv_files(scored_dir)

date_of_scored_files = []
def date_scored(data_files):
    basename_file_for_date = os.path.basename(data_files[0])
    date_scored = '_'.join(
        basename_file_for_date.split('_')[-3:]).split('.')[0]
    return date_scored

    for col in range(0, len(data_files)):
        df = pd.read_csv(data_files[col], dtype=str)
        cols = df.columns.tolist()
        all_cols.extend([df_cols for df_cols in df.columns.tolist()])
        column_list.append(cols)

    for t in trial_list:
        all_cols.extend([t + '_primacy', t + '_recency'])

    all_cols_set = sorted(list(set(all_cols)))
    return all_cols_set

# all_cols = pull_all_column_headers(data_files)

def merge_all_csvs(data_files, date_of_scored_files):

    subj_id = os.path.basename('_'.join(csv_list[0].split('_')[5:9]).split('.')[0])

    demo = os.path.join(csv, subj_id + '_inquisit_demographics_survey.csv')
    summ = os.path.join(csv, subj_id + '_inquisit_summary.csv')
    end = os.path.join(csv, subj_id + '_inquisit_rey_ant_survey.csv')

    scored = os.path.join(dirname, 'scored_data_' +
                          date_of_scored_files[0] + '.csv')
    primacy = os.path.join(dirname, 'scored_data_primacy_' +
                           date_of_scored_files[0] + '.csv')
    recency = os.path.join(dirname, 'scored_data_recency_' +
                           date_of_scored_files[0] + '.csv')
    composite = os.path.join(
        dirname, 'composite_scores_vakil_' + date_of_scored_files[0] + '.csv')

    new_df = pd.DataFrame(dtype=str)
    extra_measures = pd.DataFrame(dtype=str)

    demo_df = pd.read_csv(demo, dtype=str).rename(
        columns={'subject': 'subj_id'})
    sum_df = pd.read_csv(summ, dtype=str).rename(
        columns={'script.subjectid': 'subj_id'})
    end_df = pd.read_csv(end, dtype=str).rename(columns={'subject': 'subj_id'})

    scored_df = pd.read_csv(scored, dtype=str)
    composite_df = pd.read_csv(composite, dtype=str).drop('Unnamed: 0', axis=1)
    primacy_df = pd.read_csv(primacy, dtype=str)
    recency_df = pd.read_csv(recency, dtype=str)

    temp_df = demo_df.merge(sum_df.reset_index(), on='subj_id', how='outer')
    temp_df = temp_df.merge(end_df.reset_index(), on='subj_id', how='outer', copy=False).rename(
        columns={'group_x': 'group', 'date_x': 'date', 'build_x': 'build', 'time_x': 'time'})

    new_df = scored_df.merge(composite_df.reset_index(),
                             on='subj_id', how='outer')
    extra_measures = primacy_df.merge(
        recency_df.reset_index(), on='subj_id', suffixes=('_primacy', '_recency'))
    new_df = new_df.merge(extra_measures.reset_index(),
                          on='subj_id', how='outer')
    new_df = new_df.merge(temp_df.reset_index(), on='subj_id', copy=False).rename(
        columns={'list_type_x': 'list_type'})

    new_df_col=new_df.columns.tolist()
    nolatency=[col for col in new_df_col if 'latency' not in col]
    new_df=new_df[nolatency]
    new_df.to_csv(os.path.join(dirname, subj_id + '_inquisit_compiled.csv'))

    return new_df
