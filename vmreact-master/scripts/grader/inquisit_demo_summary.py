import collections
import csv


def demo_and_summary(all_subj_data_csv, demographic_data, final_summary_csv, frequency_count, subj_age_agerange_gender,
					 sr_responses, summary_ant_scores):
	with open(all_subj_data_csv, 'U') as file:
		input_csv_lines_all_subj = csv.reader(file)
		input_csv_lines_all_subj = map(list, zip(*input_csv_lines_all_subj))
		all_subj_csv_lines = dict((rows[0], rows[1:]) for rows in input_csv_lines_all_subj)

	with open(demographic_data, 'U') as file:
		input_demo_sr_q_csv = csv.reader(file)
		input_demo_sr_q_csv = map(list, zip(*input_demo_sr_q_csv))
		demographic_data = dict((rows[0], rows[1:]) for rows in (input_demo_sr_q_csv))

	with open(final_summary_csv, 'U') as file:
		final_summary_lines = csv.reader(file)
		final_summary_lines = map(list, zip(*final_summary_lines))
		rey_summary = dict((rows[0], rows[1:]) for rows in (final_summary_lines))

	age_ranges = {
		'16-19': range(16, 20, 1),
		'20-29': range(20, 30, 1),
		'30-39': range(30, 40, 1),
		'40-49': range(40, 50, 1),
		'50-59': range(50, 60, 1),
		'57-69': range(57, 70, 1),
		'70-79': range(70, 80, 1),
		'76-89': range(76, 90, 1)
	}
	subj_id_list_demo = []
	subj_id_only_demo = []

	for subject in sorted(set(all_subj_csv_lines['subject'])):
		subj_id_only_demo.append(subject)
		subj_id_list_combined = [demographic_data['subject'][x] for x in range(len(demographic_data['subject'])) if
								 demographic_data['subject'][x] == subject]
		subj_id_list_demo.append(subj_id_list_combined)

	subj_id_combined = [(idx, val) for idx, val in enumerate(sorted(subj_id_only_demo))]

	subj_val = []
	key_val_all = []
	for key in sorted(demographic_data.keys()):
		for value in sorted(demographic_data[key]):
			key_val_all.append([key, value])
			if 'subject' in key:
				subj_val.append(value)
			else:
				continue

	subj_id_with_index = list()
	for subj_num in subj_val:
		subj_combined = [[idx, val] for idx, val in enumerate(sorted(subj_id_only_demo)) if val == subj_num]
		subj_indexvals = [[idx, val] for idx, val in enumerate(sorted(subj_id_only_demo))]
		subj_id_with_index.append(subj_combined)

	new_demo_dict = dict()
	for key_var in sorted(demographic_data.keys()):
		if 'latency' not in key_var and 'group' not in key_var and 'build' not in key_var and 'time' not in key_var and 'date' not in key_var:
			new_demo_dict[key_var] = []

	for index1, val1 in enumerate(key_val_all):
		if val1[0] in new_demo_dict.keys():
			new_demo_dict[val1[0]].append(val1[1])

	counter_demo_dict = dict()
	for key_q in sorted(new_demo_dict.keys()):
		answer_count = collections.Counter(new_demo_dict[key_q])
		counter_demo_dict[key_q] = answer_count

	with open(frequency_count, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(['survey_question', 'response_counts'])
		for key, value in sorted(counter_demo_dict.items()):
			writer.writerow([key, value])
	csvfile.close()

	subj_age_gender_mem = []
	x = []
	for idx2, subj_id in enumerate(subj_id_only_demo):
		subj_age_gen = [[demographic_data['subject'][x], demographic_data['gender_response'][x].lower(),
						 demographic_data['age_textbox_response'][x]] for x in range(len(demographic_data['subject']))
						if demographic_data['subject'][x] == subj_id]
		y = [[demographic_data['subject'][x]] for x in range(len(demographic_data['subject'])) if
			 demographic_data['subject'][x] == subj_id]
		subj_age_gender_mem.append(subj_age_gen)

	demo_subj_age_gender = [[demographic_data['subject'][x], demographic_data['gender_response'][x].lower(),
							 demographic_data['age_textbox_response'][x]]
							for x in range(len(demographic_data['subject']))
							if demographic_data['subject'][x]]

	raw_data_responses = [[all_subj_csv_lines['subject'][x], all_subj_csv_lines['trialcode'][x],
						   all_subj_csv_lines['response'][x].lower()]
						  for x in range(len(all_subj_csv_lines['subject']))
						  if 'recall_response' in all_subj_csv_lines['trialcode'][x]]

	key_val = []
	for key in age_ranges.keys():
		for val in age_ranges[key]:
			key_val.append([key, val])

	id_age_agerange = []
	with open(subj_age_agerange_gender, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(['subj_id', 'gender', 'age', 'age_range'])
		for subj in sorted(demo_subj_age_gender):
			subj_from_main_raw_list = []
			ages = subj[2]
			gender = subj[1]
			subj_id_raw = [val for val in raw_data_responses if val[0] == subj[0]]
			for vals in key_val:
				age_vals = vals[1]
				age_vals = str(age_vals)
				if age_vals == ages:
					complete_list = subj[0] + ',' + gender + "," + age_vals + "," + vals[0]
					id_age_agerange.append(complete_list)
					writer.writerow([subj[0], gender, age_vals, vals[0]])
	csvfile.close()

	subj_id_only = []
	for subject in sorted(set(all_subj_csv_lines['subject'])):
		subj_id_only.append(subject)

	subj_id_memory = [subj_mem_trials for subj_mem_trials in subj_id_only]

	subj_ids_summary = [x for x in rey_summary['script.subjectid']]
	subj_ids_summary = sorted(subj_ids_summary)

	summary_key_val = []
	for key in sorted(rey_summary.keys()):
		for value in sorted(rey_summary[key]):
			summary_key_val.append([key, value])

	new_summary_dict = dict()
	for sum_key in sorted(rey_summary.keys()):
		if 'script.starttime' not in sum_key and 'script.startdate' not in sum_key and 'script.elapsedtime' not in sum_key and 'values.trialcount' not in sum_key and 'values.completed' not in sum_key and 'values.trialcount' not in sum_key and 'parameters.min_validlatency' not in sum_key and 'computer.platform' not in sum_key:
			new_summary_dict[sum_key] = []

	for sum_idx, sum_val in enumerate(summary_key_val):
		if sum_val[0] in new_summary_dict.keys():
			new_summary_dict[sum_val[0]].append(sum_val[1])

	subject_summary_sr_responses = [[rey_summary['script.subjectid'][x], rey_summary['expressions.gad_7_total'][x],
									 rey_summary['expressions.phq_total'][x],
									 rey_summary['expressions.pcl_4_total'][x],
									 rey_summary['expressions.pcl_total_hybridscore_corrected'][x]] for x in
									range(len(rey_summary['script.subjectid'])) if
									rey_summary['values.end_survey_completed'][x] == '1']

	subject_summary_ant_scores = [
		[rey_summary['script.subjectid'][x], rey_summary['expressions.overallpercentcorrect'][x],
		 rey_summary['expressions.meanRT'][x], rey_summary['expressions.stdRT'][x]] for x in
		range(len(rey_summary['script.subjectid'])) if rey_summary['values.end_survey_completed'][x] == '1']

	with open(sr_responses, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(['subj_id', 'gad_7', 'phq', 'pcl_dsm4', 'pcl_hybrid'])
		for responses in sorted(subject_summary_sr_responses):
			writer.writerow(responses)
	csvfile.close()

	with open(summary_ant_scores, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(['subj_id', 'percent_correct', 'meanRT', 'stdRT'])
		for scores in sorted(subject_summary_ant_scores):
			writer.writerow(scores)
		csvfile.close()
