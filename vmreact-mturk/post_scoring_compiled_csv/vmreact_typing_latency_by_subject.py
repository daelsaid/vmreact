import os
from glob import glob

import pandas as pd

final = []
data_dir = ''


def typing_test_extraction(data_dir, output_csv_path):
    for x in glob(os.path.join(data_dir, 'filtered_typing_test.csv')):
        df = pd.read_csv(x, dtype='str')
        for i, val in df.groupby(['subject', 'date']):
            print i[0] + '_' + \
                i[1], i[0], i[1], val['latency'].astype(int).mean()
            vals = i[0] + '_' + \
                i[1], i[0], i[1], val['latency'].astype(int).mean()
            vals.to_csv(os.path.join(output_csv_path,
                                     'typing_test_average_latency.csv'))
