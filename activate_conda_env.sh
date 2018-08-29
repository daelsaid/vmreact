#!/bin/bash

#install miniconda
bash ${PWD}/pre-requirements/Miniconda2-latest-MacOSX-x86_64.sh;


#add conda executables to path 
export PATH=$PATH:$PWD/pre-requirements/miniconda

#verify installation
conda info;
#update
conda update conda;

#create vmreact env
conda create --n vmreact;

#activate env
source activate vmreact;


#set configurations via condarc file
conda config $PWD/.condarc/envs/.condarc
