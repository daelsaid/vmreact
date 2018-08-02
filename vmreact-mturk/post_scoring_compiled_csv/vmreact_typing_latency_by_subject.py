import os
from glob import glob

import pandas as pd

final = []

for x in glob(os.path.join(data_dir, 'filtered_typing_test.csv')):
	df = pd.read_csv(x, dtype='str')
	for i, val in df.groupby(['subject', 'date']):
		print i[0] + '_' + i[1], i[0], i[1], val['latency'].astype(int).mean()
