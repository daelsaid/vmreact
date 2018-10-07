import os
import argparse
import datetime
import pandas as pd
from glob import glob
import numpy as np

from composite_scores import composite_scores
from inquisit_demo_summary import demo_and_summary
from inquisit_demo_summary_newageranges import demo_and_summary_new
from inquisit_grader import grader
from best_vmreact_subj_naming import best_rename_with_subj
from best_vmreact_compilation_merged import restructure_and_regrade_all_data
from extract_csv_into_dict_fxn import extract_data_from_csv_into_dict
# def install(name):
	# import subprocess
    # subprocess.call(['pip', 'install', name])
# install('pandas')


# os.chdir('/Users/lillyel-said/Desktop/stanford/scripts/projects/vmreact_conda/vmreact-master/scripts/grader')

template_dir='../../vmreact/ant_vmreact_binder-master'

parser = argparse.ArgumentParser(
	description='Grades inquisit data, output: frequency counts of responses to demo survey, parsed raw data (all, primacy, recency), scored data (all, primacy, recency), SR responses compiled, subject age ranges and gender, summary ANT scores, word correlations (all, primacy, recency)')

#ADDING ARGUMENTS REQUIRED
parser.add_argument('-r', dest='raw_data', help='path to raw data', type=str, required=True)
parser.add_argument('-d', dest='demo_data', help='demo_csv', type=str, required=True)
parser.add_argument('-s', dest='summary_data', help='summary csv', type=str, required=True)
parser.add_argument('-e', dest='rey_ant_end_survey', help='rey_ant_final survey',type=str,required=True)
parser.add_argument('-o', dest='output_csv_location', help='path to output folder', type=str, default=os.getcwd())
parser.add_argument('--site_name',dest='site_of_administration',help='best=stanford, new_mex="best_new mex"', type=str, default='stanford',required=True)
parser.add_argument('--template_dir',dest='templates',help='full path to location of template directories for ANTr', type=str,default=template_dir, required=True)


args = parser.parse_args()

if not os.path.isdir(args.output_csv_location):
	os.mkdir(args.output_csv_location)

site_location=args.site_of_administration
template_dir=args.templates
all_subj_data_csv = args.raw_data
demographic_data = args.demo_data
final_summary_csv = args.summary_data
end=args.rey_ant_end_survey
output=args.output_csv_location
csv_dir=output.split('/')[-2]
main_dir=output.split('/')[-4]



format = "%Y_%m_%d"
current_date = datetime.datetime.today()
date = current_date.strftime(format)

#all file_output csv names defined below
#demographic data
vmreact_basic_demo_frequency_counts=os.path.join(args.output_csv_location, 'vmreact_frequency_counts' + '_' + date + '.csv')
vmreact_demo_agegender_age_range_from_norms=os.path.join(args.output_csv_location, 'vmreact_subj_age_agerange_gender' + '_' + date + '.csv')
vmreact_self_report_scores=os.path.join(args.output_csv_location, 'vmreact_sr_responses' + '_' + date + '.csv') #mturk subj got the self reports, best individual did not due to the possible  overlap
vmreact_demo_agegender_age_range_new_bins=os.path.join(args.output_csv_location, 'vmreact_subj_age_agerange_gender' + '_' + date + '.csv')

#ANTr
vmreact_antr_accuracy_scores=os.path.join(args.output_csv_location, 'vmreact_summary_ant_scores' + '_' + date + '.csv')

#scores of list with all 15 words taht must be recalled
vmreact_all_words_score_assignment=os.path.join(args.output_csv_location, 'vmreact_parsed_raw_data' + '_' + date + '.csv')
vmreact_all_words_scored_data=os.path.join(args.output_csv_location, 'vmreact_scored_data' + '_' + date + '.csv')
vmreact_all_words_correlations=os.path.join(args.output_csv_location, 'vmreact_word_correlations' + '_' + date + '.csv')

#scores of words recalled that are in the last 5 /15 words
vmreact_recency_score_assignment=os.path.join(args.output_csv_location,'vmreact_parsed_raw_data_recency' + '_' + date + '.csv')
vmreact_recency_scored_data=os.path.join(args.output_csv_location,'vmreact_scored_data_recency' + '_' + date + '.csv'),
vmreact_recency_word_correlations=os.path.join(args.output_csv_location,'vmreact_word_correlations_recency' + '_' + date + '.csv')

#scores of words recalled that are in the first 5 /15 words
vmreact_primacy_score_assignment=os.path.join(args.output_csv_location, 'vmreact_parsed_raw_data_primacy' + '_' + date + '.csv')
vmreact_primacy_scored_data=os.path.join(args.output_csv_location, 'vmreact_scored_data_primacy' + '_' + date + '.csv'),
vmreact_primacy_word_correlations=os.path.join(args.output_csv_location, 'vmreact_word_correlations_primacy' + '_' + date + '.csv')

#composite scored_cols
vmreact_composite_scores_outfile=os.path.join(args.output_csv_location, 'vmreact_composite_scores_vakil' + '_' + date + '.csv')

#parse demo data and create human readable file
demo_and_summary(all_subj_data_csv, demographic_data, final_summary_csv, vmreact_basic_demo_frequency_counts, vmreact_demo_agegender_age_range_from_norms, vmreact_self_report_scores, vmreact_antr_accuracy_scores)

demo_and_summary_new(all_subj_data_csv, demographic_data, vmreact_demo_agegender_age_range_new_bins)

#regular scorin
print all_subj_data_csv,vmreact_all_words_score_assignment,vmreact_all_words_scored_data,vmreact_all_words_correlations
grader(all_subj_data_csv, vmreact_all_words_score_assignment, vmreact_all_words_scored_data, vmreact_all_words_correlations, 0)

#$scoring based off of how many recalled words from first 5 of trials that occurred before
grader(all_subj_data_csv, vmreact_primacy_score_assignment, vmreact_primacy_scored_data, vmreact_primacy_word_correlations, 1)

#$scoring based off of how many recalled words from last of trials that occurred before
grader(all_subj_data_csv, vmreact_recency_score_assignment, vmreact_recency_scored_data,vmreact_recency_word_correlations, 2)

#generate composite scores from scored data. numpy problematic on occasion, run gen_composite.sh (./gen_composie.sh)
composite_scores(vmreact_all_words_scored_data,vmreact_composite_scores_outfile,1)

#is this best data?
best_rename_with_subj(output,site_of_administration)

restructure_and_regrade_all_data(output)

#generate latency measures for vmreact
gen_vmreact_latencies(csv_dir,output)

#generate latency measures for the ANT r task
ant_extraction_and_latencies(csv_dir,output,template_dir,output)



# batch_merge(args.output_csv_location,compiled_columns(os.path.join(args.output_csv_location,csv_dir,'csv')))

# organize_columns_merge_csvs(args.output_csv_location,compiled_columns(os.path.join(args.output_csv_location,csv_dir,'csv')))
