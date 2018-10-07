#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import pandas
import sys
from collections import Counter


scored_data = pandas.read_csv('')
mturk = pandas.DataFrame(data=scored_data.set_index(
    ['gender', 'age_range']).loc[:, 'age':'trial7'])

age_ranges = {
    '18-25': range(18, 25, 1),
    '25-30': range(25, 30, 1),
    '30-35': range(30, 35, 1),
    '35-45': range(35, 45, 1),
    '45-55': range(45, 55, 1),
    '55-80': range(55, 80, 1)}


age_ranges1 = {
    '18-29': range(18, 30, 1),
    '30-39': range(30, 40, 1),
    '40-49': range(40, 50, 1),
    '50-59': range(50, 60, 1),
    '60-69': range(60, 70, 1),
    '70-79': range(70, 70, 1)}


m = dict()
m['female'] = []
m['male'] = []

f = mturk.loc['female'].get('age').values
males = mturk.loc['male'].get('age').values

females = f.tolist()
males = males.tolist()

m['female'] = females
m['male'] = males


m_kv = []
for key in m.keys():
    for value in m[key]:
        m_kv.append([key, value])

age_dicts = []
for k in sorted(age_ranges1.keys()):
    for a in sorted(age_ranges1[k]):
        print k, a
        age_dicts.append([k, a])


new_df_list = []
for i, v in enumerate(sorted(m_kv)):
    age_subj = str(v[1])
    for k, vl in enumerate(sorted(age_dicts)):
        age_dict = str(vl[1])
        if age_subj == age_dict:
            new_df_list.append([v[0], vl[0], age_subj])


new_df = pandas.DataFrame(data=new_df_list, columns=[
                          'gender', 'age_range', 'age'])
df = new_df.set_index('gender')


#
#print "MALE AND FEMALE BREAKDOWN WITH INQUISIT AGE_RANGES"
#print '*********************************'
#
#
# for ix,data in df.groupby('age_range'):
#    print ' '
#    print ix
#    males=data.loc['male']['age'].count()
#    print "number of N for males:" , males
#    num_m_agerange= abs(75 - males)
#    if males > 75:
#        print '75 subjects reached'
#    else:
#        print "needed on inquisit",num_m_agerange
#
#
#print '*********************************'
#print '*********************************'
# for ix,data1 in df.groupby('age_range'):
#    print ' '
#    print ix
#    females=data1.loc['female']['age'].count()
#    print "number of N for females" , females
#    num_per_agerange_f=abs(75-females)
#    if females > 75:
#        print '75 subjects reached'
#    else:
#        print "needed on inquisit", num_per_agerange_f
#        print ' '


print '*********************************'
print "MALE AND FEMALE BREAKDOWN WITH NEW BINNED AGE_RANGES"
print ' '

print '*** males***'
for idx, data in mturk.groupby(level=1):
    male_counts_per_agerange = data.loc['male']['trial1'].count()
    print ' '
    print idx
    num_males_needed_per_agerange = 75 - male_counts_per_agerange
    print 'current number of males:', male_counts_per_agerange
    print 'males needed to reach 75: ', num_males_needed_per_agerange


print '***females***'
for idx, data in mturk.groupby(level=1):
    if data.loc['female']['trial1'].count() > 75:
        print ' '
        print idx, data.loc['female']['trial1'].count()
        print '75 subjects reached'
    else:
        female_counts_per_agerange = data.loc['female']['trial1'].count()
        print ' '
        print idx
        num_females_needed_per_agerange = 75 - female_counts_per_agerange
        print 'current number of females:', female_counts_per_agerange
        print 'females needed to reach 75: ', num_females_needed_per_agerange
