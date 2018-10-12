#!/usr/bin/env python2

import os
import pandas as pd
import numpy as np
from glob import glob
import csv


# defined within th emaster script
# raw_path=''
# output_dir=''
# template_dir=''
# cleaned_dir=''


def ant_extraction_and_latencies(raw_path, output_dir, template_dir, cleaned_dir):

    template1 = os.path.join(template_dir, 'ant_block_1_template.csv')
    template2 = os.path.join(template_dir, 'ant_block_2_template.csv')
    temp_1_df = pd.read_csv(template1, dtype=str)
    temp_2_df = pd.read_csv(template2, dtype=str)

    r1 = map(str, [0, 0, 800, 400, 400, 400, 400, 0, 400, 800])
    r2 = map(str, [400, 800, 0, 800, 800, 400, 400, 800, 0, 0])

    format = "%Y_%m_%d"
    current_date = datetime.datetime.today()
    date = current_date.strftime(format)

    for idx, file in enumerate([f for f in glob(os.path.join(raw_path, '*_raw.csv'))]):
        try:
            subj_id_prefix = os.path.basename(file).split('_')[0:3]
            subj_id_prefix = '_'.join(subj_id_prefix)
            tp = os.path.basename(data_file).split('_')[2]
            raw = pd.read_csv(file, dtype=str)

            ant_r = raw.loc[raw['blockcode'] == 'ANT_R']
            for subj, subj_df in ant_r.groupby(['subject']):
                subj_df_compiled = pd.DataFrame()
                for block, block_df in subj_df.groupby(['values.blockcount']):
                    if (block_df['values.CT_ISI'].values[0:10] == r1).all():
                        block_df_compiled = pd.merge(block_df.reset_index(
                        ), temp_1_df, left_index=True, right_index=True, how="outer")
                    else:
                        block_df_compiled = pd.merge(block_df.reset_index(
                        ), temp_2_df, left_index=True, right_index=True, how="outer")
                    subj_df_compiled = subj_df_compiled.append(
                        block_df_compiled)
                try:
                    print subj_id_prefix + '_antr_raw_data_' + date + '.csv'
                    subj_df_compiled.to_csv(os.path.join(
                        output_dir, subj_id_prefix + '_parsed_raw_antr_data_' + date + '.csv'))
                except:
                    subj_df_compiled.to_csv(os.path.join(
                        output_dir, subj_id_prefix + '_parsed_raw_antr_data_' + date + '.csv'))
        except:
            continue

    all_data = [[]]
    all_data_corr = [[]]
    all_data_acc = [[]]

    for batch_csv in sorted(glob(os.path.join(output_dir, '*antr*.csv'))):
        try:
            subj_id_prefix = os.path.basename(batch_csv).split('_')[0:3]
            subj_id_prefix = '_'.join(subj_id_prefix)
            subj = os.path.basename(batch_csv[:-4])
            subj_df = pd.read_csv(batch_csv, dtype=str)
            tp = os.path.basename(data_file).split('_')[2]

            # Data clean up
            date_administration = subj_df['date'].unique()[0]
            subjid = subj_df['subject'].unique()[0]
            subj_df.loc[subj_df['cue_condition'].str.contains(
                '.invalidspatial'), 'cue_condition'] = 'trial.invalid'
            subj_df.loc[subj_df['cue_condition'].str.contains(
                '.validspatial'), 'cue_condition'] = 'trial.validspatial'
            subj_df.loc[subj_df['cue_condition'] ==
                'trial.nocue', 'cue_target_interval'] = 'NaN'

            results = pd.DataFrame()

            data = subj_df[['subject', 'date', 'location_congruence_val', 'flanker_congruence_val',
                'cue_target_interval', 'cue_condition', 'latency', 'values.correct']]
            data.to_csv(os.path.join(cleaned_dir, subj_id_prefix +
                        '_extracted_antr_raw_data_' + date + '.csv'), index=False)

            print subj_id_prefix
            cols = ['subjid'] + ['tp'] + ['date']
            subj_vals = [subjid] + [tp] + [date_administration]
            subj_vals_corr = [subjid] + [tp] + [date_administration]
            subj_acc = [subjid] + [tp] + [date_administration]

            for bygroup, bygroup_df in subj_df.groupby(['location_congruence_val', 'flanker_congruence_val', 'cue_target_interval', 'cue_condition']):
                cols.append('loc-con-%s_flank-con-%s_cue-int-%s_cue-cond-%s' %
                            (bygroup[0], bygroup[1], bygroup[2], bygroup[3]))
                subj_vals.append(bygroup_df['latency'].mean())
                subj_vals_corr.append(
                    bygroup_df.loc[bygroup_df['values.correct'] == 1, 'latency'].mean())
                subj_acc.append(bygroup_df['values.correct'].mean())
        except:
            print subj, " did not work"
            continue

        all_data[0] = cols
        all_data.append(subj_vals)

        all_data_corr[0] = cols
        all_data_corr.append(subj_vals_corr)

        all_data_acc[0] = cols
        all_data_acc.append(subj_acc)

    with open(os.path.join(output_dir, 'ant-r_summary_latency_corr' + date + '.csv') as f:
        writer=csv.writer(f)
        writer.writerows(all_data)

    with open(os.path.join(output_dir, 'ant-r_summary_latency_corr' + date + '.csv'), 'wb') as f:
        writer=csv.writer(f)
        writer.writerows(all_data_corr)

    with open(os.path.join(output_dir, 'ant-r_summary_acc' + date + '.csv'), 'wb') as f:
        writer=csv.writer(f)
        writer.writerows(all_data_acc)
