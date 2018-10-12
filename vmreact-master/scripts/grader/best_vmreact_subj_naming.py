#!/usr/bin/env python2

from glob import glob
import os
import datetime
import pandas as pd

format = "%Y_%m_%d"
current_date = datetime.datetime.today()
date = current_date.strftime(format)


def best_rename_with_subj(subj_dir, site_name):
    files = glob(os.path.join(subj_dir, '*.csv'))
    for file in range(0, len(files)):
        fullpath = files[file]
        fname = os.path.basename(fullpath)
        path = os.path.dirname(fullpath)
        old = os.path.join(path, fname)
        prefix_id = fullpath.split('/')[-3]
        if 'new_mex' in site_name:
            new_mex_specific_id = os.path.join(
                path, 'best_newmex_' + prefix_id.split('-')[0] + '_' + fname)
            print new_mex_specific_id
            try:
                os.rename(old, new_mex_specific_id)
            except OSError:
                print 'file note found:', old
        elif 'stanford' in site_name:
            best_specific_fname = os.path.join(
                path, 'best_' + prefix_id.split('_')[1] + '_' + prefix_id.split('_')[2] + '_' + fname)
            try:
                os.rename(old, best_specific_fname)
            except OSError:
                print 'file note found:', old
    return files
