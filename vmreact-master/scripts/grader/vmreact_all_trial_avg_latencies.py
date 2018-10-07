import os
import numpy as np
import pandas as pd
import csv
from glob import glob


def gen_vmreact_latencies(data_dir, output_dir):
    trials = ['trial1', 'trial2', 'trial3', 'trial4',
              'trial5', 'listb', 'trial6', 'trial7']

    cols = ['values.response_latency', 'expressions.trial_recall_word_latency',
            'values.recall_firstcharlatency', 'values.recall_lastcharlatency']

    column_titles = ['subjid', 'timepoint', 'date']

    for trial in trials:
        for meas in cols:
            column_titles.append(trial + "_" + meas)

    final_csv = [column_titles]

    total_columns = []
    for file in glob(os.path.join(data_dir, '*_raw.csv')):
        try:
            datadf = pd.read_csv(file, dtype=str)
            datadf.loc[datadf['response'] == ' ',
                       'trialcode'] = 'trial_confirmation'

            for trial_name in ['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'trial6', 'trial7', 'trial8', 'listb']:
                datadf.loc[data_df['trialcode'].str.contains(
                    trial_name), 'trialcode'] = trial

            datadf.rename(
                columns={'latency': 'values.response_latency'}, inplace=True)

            for col in datadf.columns.tolist():
                if col not in total_columns:
                    total_columns.append(col)
        except:
            continue

    for data_file in glob(os.path.join(data_dir, '*_raw.csv')):
        try:
            data_df = pd.read_csv(data_file, dtype=str)
            data_df.loc[data_df['response'] == ' ',
                        'trialcode'].any() == 'trial_confirmation'

            for trial in ['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'trial6', 'trial7', 'trial8', 'listb']:
                data_df.loc[data_df['trialcode'].str.contains(
                    trial), 'trialcode'] = trial

            data_df.rename(
                columns={'latency': 'values.response_latency'}, inplace=True)

            for subj, subj_df in data_df.groupby(['subject']):
                measures = []
                for trial, trial_df in subj_df.groupby(['trialcode']):
                    if trial in ['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'listb', 'trial6', 'trial7']:
                        trial_measures = [np.nan] * 4
                        for idx, meas in enumerate(cols):
                            try:
                                trial_measures[idx] = round(
                                    trial_df[meas].astype('float').mean(), 4)
                            except:
                                trial_measures[idx] = np.nan
                                continue

                        measures.append([trial] + trial_measures)

                    elif trial == 'trial_confirmation':
                        confirmation_mean = trial_df['values.response_latency'].astype(
                            float).mean()
                        confirmation_vals = trial_df['values.response_latency'].astype(
                            float)

                tp = os.path.basename(data_file).split('_')[2]
                subj_line = [subj, tp, subj_df['date'].unique().astype(str)[0]]

                for trial in ['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'listb', 'trial6', 'trial7']:
                    try:
                        trial_idx = [meas[0] for meas in measures].index(trial)
                        subj_line.extend(measures[int(trial_idx)][1:])
                    except:
                        subj_line.extend(4 * np.nan)
                        continue
            final_csv.append(subj_line)
        except:
            continue
    final_csv_no_duplicates = pd.DataFrame(data=final_csv).drop_duplicates()
    final_csv_no_duplicates.fillna('nan', inplace=True)
    final_csv_no_duplicates.to_csv(os.path.join(
        output_dir, 'best_vmreact_latencies_summary.csv'), index=False, header=False)

# gen_vmreact_latencies(data_dir,output_dir)
