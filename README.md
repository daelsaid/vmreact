## VMREACT

These directories represent the VMREACT associated scripts that have been generated to parse and clean up the raw data output. They also generate additional measures.

Site specific example output can be found in the participant_data directory located here:

	New Mexico: `/vmreact_local_lab_workflow/inquisit_task/participant_data`


Check out the wiki page for detailed installation instructions:  
### <center>**`WIKI PAGE: https://github.com/daelsaid/vmreact/wiki`**</center>  

---

#### VMREACT LOCAL LAB WORKFLOW  

MAIN LOCAL SCRIPT: **`vmreact_local_lab_main_workflow_all_sites.sh`**  
	- to run:
		option 1: ./vmreact_local_lab_main_workflow_all_sites.sh
		option 2: bash vmreact_local_lab_main_workflow_all_sites.sh   

##### Usage:

`bash vmreact_local_lab_main_workflow_all_sites.sh` [subject_number] [timepoint] [site_of_administration] [initial_list]  

<u>[subject_number]</u> numeric ID- ####  
<u>[timepoint]</u> single numeric digit representing timepoint (1,2,3,4..)  
<u>[site_of_administration]</u> location of administration, (either newmex or emoryu)  
<u>[initial_list]:</u> If tp2, enter list form as a single numeric digit (1,2,3,or 4). if timepoint 1, leave BLANK  

---

#### **Running this script will**

1. Administer the task  
2. Organize the participant data folder  
3. Convert .iqdat data to CSV  
4. Score and generate all relevant output  
5. generate a log.txt the above process  
6. <u>master grading:</u>  
	- grader directory (with all needed scripts)  
	- vmreact_local_lab_main_workflow_all_sites.sh  
	- see usage fxn  
8. <u>inquisit_task</u>  
	- participant_data: organized and scored data output  
	- all_data: a copy of the raw .iqdat data  
	- task_script: script used for first timepoint  
	- task_scrpt_by_form: task scripts broken up by lists for second timepoint  
