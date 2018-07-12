# vmreact
These directories represent the vmreact associated scripts that have been generated to parse and clean up the raw data output. They also generate additional measures.


#vmreact_task_workflow

* running this script will:

1. Administer the task 
2. Organize the participant data folder
3. Convert .iqdat data to CSV
4. Score and generate all relevant output
5. log.txt the above process 


* scripts:
	* grader directory (with all needed scripts)
	* full_inqquisit_wkflw_all_sites.sh
		* see usage fxn
* inquisit_task
	* participant_dataa: organized and scored data output
	* all_data: a copy of the raw .iqdat data
	* task_script: script used for first timepoint
	* task_scrpt_by_form: task scripts broken up by lists for second timepoint


* New mexico example output can be found in participant_data 