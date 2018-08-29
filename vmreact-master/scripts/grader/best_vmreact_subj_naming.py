from glob import glob
import os
import datetime
import pandas as pd

format = "%Y_%m_%d"
current_date = datetime.datetime.today()
date = current_date.strftime(format)


def best_rename_with_subj(subj_dir):
	files=glob(os.path.join(subj_dir,'*.csv'))

	for file in range(0,len(files)):
		fullpath=files[file]
		fname=os.path.basename(fullpath)
		path=os.path.dirname(fullpath)
		old=os.path.join(path,fname)
		prefix_id=fullpath.split('/')[-3]
		new=os.path.join(path,'best_'+prefix_id.split('_')[1]+'_'+prefix_id.split('_')[2]+'_'+fname)
		try:
			os.rename(old,new)
		except OSError:
			print 'file note found:', old
