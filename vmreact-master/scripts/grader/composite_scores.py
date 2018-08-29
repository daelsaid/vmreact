# !/usr/bin/env python2

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 12:04:33 2018

@author: dawlat_elsaid
"""

import pandas
import numpy as np


def composite_scores(get_comp_scores, input_csv, output_csv):
	scored_data = pandas.read_csv(input_csv)

	if get_comp_scores == 1:
		df_trials = scored_data.loc[:, 'subj_id':'trial7']
		composite_scores = pandas.DataFrame()
		tmp = pandas.DataFrame()

		composite_scores[['subj_id', 'list_type']] = df_trials[['subj_id', 'list_type']]

		composite_scores['total_learning'] = df_trials[['trial1', 'trial2', 'trial3', 'trial4', 'trial5']].apply(
			lambda row: np.sum(row), axis=1)

		tmp['test'] = df_trials[['trial1']] * 5

		composite_scores['corrected_total_learning'] = composite_scores['total_learning'].subtract(tmp['test'])

		composite_scores['learning_rate'] = df_trials['trial5'].subtract(df_trials['trial1'], axis='rows')
		composite_scores['proactive_interference'] = df_trials['trial1'].subtract(scored_data['listb'], axis='rows')
		composite_scores['retroactive_interference'] = df_trials['trial5'].subtract(df_trials['trial6'], axis='rows')
		composite_scores['forgetting_and_retention'] = df_trials['trial5'].subtract(df_trials['trial7'], axis='rows')
		# composite_scores_transposed=composite_scores.transpose()
		# composite_scores_transposed.to_csv(output_csv,header=True,index=['measure','score'])
		composite_scores.to_csv(output_csv, header=True, index=['measure', 'score'])
