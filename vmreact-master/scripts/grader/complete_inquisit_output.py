import argparse
import datetime
import pandas as pd
import datetime
from glob import glob
import os
import numpy as np

from composite_scores import composite_scores
from inquisit_demo_summary import demo_and_summary
from inquisit_demo_summary_newageranges import demo_and_summary_new
from inquisit_grader import grader
from best_vmreact_subj_naming import best_rename_with_subj
from best_vmreact_compilation_merged import restructure_and_regrade_all_data
# os.chdir('/Users/lillyel-said/Desktop/stanford/scripts/projects/vmreact_conda/vmreact-master/scripts/grader')

format = "%Y_%m_%d"
current_date = datetime.datetime.today()
date = current_date.strftime(format)

parser = argparse.ArgumentParser(
	description='Grades inquisit data, output: frequency counts of responses to demo survey, parsed raw data (all, primacy, recency), scored data (all, primacy, recency), SR responses compiled, subject age ranges and gender, summary ANT scores, word correlations (all, primacy, recency)')

parser.add_argument('-r', dest='raw_data', help='path to raw data', type=str, required=True)
parser.add_argument('-d', dest='demo_data', help='demo_csv', type=str, required=True)
parser.add_argument('-s', dest='summary_data', help='summary csv', type=str, required=True)
parser.add_argument('-e', dest='rey_ant_end_survey', help='rey_ant_final survey',type=str,required=True)
parser.add_argument('-o', dest='output_csv_location', help='path to output folder', type=str, default=os.getcwd())

args = parser.parse_args()

if not os.path.isdir(args.output_csv_location):
	os.mkdir(args.output_csv_location)

all_subj_data_csv = args.raw_data
demographic_data = args.demo_data
final_summary_csv = args.summary_data
end=args.rey_ant_end_survey
output=args.output_csv_location

template_dir='${HOME}/Desktop/vmreact/ant_vmreact_binder-master/templates'
csv_dir=output.split('/')[-2]
main_dir=output.split('/')[-4]

demo_and_summary(all_subj_data_csv, args.demo_data, args.summary_data,
				 os.path.join(args.output_csv_location, 'frequency_counts' + '_' + date + '.csv'),
				 os.path.join(args.output_csv_location, 'subj_age_agerange_gender' + '_' + date + '.csv'),
				 os.path.join(args.output_csv_location, 'sr_responses' + '_' + date + '.csv'),
				 os.path.join(args.output_csv_location, 'summary_ant_scores' + '_' + date + '.csv'))

demo_and_summary_new(all_subj_data_csv, args.demo_data, os.path.join(args.output_csv_location,
																	 'subj_age_agerange_gender_new_age_bins' + '_' + date + '.csv'))

grader(all_subj_data_csv, os.path.join(args.output_csv_location, 'vmreact_parsed_raw_data' + '_' + date + '.csv'),
	   os.path.join(args.output_csv_location, 'vmreact_scored_data' + '_' + date + '.csv'),
	   os.path.join(args.output_csv_location, 'vmreact_word_correlations' + '_' + date + '.csv'), 0)

grader(all_subj_data_csv, os.path.join(args.output_csv_location, 'parsed_raw_data_primacy' + '_' + date + '.csv'),
	   os.path.join(args.output_csv_location, 'vmreact_scored_data_primacy' + '_' + date + '.csv'),
	   os.path.join(args.output_csv_location, 'vmreact_word_correlations_primacy' + '_' + date + '.csv'), 1)

grader(all_subj_data_csv, os.path.join(args.output_csv_location, 'vmreact_parsed_raw_data_recency' + '_' + date + '.csv'),
	   os.path.join(args.output_csv_location, 'vmreact_scored_data_recency' + '_' + date + '.csv'),
	   os.path.join(args.output_csv_location, 'vmreact_word_correlations_recency' + '_' + date + '.csv'), 2)

composite_scores(1, os.path.join(args.output_csv_location, 'vmreact_scored_data' + '_' + date + '.csv'),os.path.join(args.output_csv_location, 'vmreact_composite_scores_vakil' + '_' + date + '.csv'))

best_rename_with_subj(args.output_csv_location)

restructure_and_regrade_all_data(args.output_csv_location)

gen_vmreact_latencies(csv_dir,args.output_csv_location)

ant_extraction_and_latencies(csv_dir,args.output_csv_location,template_dir,args.output_csv_location)



# batch_merge(args.output_csv_location,compiled_columns(os.path.join(args.output_csv_location,csv_dir,'csv')))

# organize_columns_merge_csvs(args.output_csv_location,compiled_columns(os.path.join(args.output_csv_location,csv_dir,'csv')))
