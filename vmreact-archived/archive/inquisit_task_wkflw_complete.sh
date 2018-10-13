data_output_path='/Users/bestptsd/Desktop/inquisit_task'
tp1_script_path='/Users/bestptsd/Desktop/inquisit_task/task_script'
tp2_script_path='/Users/bestptsd/Desktop/inquisit_task/task_script_by_form'

list_types=($(seq 1 1 4))
subj_id=$1
timepoint=$2
initial_list=$3

main_dir_id=best_${subj_id}_tp${timepoint}_inquisit
dir_id=best_${subj_id}_tp${timepoint}
full_subj_path=${data_output_path}/participant_data/${main_dir_id}

cd ${data_output_path}/participant_data; mkdir $main_dir_id;
cd $main_dir_id; mkdir csv raw out; 

if [ "$timepoint" == 1 ]; then
	cd ${tp1_script_path}
	/Applications/Inquisit\ 5.app/Contents/MacOS/Inquisit\ 5 `echo ${tp1_script_path}/rey_ant_pt_hv_version_all_lists_17_08_01.iqx` `echo '-s'` "$subj_id" `echo '-g 1'`;
else
	cd ${tp2_script_path}
	unset list_types[$initial_list-1]
	/Applications/Inquisit\ 5.app/Contents/MacOS/Inquisit\ 5 `echo ${tp2_script_path}/rey_ant_pt_hv_version_form\`for x in $list_types; do echo ${list_types[ $(( RANDOM % ${#list_types[@]} )) ]}; done\`_17_10_11.iqx` `echo '-s'` "$subj_id" `echo '-g 1'`;
fi

number_of_processes=`ps -ef | grep "/Applications/Inquisit 5.app*" | grep -v grep > /dev/null | wc -l`
pid=0
if [ $number_of_processes -gt 0 ]; then
	while [ pid -eq 0 ]
	do
		ps -ef | grep "/Applications/Inquisit 5.app*" | grep -v grep > /dev/null
		pid=`echo $!`
		sleep 10
	done
fi

cd $data_output_path;
for data in `find . -maxdepth 2 -name "*${subj_id}_*.iqdat" -type f`; do echo ${data_output_path}/$data; rsync -azvp --progress $data ${data_output_path}/participant_data/${main_dir_id}/raw/; done;

sleep 2

for data in `find . -maxdepth 2 -name "*${subj_id}_*.iqdat" -type f`; do echo ${data_output_path}/$data; mv ${data_output_path}/$data ${data_output_path}/all_data; done;

cd ${full_subj_path}/raw/; for file in `ls *`; do cp $file ${full_subj_path}/csv; done;

cd  ${full_subj_path}/csv;

for datafile in `ls ${full_subj_path}/csv`; do ext="iqdat" demo=`echo $datafile | grep demographics`; summary=`echo $datafile | grep summary`; final=`echo $datafile | grep "rey_ant_survey_survey"`; raw=`echo $datafile | grep "_raw_"`; rename_dirs $final ${dir_id}_rey_ant_survey.$ext; rename_dirs $demo ${dir_id}_demographics_survey.$ext; rename_dirs $raw ${dir_id}_raw.$ext; rename_dirs $summary ${dir_id}_summary.$ext; done;


for iqdat in `ls *.iqdat`; do cat $iqdat | tr "\\t" "," > `echo $iqdat | cut -d. -f1`.csv; done

inquisit_grader `ls *raw.csv` `ls *demo*.csv` `ls *summary.csv*` ${full_subj_path}/out