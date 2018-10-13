#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 12:04:33 2018

@author: dawlat_local
"""

import datetime
from composite_scores import composite_scores

import sys
import os

input_csv=sys.argv[1]
output_path=sys.argv[2]

format = "%Y_%m_%d"
current_date=datetime.datetime.today()
date = current_date.strftime(format)


output_csv=os.path.join(output_path,'composite_scores_vakil'+ '_'+ date + '.csv')

composite_scores(1,input_csv,output_csv)
