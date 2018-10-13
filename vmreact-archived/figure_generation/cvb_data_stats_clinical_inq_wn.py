#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:16:33 2017

@author: dawlat_local
"""

import scipy.stats as st
import pandas


#data
clinical_all=pandas.read_csv('/Volumes/daelsaid/cvb/best_clinical_comparison_cvb.csv')

data_wn_inq= pandas.read_csv('/Volumes/daelsaid/wn_recog_inq_recall.csv')



# WN vs Inquisit delayed recall
data_wn_inq.plot.hist()

inquisit=data_wn_inq.iloc[:,1:2].values
wn=data_wn_inq.iloc[:,2:3].values


rho, p = st.spearmanr(inquisit,wn)



#caps vs pcl for tp1

tp1_caps=clinical_all.iloc[2:24,1:2].values
tp1_pcl=clinical_all.iloc[2:24,2:3].values

clinical_all.plot.hist(y=['tp1_caps','tp1_pcl'], xlim=(0,80), ylim=(0,8), bins=12)


rho_c, p_c=st.spearmanr(tp1_caps,tp1_pcl)


fig = plt.figure()
ax = plt.subplot(111)
clinical_all.plot(x='tp1_caps',y='tp1_pcl',ax=ax, kind='scatter')
ax.set_xlim(20,55)
ax.set_ylim(20,80)


#pcl tp1 vs session1
df= clinical_all[['tp1_pc','pcl_clinics1']]

pcl_df1=df.dropna()

tp1_pcl=pcl_df1['tp1_pc'].values
pcl_clinic1=pcl_df1['pcl_clinics1'].values

rho_1,p_1=st.spearmanr(tp1_pcl,pcl_clinic1)



#pcl session 2, pcl sr 2


df_s2=clinical_all[['pcl_clinic_s2','sr2_pcl']]
session_2_pcl=df_s2.dropna()



print 'Inquisit Trial 7 delayed recall vs Webneuro Delayed Recognition'
print ' '
print 'N=23'
print 'rho:',rho, 'p:', p
print' '
print ' '


print 'TP1 CAPS DSM 5 Overall Scores vs. TP1 PCL DSM 5 Scores'
print ' '
print 'N=22'
print 'rho:', rho_c, 'p:', p_c
print ' '



print 'TP1 PCL Scores vs. Clinic Session 1 PCL-5 Scores'
print ' '
print 'N=14'
print 'rho:', rho_1, 'p:', p_1
print ' '

print 'Number of subjects per measure'
print clinical_all.count()





print plt.scatter(tp1_caps, tp1_pcl, c=['cyan','g'], )