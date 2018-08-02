import collections
import csv
from difflib import SequenceMatcher
from math import ceil


def grader(all_subj_data_csv, data_output_raw_csv, data_output_scored_csv, word_corr, p_r):
	with open(all_subj_data_csv, 'U') as file:
		input_csv_lines_all_subj = csv.reader(file)
		input_csv_lines_all_subj = map(list, zip(*input_csv_lines_all_subj))
		all_subj_csv_lines = dict((rows[0], rows[1:]) for rows in input_csv_lines_all_subj)

	subj_listtype = []
	for idx, row in enumerate(all_subj_csv_lines['subject']):
		if 'rey_list' in all_subj_csv_lines['trialcode'][idx]:
			subj_listtype.append([all_subj_csv_lines['subject'][idx], all_subj_csv_lines['trialcode'][idx]])

	set_subj_listtype = []
	for subj in subj_listtype:
		if subj not in set_subj_listtype:
			set_subj_listtype.append(subj)

	## count per list type
	index_number_resp = dict()
	for list_type in sorted([x for x in set(all_subj_csv_lines['trialcode']) if 'rey_list' in x]):
		index_number_resp[list_type] = []

	for idx, response in enumerate(all_subj_csv_lines['response']):
		if 'recall_response' in all_subj_csv_lines['trialcode'][idx]:
			if 'listb' not in all_subj_csv_lines['trialcode'][idx]:
				index_number_resp[
					set_subj_listtype[[x[0] for x in set_subj_listtype].index(all_subj_csv_lines['subject'][idx])][
						1]].append(response.lower().strip())
			elif 'listb' in all_subj_csv_lines['trialcode'][idx]:
				index_number_resp[
					set_subj_listtype[[x[0] for x in set_subj_listtype].index(all_subj_csv_lines['subject'][idx])][1][
					:-1] + 'b'].append(response.lower().strip())

	counter_dict = dict()
	for list_type in sorted(index_number_resp.keys()):
		rey_recall_word_count = collections.Counter(index_number_resp[list_type])
		counter_dict[list_type] = rey_recall_word_count

	total_response_for_list = dict()
	for list_type in sorted(index_number_resp.keys()):
		total_response_for_list[list_type] = sorted(set(index_number_resp[list_type]))

	if p_r == 0:
		rey_word_lists = {
			'rey_list_presentation_1a': ['drum', 'curtain', 'bell', 'coffee', 'school', 'parent', 'moon', 'garden',
										 'hat', 'farmer', 'nose', 'turkey', 'color', 'house', 'river'],

			'rey_list_presentation_2a': ['pipe', 'wall', 'alarm', 'sugar', 'student', 'mother', 'star', 'painting',
										 'bag', 'wheat', 'mouth', 'chicken', 'sound', 'door', 'stream'],

			'rey_list_presentation_3a': ['violin', 'tree', 'scarf', 'ham', 'suitcase', 'cousin', 'earth', 'stairs',
										 'dog', 'banana', 'town', 'radio', 'hunter', 'bucket', 'field'],

			'rey_list_presentation_4a': ['doll', 'mirror', 'nail', 'sailor', 'heart', 'desert', 'face', 'letter', 'bed',
										 'machine', 'milk', 'helmet', 'music', 'horse', 'road'],
			'rey_list_presentation_1b': ['desk', 'ranger', 'bird', 'shoe', 'stove', 'mountain', 'glasses', 'towel',
										 'cloud', 'boar', 'lamb', 'gun', 'pencil', 'church', 'fish'],
			'rey_list_presentation_2b': ['bench', 'officer', 'cage', 'sock', 'fridge', 'cliff', 'bottle', 'soap',
										 'sky', 'ship', 'goat', 'bullet', 'paper', 'chapel', 'crab'],
			'rey_list_presentation_3b': ['orange', 'table', 'toad', 'corn', 'bus', 'chin', 'bleach', 'soap', 'hotel',
										 'donkey', 'spider', 'money', 'book', 'soldier', 'padlock'],
			'rey_list_presentation_4b': ['dish', 'jester', 'hill', 'coat', 'tool', 'forest', 'perfume', 'ladder',
										 'girl', 'foot', 'shield', 'pie', 'insect', 'ball', 'car']
		}
	elif p_r == 1:
		rey_word_lists = {'rey_list_presentation_1a': ['drum', 'curtain', 'bell', 'coffee', 'school'],
						  'rey_list_presentation_2a': ['pipe', 'wall', 'alarm', 'sugar', 'student'],
						  'rey_list_presentation_3a': ['violin', 'tree', 'scarf', 'ham', 'suitcase'],
						  'rey_list_presentation_4a': ['doll', 'mirror', 'nail', 'sailor', 'heart'],
						  'rey_list_presentation_1b': ['desk', 'ranger', 'bird', 'shoe', 'stove'],
						  'rey_list_presentation_2b': ['bench', 'officer', 'cage', 'sock', 'fridge'],
						  'rey_list_presentation_3b': ['orange', 'table', 'toad', 'corn', 'bus'],
						  'rey_list_presentation_4b': ['dish', 'jester', 'hill', 'coat', 'tool']
						  }
	elif p_r == 2:
		rey_word_lists = {'rey_list_presentation_1a': ['nose', 'turkey', 'color', 'house', 'river'],
						  'rey_list_presentation_2a': ['mouth', 'chicken', 'sound', 'door', 'stream'],
						  'rey_list_presentation_3a': ['town', 'radio', 'hunter', 'bucket', 'field'],
						  'rey_list_presentation_4a': ['milk', 'helmet', 'music', 'horse', 'road'],
						  'rey_list_presentation_1b': ['lamb', 'gun', 'pencil', 'church', 'fish'],
						  'rey_list_presentation_2b': ['goat', 'bullet', 'paper', 'chapel', 'crab'],
						  'rey_list_presentation_3b': ['spider', 'money', 'book', 'soldier', 'padlock'],
						  'rey_list_presentation_4b': ['shield', 'pie', 'insect', 'ball', 'car']
						  }

	with open(word_corr, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		for word_list in sorted(total_response_for_list.keys()):
			word_corrs = []
			for word in total_response_for_list[word_list]:
				wordcorrs = [round(SequenceMatcher(None, word, x).ratio(), 3) for x in rey_word_lists[word_list]]
				word_corrs.append(wordcorrs)
				writer.writerow([word, max(wordcorrs), rey_word_lists[word_list][wordcorrs.index(max(wordcorrs))]])
	csvfile.close()

	subj_id_list = []
	subj_only = []
	for subj in sorted(set(all_subj_csv_lines['subject'])):
		try:
			subj_list_type = [all_subj_csv_lines['trialcode'][x] for x in range(len(all_subj_csv_lines['subject']))
							  if (all_subj_csv_lines['subject'][x] == subj) and (
									  'rey_list_presentation_' in all_subj_csv_lines['trialcode'][x])][0]
			subj_id_list.append([subj, subj_list_type])
			subj_only.append(subj)
		except:
			print "%s has an error in their data" % subj
			continue

	full_raw_data_responses = [[all_subj_csv_lines['subject'][x], all_subj_csv_lines['trialcode'][x],
								all_subj_csv_lines['response'][x].lower()]
							   for x in range(len(all_subj_csv_lines['subject']))
							   if 'recall_response' in all_subj_csv_lines['trialcode'][x]]
	all_responses = []
	repeats = []
	list_b_all = []
	list_a_all = []
	with open(data_output_raw_csv, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(('subj_id', 'list_type', 'trial', 'response', 'score'))
		for response in full_raw_data_responses:
			subj = response[0]
			list_to_use = [subj_id_list[x][1] for x in range(len(subj_id_list)) if subj_id_list[x][0] == subj][0]
			list_a_all.append(list_to_use)
			list_b = list_to_use[:-1] + 'b'
			list_b_all.append(list_b)
			if 'listb' in response[1]:
				if response[2] in rey_word_lists[list_b]:
					response.append(1)
				else:
					if any(n > 0.8 for n in
						   [SequenceMatcher(None, response[2], x).ratio() for x in rey_word_lists[list_b]]):
						response.append(1)
					else:
						response.append(0)
				new_row = response[0], list_b, response[1].split('_')[0], response[2], response[3]
			else:
				if response[2] in rey_word_lists[list_to_use]:
					response.append(1)
				else:
					if any(n > 0.8 for n in
						   [SequenceMatcher(None, response[2], x).ratio() for x in rey_word_lists[list_to_use]]):
						response.append(1)
					else:
						response.append(0)
				new_row = response[0], list_to_use, response[1].split('_')[0], response[2], response[3]
			writer.writerow(new_row)
			all_responses.append(response)
			rep = new_row
			repeats.append(rep)
	csvfile.close()

	trial_breaks = []
	trial_lines = [all_responses[y][1] for y in range(0, len(all_responses))]
	trial_breaks = [i for i, x in enumerate(trial_lines[0:])
					if x.split('_')[0] != trial_lines[i - 1].split('_')[0]]

	trial_breaks = trial_breaks + [len(all_responses)]

	subj_scores = []
	final = []
	final_repeats = []
	for idx, val in enumerate(trial_breaks[:-1]):
		score = 0
		word_list = []
		for line in all_responses[trial_breaks[idx]:trial_breaks[idx + 1]]:
			if line[3] == 1:
				score = score + 1
				word_list.append(line[2])
		test = []
		for idx, word in enumerate(word_list):
			test.append([SequenceMatcher(None, word, x).ratio() for x in
						 [y for idx2, y in enumerate(word_list) if idx != idx2]])
		repeats = 0
		for word in test:
			word_thresholded = [ceil(x) for x in word if x > 0.8]
			n = sum(word_thresholded)
			if n != 0:
				repeats = repeats + (((n * (n + 1)) - 1) / (n + 1))
		subj_scores.append([line[0], line[1].split('_')[0], score, repeats])

	with open(data_output_scored_csv, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(
			['subj_id', 'list_type', 'listb', 'trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'trial6', 'trial7',
			 'listb_#_repeats', 'trial1_#_repeats', 'trial2_#_repeats', 'trial3_#_repeats', 'trial4_#_repeats',
			 'trial5_#_repeats', 'trial6_#_repeats', 'trial7_#_repeats'])
		subj_scores = subj_scores + ['placeholder']
		for idx, scores in enumerate(sorted(subj_scores[:-1])):
			scored = str(scores[2] - scores[3])
			repeat_nm = scores[3]
			final.append(scored)
			final_repeats.append(repeat_nm)
			subj_id = [scores[0]]
			for idx2, val in enumerate(subj_id_list):
				if subj_id[0] == subj_id_list[idx2][0]:
					subj_list = subj_id_list[idx2][1].split('_')[3]
			final_row = subj_id + [subj_list] + final + final_repeats
			if scores[0] != sorted(subj_scores)[idx + 1][0]:
				writer.writerow(final_row)
				final_row = []
				subj_id = []
				final = []
				final_repeats = []
	csvfile.close()
