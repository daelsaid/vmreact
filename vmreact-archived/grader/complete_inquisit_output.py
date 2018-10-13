import os
import argparse
import datetime
from inquisit_demo_summary import demo_and_summary
from inquisit_grader import grader
from inquisit_demo_summary_newageranges import demo_and_summary_new

format = "%Y_%m_%d"
current_date=datetime.datetime.today()
date = current_date.strftime(format)

parser = argparse.ArgumentParser(description='Grades inquisit data, output: frequency counts of responses to demo survey, parsed raw data (all, primacy, recency), scored data (all, primacy, recency), SR responses compiled, subject age ranges and gender, summary ANT scores, word correlations (all, primacy, recency)')

parser.add_argument('-r', dest='raw_data',help='path to raw data',type=str,required=True)
parser.add_argument('-d', dest='demo_data', help='demo_csv', type=str, required=True)
parser.add_argument('-s', dest='summary_data', help='summary csv', type=str, required=True)
parser.add_argument('-o', dest='output_csv_location', help='path to output folder',type=str,default=os.getcwd())


args=parser.parse_args()

if not os.path.isdir(args.output_csv_location):
    os.mkdir(args.output_csv_location)

all_subj_data_csv = args.raw_data
demographic_data = args.demo_data
final_summary_csv = args.summary_data

demo_and_summary(all_subj_data_csv, args.demo_data, args.summary_data, os.path.join(args.output_csv_location, 'frequency_counts'+ '_'+ date + '.csv'),os.path.join(args.output_csv_location, 'subj_age_agerange_gender'+ '_'+ date + '.csv'), os.path.join(args.output_csv_location, 'sr_responses'+ '_'+ date + '.csv'), os.path.join(args.output_csv_location, 'summary_ant_scores'+ '_'+ date + '.csv'))

demo_and_summary_new(all_subj_data_csv, args.demo_data,os.path.join(args.output_csv_location, 'subj_age_agerange_gender_new_age_bins'+ '_'+ date + '.csv'))


grader(all_subj_data_csv, os.path.join(args.output_csv_location,'parsed_raw_data' + '_'+ date + '.csv'),os.path.join(args.output_csv_location,'scored_data' + '_'+ date + '.csv'),os.path.join(args.output_csv_location,'word_correlations' + '_'+ date + '.csv'),0)

grader(all_subj_data_csv,os.path.join(args.output_csv_location,'parsed_raw_data_primacy'+ '_'+ date + '.csv'),os.path.join(args.output_csv_location,'scored_data_primacy'+ '_'+ date + '.csv'),os.path.join(args.output_csv_location,'word_correlations_primacy'+ '_'+ date + '.csv'),1)

grader(all_subj_data_csv,os.path.join(args.output_csv_location,'parsed_raw_data_recency'+ '_'+ date + '.csv'),os.path.join(args.output_csv_location,'scored_data_recency'+ '_'+ date + '.csv'),os.path.join(args.output_csv_location,'word_correlations_recency'+ '_'+ date + '.csv'),2)