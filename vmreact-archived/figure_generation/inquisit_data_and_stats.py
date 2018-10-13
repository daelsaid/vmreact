import os
import numpy
import pandas
import datetime
import scipy.stats.stats as st
# import matplotlib.pyplot as plt

format = "%Y_%m_%d"
current_date=datetime.datetime.today()
print 'dataset path: /Volumes/daelsaid/inquisit/INQUISIT_RERUN/all_launches_dir/scored/clean_copies/scored_data_2017_07_01_comb_mturk.csv'
print ' '
print current_date


scored_data=pandas.read_csv('/Volumes/daelsaid/inquisit/INQUISIT_RERUN/all_launches_dir/scored/clean_copies/scored_data_2017_07_01_newageranges_comb_mturk.csv')
y=['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'listb', 'trial6', 'trial7']

test_df=pandas.DataFrame(data=scored_data.set_index(['gender', 'age_range']).loc[:,'trial1':'trial7'])

for col in y:
    print '     '
    print '*******' + col + '*******'
    for idx,val in test_df.groupby(level=1):
        if len(val) >3:
            u,p= st.mannwhitneyu(val.loc['female'][col],val.loc['male'][col], use_continuity=True,alternative='two-sided')
            if p < 0.05:
                print 'age_range ' + list(set(val.loc['female'][col].index.tolist()))[0] + ':', u, p, '**'
            else:
                print 'age_range ' + list(set(val.loc['female'][col].index.tolist()))[0] + ':', u, p, 'ns'
        else:
            print 'age_range ' + list(set(val.loc['female'][col].index.tolist()))[0]+ ': n is less than 3'









