import os
import pandas as pd


def extra_compiled_measures(datadir, compiled_csv, typing_test_csv, average_typing_csv, updated_compilation_csv):
    # data_dir = '/Users/lillyel-said/Desktop/vmreact/vmreact/2_vmreact/'
    # compiled_csv = '/Users/lillyel-said/Desktop/vmreact/vmreact/2_vmreact/mturk_vmreact_complete_compilation_initiation.csv'
    # average_typing_csv= '/Users/lillyel-said/Desktop/vmreact/vmreact/2_vmreact/typing_test_averages.csv'

    trials = ['trial1', 'trial2', 'trial3', 'trial4',
              'trial5', 'listb', 'trial6', 'trial7']

    cols = ['values.response_latency', 'expressions.trial_recall_word_latency',
            'values.recall_firstcharlatency', 'values.recall_lastcharlatency']

    column_titles = ['subjid', 'date']

    incorrect_df = pd.read_csv(os.path.join(
        data_dir, 'incorrect_response.csv'), dtype=str)

    vmreact_df = pd.read_csv(compiled, dtype='str')

    avg_typing_df = pd.read_csv(average_typing_csv, dtype='str')

    vmreact_df['unique_identifier'] = vmreact_df['subject'] + \
        '_' + vmreact_df['date']

    add_avg_typing_merge = vmreact_df.merge(
        avg_typing_df, left_on='unique_identifier', right_on='unique_identifier', how='outer')

    temp = pd.DataFrame(data=add_avg_typing_merge, dtype=str)

    new_compiled["total_average_repeats"] = temp.loc[:, 'listb_#_repeats':'trial7_#_repeats'].astype(float).mean(
        axis=1)

    new_compiled["total_incorrect"] = new_compiled.loc[:,
                                                       'listb':'trial7'].astype(float).subtract(15, axis=0)

    new_compiled[['listb_errors', 'trial1_errors', 'trial2_errors', 'trial3_errors', 'trial4_errors', 'trial5_errors',
                  'trial6_errors', 'trial7_errors']] = new_compiled.loc[:, 'listb':'trial7'].astype(float).subtract(15, axis=0).abs()

    new_compiled.to_csv(os.path.join(updated_compilation_csv,
                                     'updated_mturk_vmreact_complete_compilation.csv'))
