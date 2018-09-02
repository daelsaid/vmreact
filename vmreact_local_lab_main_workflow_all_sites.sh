#!/bin/bash

#Created on Tuesday Jul 3 13:10:06 2018

#@author: dawlat_elsaid
## needs python 2.7, panda, numpy

function usage() {
    echo ""
    echo "Usage: full_inquisit_wkflw_all_sites.sh <subject_number> <timepoint> <site_of_administration> <initial_list>"
    echo ""
    echo "<subject_number>: numeric ID- ####"
    echo "<timepoint>: single numeric digit representing timepoint (1,2,3,4..)"
    echo "<site_of_administration>: location of administration, (either newmex or emoryu)."
    echo "<initial_list>: If tp2, enter list form as a single numeric digit (1,2,3,or 4). if timepoint 1, leave BLANK"
    exit 1
}

# usage
###change with caution


#path definitions
#path to grader script

grader_script="${HOME}/Desktop/vmreact/vmreact-master/scripts/grader/"


#main inquisit directory
# inquisit_dir="/Users/`echo $USER`/Desktop/vmreact/vmreact_local_lab_workflow"



#task directory where data output lives and the task scripts are located
data_output_path="${inquisit_dir}/inquisit_task"
tp1_script_path="${inquisit_dir}/inquisit_task/task_script"
tp2_script_path="${inquisit_dir}/inquisit_task/task_script_by_form"


#variable assignments

#arguments
subj_id=$1 #enter 4 digit id only
timepoint=$2 # timepoint 1 or 2
site=$3 # emoryu, newmex, caps5
initial_list=$4 #if tp2, enter list (1,2,3,or 4)

list_types=($(seq 1 1 4)) #enter 1 numeric value (list 1,2,3,4)

#site name for new mexico is newmex
#site name for emory is emoryu


#makes data directories
cd ${data_output_path}/participant_data;

dir_id=${site}_${subj_id}_tp${timepoint}
main_dir_id=${site}_${subj_id}_tp${timepoint}_inquisit
full_subj_path=${data_output_path}/participant_data/${main_dir_id}
log_file=${full_subj_path}/out/log.txt

cd ${data_output_path}/participant_data

mkdir ${full_subj_path};
mkdir ${full_subj_path}/csv ${full_subj_path}/raw ${full_subj_path}/out;


#runs the inquisit script
cd ${full_subj_path};

if [ ${timepoint} == 1 ]; then
	/Applications/Inquisit\ 5.app/Contents/MacOS/Inquisit\ 5 ${tp1_script_path}/rey_ant_pt_hv_version_all_lists_17_08_01.iqx -s ${subj_id} -g 1 >> /dev/null 2>&1;
else
    unset list_types[$initial_list-1]
    list_types=(${list_types[@]})
    tp2_list=${list_types[$(( RANDOM % 3))]}
    /Applications/Inquisit\ 5.app/Contents/MacOS/Inquisit\ 5 ${tp2_script_path}/rey_ant_pt_hv_version_form${tp2_list}_17_10_11.iqx -s ${subj_id} -g 1 >> /dev/null 2>&1;
fi

echo "vmreact task completed, data output is being written to log file " >> ${log_file} 2>&1;
sleep 10;


#organizes data
cd ${data_output_path};
rsync -ap --progress ${data_output_path}/*/*_${subj_id}_*.iqdat ${data_output_path}/participant_data/${main_dir_id}/raw/ >> ${log_file} 2>&1;
cp -v ${full_subj_path}/raw/* ${full_subj_path}/csv/ >> ${log_file} 2>&1;
mv -v ${data_output_path}/task_script*/*_${subj_id}_*.iqdat ${data_output_path}/all_data >> ${log_file} 2>&1;

# renames the data
cd  ${full_subj_path}/csv;
mv -v `ls *demographics*` ${dir_id}_demographics_survey.iqdat >> ${log_file} 2>&1;
mv -v `ls *rey_ant_survey_survey*` ${dir_id}_rey_ant_survey.iqdat >> ${log_file} 2>&1;
mv -v `ls *_raw_*` ${dir_id}_raw.iqdat >> ${log_file} 2>&1;
mv -v `ls *_summary_*` ${dir_id}_summary.iqdat >> ${log_file} 2>&1;


#converts to csv from tab-delimited
for iqdat in `ls *.iqdat`;
	do
	cat $iqdat | tr "\\t" "," > `echo $iqdat | cut -d. -f1`.csv;
done

#grades the data
cd ${full_subj_path}/csv;

echo "grading output located at ${full_subj_path}/out" >> ${log_file} 2>&1;

python ${grader_script}/complete_inquisit_output.py -r `ls *raw.csv` -d `ls *demo*.csv` -s `ls *summary.csv*` -e `ls *_rey_ant_survey.csv` -o ${full_subj_path}/out;

echo "grading has completed"
echo "subject scores:" `cat ${full_subj_path}`"/out/*scored_data_2*.csv";

echo "deactivating vmreact environment";
source deactivate vmreact;
