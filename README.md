# vmreact
These directories represent the vmreact associated scripts that have been generated to parse and clean up the raw data output. They also generate additional measures.

Check out the wiki page for detailed installation instructions:

**`WIKI PAGE: https://github.com/daelsaid/vmreact/wiki`**


Relative paths for each directory within "vmreact" are listed below:


#VMREACT WORKFLOW

MAIN SCRIPT: **``vmreact_local_lab_main_workflow_all_sites.sh``**

Usage: full_inquisit_wkflw_all_sites.sh <subject_number> <timepoint> <site_of_administration> <initial_list>

<subject_number>: numeric ID- ####

<timepoint>: single numeric digit representing timepoint (1,2,3,4..)

<site_of_administration>: location of administration, (either newmex or emoryu).

<initial_list>: If tp2, enter list form as a single numeric digit (1,2,3,or 4). if timepoint 1, leave BLANK

**running this script will:

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
