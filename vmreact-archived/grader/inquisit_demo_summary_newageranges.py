import os
import csv
import collections

def demo_and_summary_new(all_subj_data_csv,demographic_data,subj_age_agerange_gender):

    with open(all_subj_data_csv,'U') as file:
        input_csv_lines_all_subj = csv.reader(file)
        input_csv_lines_all_subj= map(list, zip(*input_csv_lines_all_subj))          
        all_subj_csv_lines = dict((rows[0],rows[1:]) for rows in input_csv_lines_all_subj)

    with open(demographic_data,'U') as file:
        input_demo_sr_q_csv = csv.reader(file)
        input_demo_sr_q_csv= map(list, zip(*input_demo_sr_q_csv))          
        demographic_data = dict((rows[0],rows[1:]) for rows in (input_demo_sr_q_csv))


    age_ranges = {
        '20-29': range(20,30,1),
        '30-39': range(30,40,1),
        '40-49': range(40,50,1),
        '50-59': range(50,60,1),
        '60-69': range(60,70,1),
        '70-90': range(70,90,1)}

    subj_id_list_demo=[]
    subj_id_only_demo=[]

    for subject in sorted(set(all_subj_csv_lines['subject'])):
        subj_id_only_demo.append(subject)
        subj_id_list_combined = [demographic_data['subject'][x] for x in range(len(demographic_data['subject'])) if demographic_data['subject'][x] == subject]
        subj_id_list_demo.append(subj_id_list_combined)

    subj_id_combined=[(idx,val) for idx,val in enumerate(sorted(subj_id_only_demo))]

    subj_val=[]
    key_val_all=[]
    for key in sorted(demographic_data.keys()):
        for value in sorted(demographic_data[key]):
            key_val_all.append([key,value])
            if 'subject' in key:
                subj_val.append(value)
            else:
                continue

    subj_id_with_index=list()
    for subj_num in subj_val:
        subj_combined=[[idx,val] for idx,val in enumerate(sorted(subj_id_only_demo)) if val == subj_num]
        subj_indexvals=[[idx,val] for idx,val in enumerate(sorted(subj_id_only_demo))]
        subj_id_with_index.append(subj_combined)


    subj_age_gender_mem=[]
    x=[]
    for idx2,subj_id in enumerate(subj_id_only_demo):
        subj_age_gen = [[demographic_data['subject'][x], demographic_data['gender_response'][x].lower(), demographic_data['age_textbox_response'][x]] for x in range(len(demographic_data['subject'])) if demographic_data['subject'][x] == subj_id]
        y= [[demographic_data['subject'][x]] for x in range(len(demographic_data['subject'])) if demographic_data['subject'][x] == subj_id]
        subj_age_gender_mem.append(subj_age_gen)


    demo_subj_age_gender =[[demographic_data['subject'][x], demographic_data['gender_response'][x].lower(), demographic_data['age_textbox_response'][x]]
                           for x in range(len(demographic_data['subject']))
                           if demographic_data['subject'][x]]

    raw_data_responses= [[all_subj_csv_lines['subject'][x],all_subj_csv_lines['trialcode'][x], all_subj_csv_lines['response'][x].lower()]
                         for x in range(len(all_subj_csv_lines['subject']))
                         if 'recall_response' in all_subj_csv_lines['trialcode'][x]]


    key_val=[]
    for key in age_ranges.keys():
        for val in age_ranges[key]:
            key_val.append([key, val])

    id_age_agerange=[]
    with open(subj_age_agerange_gender, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['subj_id','age', 'age_range', 'gender'])
        for subj in sorted(demo_subj_age_gender):
            subj_from_main_raw_list=[]
            ages=subj[2]
            gender=subj[1]
            subj_id_raw=[val for val in raw_data_responses if val[0] == subj[0]]
            for vals in key_val:
                age_vals=vals[1]
                age_vals=str(age_vals)
                if age_vals == ages:
                    complete_list = subj[0] + ',' + age_vals + "," + vals[0] + "," +  gender 
                    id_age_agerange.append(complete_list)
                    writer.writerow([subj[0], age_vals, vals[0],gender])
    csvfile.close()





