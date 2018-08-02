# coding: utf-8

# In[40]:

import os
from glob import glob

import pandas as pd

# In[41]:

scored_dir = '/Users/lillyel-said/Desktop/vmreact/vmreact/2_vmreact/'
parsed_list = []

for batch in range(1, 9):
	batch = str(batch)
	parsed = os.path.join(scored_dir, 'mturk_batch' + batch + '_parsed_raw_data.csv')
	parsed_df = pd.read_csv(parsed, dtype=str)
	parsed_list.append(parsed_df)
	parsed_df['identifier'] = parsed_df['subj_id'] + '_' + parsed.split('_')[-4]

# In[42]:

all_parsed = pd.concat(parsed_list, axis=0)
all_parsed_df = pd.DataFrame(data=all_parsed)

cols = ['subj_id', 'identifier', 'list_type', 'trial', 'response', 'score']
final_csv = pd.DataFrame(data=all_parsed_df, columns=cols)
# final_csv.to_csv(os.path.join(scored_dir,'parsed_raw_with_errors.csv'))


# In[43]:

zero = final_csv.loc[final_csv['score'] == '0']
zero.dropna(inplace=True)
incorrect_df = pd.DataFrame(data=zero)

# incorrect_df.to_csv(os.path.join(scored_dir,'incorrect_response.csv'))


# In[56]:

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
word_lists_df = pd.DataFrame.from_dict(rey_word_lists)

# In[ ]:

for lists, response in incorrect_df.groupby(level=1):
	print response

# In[55]:


# In[45]:

cols = ['typing_test_openended_sentence1', 'typing_speed_next_trial', 'typing_test_openended_sentence2',
		'typing_test_error2', 'typing_test_openended_sentence2', 'typing_speed_next_trial_2',
		'typing_test_openended_sentence3']
scored_dir = '/Users/lillyel-said/Desktop/vmreact/vmreact/1_rawdata/'

typing_test_list = []
for scored_csv in glob(os.path.join(scored_dir, '*mturk*', '*raw.csv')):
	raw_csv = pd.read_csv(scored_csv, dtype=str)
	typing_test = raw_csv.loc[raw_csv['blockcode'] == 'typing_test']
	typing_test_list.append(typing_test)

#         typingtest=df.loc[df['trialcode'].str.contains(trial),'trialcode']

combined = pd.concat(typing_test_list, axis=0)

# In[46]:

typing_test_cols = combined.columns.tolist()
final_cols = ['subject', 'date', 'blockcode', 'trialcode', 'response', 'latency']
typing_test_only = combined[final_cols]
unique_cols = combined['trialcode'].unique().tolist()

# In[47]:

typing_test_only.to_csv(os.path.join(scored_dir, 'typing_test_raw.csv'))

# In[48]:

for ix, response in typing_test_only.groupby('subject'):
	if (response.response != 57).any():
		print response['trialcode'][0] ==
#         print response.subject.head(),response.response.unique()


# In[38]:

sentence_1 = ['typing_test_openended_sentence1', 'typing_speed_next_trial']
sentence_2 = ['typing_test_openended_sentence2', 'typing_speed_next_trial_2']
sentence_3 = ['typing_test_openended_sentence3', 'typing_speed_next_trial_3']

for i, sentence in typing_test_only.groupby('subject'):
	print sentence

# In[ ]:


# In[ ]:
