import os
import numpy
import pandas
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats.stats as st
from matplotlib.backends.backend_pdf import PdfPages


scored_data=pandas.read_csv(scored_data)

#scored_data=pandas.read_csv('/Volumes/daelsaid/inquisit/INQUISIT_RERUN/all_launches_dir/scored/clean_copies/scored_data_2017_07_01_newageranges_comb_mturk.csv')
#
#patient_scored=pandas.read_csv('/Volumes/daelsaid/inquisit/INQUISIT_RERUN/all_launches_dir/scored/clean_copies/scored_data_2017_07_19_patients.csv')



# colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','cyan', '#E1396C', '#96D38C', '#FEBFB3']



def make_datatype_dir(data_type, output_path):
    if data_type='pt':
        if not os.path.isdir(args.output_path):
            os.chdir(args.output_path)
            os.mkdir(args.output_csv_location)




def age_by_gender_subplots(data, fig_out, output):
    columns=[c for c in y]
    bins=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
    colors =  ['lightskyblue','lightskyblue','lightskyblue','lightskyblue','lightskyblue','#96D38C', '#E1396C','#E1396C']

   y=['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'listb', 'trial6', 'trial7']





bins=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
colors = ['lightskyblue','lightskyblue','lightskyblue','lightskyblue','lightskyblue','#96D38C', '#E1396C','#E1396C']
y=['trial1', 'trial2', 'trial3', 'trial4', 'trial5', 'listb', 'trial6', 'trial7']
columns=[c for c in y]

with PdfPages('age_range_by_gender_figs.pdf') as pdf:
    for idx,val in scored_data.groupby(['gender', 'age_range']):
        if len(val[columns]) > 3:
            val_trials = val.loc[:,'trial1':'trial7']
            fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(14,12))
            fig=val_trials.plot.hist(y=y, bins=bins, subplots=True, ax=axes, legend=True, title=idx, xticks=range(0,16), \
            xlim=(0,16), fontsize=10, color=colors)
            for (m,n),subplot in numpy.ndenumerate(axes):
                ymin,ymax=subplot.get_ylim()
                subplot.set_ylim(0,(ymax+1))
            pdf.savefig()
        else:
            print idx, 'n too small'


with PdfPages('list_type_age_range_gender.pdf') as pdf:
    for idx,val in scored_data.groupby(['list_type', 'age_range','gender']):
        if len(val[columns]) > 3:
            val_trials = val.loc[:,'trial1':'trial7']
            fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(14,12))
            fig=val_trials.plot.hist(y=y, bins=bins, subplots=True, ax=axes, legend=True, title=idx, xticks=range(0,16), \
            xlim=(0,16), fontsize=10, color=colors)
            for (m,n),subplot in numpy.ndenumerate(axes):
                ymin,ymax=subplot.get_ylim()
                subplot.set_ylim(0,(ymax+1))
            pdf.savefig()
        else:
            print idx, 'n too small'