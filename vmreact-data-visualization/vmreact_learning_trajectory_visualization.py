#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 17:09:19 2018

@author: dawlat_local
"""
import pandas
import matplotlib.pyplot as plt
from prettyplotlib import brewer2mpl
import prettyplotlib as ppl
from matplotlib.backends.backend_pdf import PdfPages

set2 = brewer2mpl.get_map('Set2', 'qualitative', 8).mpl_colors
set1 = brewer2mpl.get_map('Set1', 'qualitative', 9).mpl_colors
bmap = brewer2mpl.get_map('Dark2', 'Qualitative', 4).mpl_colors
mpl.rcParams['axes.color_cycle'] = bmap

# scored csv
patient_scored = pandas.read_csv('')
test_df = patient_scored.loc[:, 'subj_id':'trial7'].dropna()

pt_all_trials = pandas.DataFrame(data=patient_scored.set_index(
    'subj_id').loc[:, 'trial1':'trial7']).dropna().astype(int)
pt_learning_trials = pandas.DataFrame(data=patient_scored.set_index(
    'subj_id').loc[:, 'trial1':'trial5']).dropna().astype(int)

# tp1 tp2 composite scores
comp = ['total_learning', 'corrected_total_learning', 'learning_rate',
        'proactive_interference', 'retroactive_interference', 'forgetting_and_retention']
comp_2 = ['total_learning_2', 'corrected_total_learning_2', 'learning_rate_2',
          'proactive_interference_2', 'retroactive_interference_2', 'forgetting_and_retention_2']

# tp1 tp2 scored data
y = ['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'listb', 'trial6', 'trial7', 'total_learning',
     'corrected_total_learning', 'learning_rate', 'proactive_interference', 'retroactive_interference', 'forgetting_and_retention']
y_2 = ['trial1_2', 'trial2_2', 'trial3_2', 'trial4_2',
       'trial5_2', 'listb_2', 'trial6_2', 'trial7_2']

columns = [c for c in y[0:6]]
columns = [c for c in comp]
columns_2 = [c for c in comp_2]

plt.cla()
plt.clf()
plt.close()


with PdfPages('/Users/lillyel-said/Desktop/tp1_tp2_patient_learning_trajectories.pdf') as pdf:
    for index, value in test_df.groupby('subj_id'):
        val = value.loc[:, 'trial1':'trial7']
        fig, axes = plt.subplots(nrows=1, ncols=1)
        color = 'blue'
        fig = pt_all_trials.loc[index][y_2].plot(ax=axes, y=y_2, subplots=True, fontsize=14, grid=True, yticks=range(
            0, 16), ylim=(0, 16), xticks=range(0, 8), xlim=(-0.20, 7.2), color=color, marker='o', linewidth=3.0, markersize=3.5)
        fig2 = pt_all_trials.loc[index][y].plot(ax=axes, y=y, subplots=True, fontsize=14, grid=True, yticks=range(
            0, 16), ylim=(0, 16), xticks=range(0, 8), xlim=(-0.20, 7.2), marker='o', linewidth=3.0, markersize=3.5)
        title = 'Learning Trajectory for Pt: ' + \
            str(index.replace("'", "").replace('.0', ""))
        axes.set_title(title, fontsize=15)
        axes.legend(['tp1', 'tp2'])
        pdf.savefig()


with PdfPages('/Users/lillyel-said/Desktop/patient_specific_learning_trajectories.pdf') as pdf:
    for index, value in test_df.groupby('subj_id'):
        print index, value
        axes = plt.subplot(111)
        fig = pt_all_trials.loc[index].astype(float).plot(ax=axes, y=y, subplots=False, fontsize=12, grid=True, yticks=range(0, 16), ylim=(
            0, 16), figsize=(14, 10), xticks=range(0, 6), xlim=(-0.2, 4.2), marker='o', linewidth=2, markersize=5, color='purple')
        fig = pt_all_trials.loc[index].astype(float).plot(ax=axes, y=y, subplots=False, fontsize=16, grid=True, yticks=range(0, 16), ylim=(
            0, 16), figsize=(14, 10), xticks=range(0, 6), xlim=(-0.2, 4.2), marker='o', linewidth=2, markersize=5, color='purple')
        title = 'Patient Learning Trials'
        axes.set_title(title, fontsize=20)
    pdf.savefig()
    plt.cla()
    plt.clf()
    plt.close()

    for ix, value in test_df.groupby('subj_id'):
        axes2 = plt.subplot(121)
        learning2 = pt_all_trials.loc[(ix)][['trial5', 'trial7']].astype(float).plot(ax=axes2, fontsize=15, subplots=False, grid=True, yticks=range(
            0, 16), figsize=(14, 8), ylim=(0, 16), xticks=range(0, 16), xlim=(-0.2, 1.2), marker='o', linewidth=1.75, markersize=5.0, color='#96D38C')
        axes2.yaxis.set_ylabel = ('# of words remembered')
        pdf.savefig()

    new_df = pt_all_trials[['trial5', 'trial7']].astype(int)
    new_df["diff_7_5"] = pt_all_trials["trial7"].sub(
        patient_testdf["trial5"].astype(int), axis=0)
    sorted_df = new_df.sort_values(['diff_7_5'])
    test_group5_7 = []

    for idx, val in sorted_df.groupby(level=0):
        if (val.loc[:, 'diff_7_5'] > 0).bool():
            print idx, '1'
            test_group5_7.append([idx, 1])
        if (val.loc[:, 'diff_7_5'] < -5).bool():
            print idx, '3'
            test_group5_7.append([idx, 3])
        else:
            print idx, '2'
            test_group5_7.append([idx, 2])

    df_with_groupings = pandas.DataFrame(
        data=test_group5_7, columns=['subj_id', 'group'])
    new_df = new_df.reset_index()
    merged_df = pandas.merge(new_df, df_with_groupings,
                             on='subj_id', copy=True, indicator=False).reset_index()

    plt.cla()
    plt.clf()
    plt.close()


# trials 5 scores vs trial 7 delayed scores
with PdfPages('/Users/lillyel-said/Desktop/patient_specific_learning_trajectories.pdf') as pdf:
    for index, value in merged_df.groupby('subj_id'):
        ax2 = plt.subplot(121)
        color = 'coral' if (value['group'] == 1).any() else'skyblue' if (
            value['group'] == 2).any() else 'lightgreen'
        learning_to_delay = patient_testdf.loc[(index)][['trial5', 'trial7']].astype(float).plot(ax=ax2, fontsize=15, grid=True, yticks=range(
            0, 16), figsize=(16, 10), ylim=(0, 16), xticks=range(0, 16), xlim=(-0.2, 1.2), marker='o', c=color, subplots=False, linewidth=1.75, markersize=5.0)
        ax2.set_title = 'Patient performance grouped based on Trial 5 and 7 scores'
        handles, labels = axes.get_legend_handles_labels()
        labels = ['group 1: 0+ words remembered',
                  'group 2: between 0 and -5', 'group 3: > -5 words remembered']
        display = (0, 1, 2)
        ax2.legend([label for i, label in enumerate(labels) if i in display],
                   fontsize=10, bbox_to_anchor=(1.57, 1.00), ncol=1)
        ax2.legend
        pdf.savefig()


# trials 5-6 differences

xtick_labels_5_6 = ['trial5', 'trial6']
for index, value in test_df.groupby('subj_id'):
    val = value.loc[:, 'trial1':'trial7']
    axes1 = plt.subplot(121)
    fig1 = pt_all_trials.loc[(index)][['trial5', 'trial6']].astype(float).plot(ax=axes1, fontsize=15, grid=True, yticks=range(0, 16), figsize=(
        12, 6), ylim=(0, 16), xticks=range(0, 2), xlim=(-0.2, 1.2), marker='.', linewidth=1.5, markersize=5.0, legend=False, color='b')
    axes1.set_ylabel = ('# of words remembered')
    ax2 = plt.subplot(122)
    learning_to_delay = pt_all_trials.loc[(index)][['trial5', 'trial7']].astype(float).plot(ax=ax2, fontsize=15, grid=True, yticks=range(
        0, 16), figsize=(12, 6), ylim=(0, 16), xticks=range(0, 16), xlim=(-0.2, 1.2), marker='.', linewidth=1.75, markersize=5.0)
    ax2.legend(fontsize=10, bbox_to_anchor=(1.37, 1.10), ncol=1)
