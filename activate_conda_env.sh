#!/bin/bash

project_path=${HOME}/Desktop/vmreact

env_path="${project_path}/pre-requirements/vmreact_miniconda2/envs/vmreact"

#rename vmreact-master to vmreact

echo "renaming vmreact-master to vmreact"
#mv "/Users/`echo $USER`/Desktop/vmreact-master" "/Users/`echo $USER`/Desktop/vmreact";

#install miniconda in the pre-requirements dir
echo "Installing miniconda2 in the pre-requirements folder....";

bash `echo ${project_path}`/pre-requirements/Miniconda2-latest-MacOSX-x86_64.sh -b -p `echo ${project_path}`/pre-requirements/vmreact_miniconda2;

#add conda executables to path
export PATH=$PATH:${project_path}/pre-requirements/vmreact_miniconda2/bin/

#verify installation
echo "verification of conda installation....."
conda info;

#update
# conda update conda;

#create vmreact env

echo "creating vmreact conda environment...."
conda env create --file `echo ${project_path}`/pre-requirements/vmreact_miniconda_env.yaml -p `echo ${project_path}`/pre-requirements/vmreact_miniconda2/envs/vmreact;

#conda config
# touch ${env_path}/.condarc;
# cat `echo {project_path}/pre-requirements/.condarc` > ${env_path}/.condarc;

echo "source activate `echo ${env_path}`" >> ~/.bashrc
echo "source ~/.bashrc" >> ~/.bash_profile
source ~/.bash_profile;

echo "running setup.py for installation....."

python setup.py install;

#activate env
source activate `echo ${env_path}`;
