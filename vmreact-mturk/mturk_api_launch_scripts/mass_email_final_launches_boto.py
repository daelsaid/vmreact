
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 13:30:41 2017

@author: dawlat_local
"""

import boto3
from boto.mturk.connection import *
import boto.mturk.connection

sandbox_host = 'mechanicalturk.sandbox.amazonaws.com'
real_host = 'mechanicalturk.amazonaws.com'

access_key=''
secret_key=''


mturk = boto.mturk.connection.MTurkConnection(
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key,
    host = real_host,
    debug = 2 # debug = 2 prints out all requests. but we'll just keep it at 1
)

test=mturk.get_all_hits()

print mturk.
current_rey_id='3I01FDIL6M78RQKKPWFLHBJZXC32DI'
f5_20s='3087LXLJ6MFYT0V21F6XMNT5C0MF0R'
test.search_qualification_types(sort_by='Name', page_size=10, page_number=1)
# c=boto.mturk.connection.MTurkConnection(access_key,secret_key)

# c.get_account_balance()

for t in test:
    print list(chain(*t))

test=c.get_all_hits()
response = mturk.list_hits(
    NextToken='string',
    MaxResults=50)



worker_ids=[]

subject='Eligible for 10$ HIT!'

message="""you are eligible for the $10 HIT! Please search for "Learning and Attention Task" for 10$.
You will be able to see it due to being assigned this qualification type.
You have 2 days to complete this HIT before we revoke access to completing the task."""


for id in worker_ids:
    c.notify_workers(item, subject, message)



#service_url=https://mechanicalturk.sandbox.amazonaws.com/?Service=AWSMechanicalTurkRequester

# If you want to have your solution work against the Amazon Mechnical Turk Production site (http://www.mturk.com)
# use the service_url defined below:
service_url=https://mechanicalturk.amazonaws.com/?Service=AWSMechanicalTurkRequester


region_name = 'us-east-1'
aws_access_key_id = ['AKIAIEHUSR6DIJ7ENRLA']
aws_secret_access_key = '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'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

# Uncomment this line to use in production
# endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# This will return $10,000.00 in the MTurk Developer Sandbox
print(client.get_account_balance()['AvailableBalance'])

QuestionForm <- paste0(readLines('Test.xml'), collapse='')
AnswerKey <- paste0(readLines('AnswerKey.xml'), collapse='')

# Created the QualificationType
newqual <- CreateQualificationType(name="Qualification",
                                   description="AgexGender Qualification",
                                   status="Active", test.duration=seconds(hours=1),
                                   test=qual_test, answerkey = answer_key)




import boto3

# Before connecting to MTurk, set up your AWS account and IAM settings as described here:
# https://blog.mturk.com/how-to-use-iam-to-control-api-access-to-your-mturk-account-76fe2c2e66e2
#
# Follow AWS best practices for setting up credentials here:
# http://boto3.readthedocs.io/en/latest/guide/configuration.html

# Use the Amazon Mechanical Turk Sandbox to publish test Human Intelligence Tasks (HITs) without paying any money.
# Sign up for a Sandbox account at https://requestersandbox.mturk.com/ with the same credentials as your main MTurk account.
client = boto3.client(
    service_name = 'mturk',
    endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
)

# Uncomment the below to connect to the live marketplace
# Region is always us-east-1
# client = boto3.client(service_name = 'mturk', region_name='us-east-1')

# Test that you can connect to the API by checking your account balance
user_balance = client.get_account_balance()

# In Sandbox this always returns $10,000
print "Your account balance is {}".format(user_balance['AvailableBalance'])

questionSampleFile = open("/Users/lillyel-said/Desktop/stanford/scripts/inquisit/mturk_qualification_questions_and_key.xml", "r")
questionSample = questionSampleFile.read()

qual=client.create_qualification_type('test', 'test', 'Active', 'string', 1,, answer_key='/Users/lillyel-said/Desktop/stanford/scripts/inquisit/answer_key.xml', answer_key_xml='/Users/lillyel-said/Desktop/stanford/scripts/inquisit/answer_key.xml', test_duration=600, auto_granted=True, auto_granted_value=1)



# Create a qualification with Locale In('US', 'CA') requirement attached
round1_1= [{
    'QualificationTypeId': '00000000000000000060',
    'Comparator': 'EqualTo',
    'IntegerValues':[{'test':'1'}],
    'RequiredToPreview': True
}]

round1_2= [{
    'QualificationTypeId': '2',
    'Comparator': 'EqualTo',
    'RequiredToPreview': True
}]

round1_3= [{
    'QualificationTypeId': '3',
    'Comparator': 'EqualTo',
    'RequiredToPreview': True
}]


round1_4= [{
    'QualificationTypeId': '4',
    'Comparator': 'EqualTo',
    'RequiredToPreview': True
}]

round1_5= [{
    'QualificationTypeId': '5',
    'Comparator': 'EqualTo',
    'RequiredToPreview': True
}]

localRequirements = [{
    'QualificationTypeId': '00000000000000000071',
    'Comparator': 'In',
    'LocaleValues': [{
        'Country': 'US'
    }, {
        'Country': 'CA'
    }],
    'RequiredToPreview': True

}]



response = client.create_hit(
    MaxAssignments=123,
    AutoApprovalDelayInSeconds=123,
    LifetimeInSeconds=123,
    AssignmentDurationInSeconds=123,
    Reward='string',
    Title='string',
    Keywords='string',
    Description='string',
    Question='string',
    RequesterAnnotation='string',
    QualificationRequirements=[
        {
            'QualificationTypeId': 'string',
            'Comparator': 'EqualTo',
            'IntegerValues':[123],
            'LocaleValues': [
                {
                    'Country': 'string',
                    'Subdivision': 'string'
                },
            ],
            'RequiredToPreview': True,
        },
    ],
)
# Create the HIT
round1_male_1 = client.create_hit(
    MaxAssignments = 9,
    LifetimeInSeconds = 600,
    AssignmentDurationInSeconds = 600,
    Reward ='0.40',
    Title = 'Answer a simple question',
    Keywords = 'question, answer, research',
    Description = 'Answer a simple question',
    Question = questionSample,
    QualificationRequirements = localRequirements,
)


round1_male_2 = client.create_hit(
    MaxAssignments = 28,
    LifetimeInSeconds = 600,
    AssignmentDurationInSeconds = 600,
    Reward ='0.40',
    Title = 'Answer a simple question',
    Keywords = 'question, answer, research',
    Description = 'Answer a simple question',
    Question = questionSample,
    QualificationRequirements =round1_2
)


round1_male_3 = client.create_hit(
    MaxAssignments = 19,
    LifetimeInSeconds = 600,
    AssignmentDurationInSeconds = 600,
    Reward ='0.40',
    Title = 'Answer a simple question',
    Keywords = 'question, answer, research',
    Description = 'Answer a simple question',
    Question = questionSample,
    QualificationRequirements = round1_3
)



round1_male_4 = client.create_hit(
    MaxAssignments = 32,
    LifetimeInSeconds = 600,
    AssignmentDurationInSeconds = 600,
    Reward ='0.40',
    Title = 'Answer a simple question',
    Keywords = 'question, answer, research',
    Description = 'Answer a simple question',
    Question = questionSample,
    QualificationRequirements = round1_4
)



round1_male_5 = client.create_hit(
    MaxAssignments = 63,
    LifetimeInSeconds = 600,
    AssignmentDurationInSeconds = 600,
    Reward ='0.40',
    Title = 'Answer a simple question',
    Keywords = 'question, answer, research',
    Description = 'Answer a simple question',
    Question = questionSample,
    QualificationRequirements = round1_5
)
# The response included several fields that will be helpful later
hit_type_id = response['HIT']['HITTypeId']
hit_id = response['HIT']['HITId']
print "Your HIT has been created. You can see it at this link:"
print "https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id)
print "Your HIT ID is: {}".format(hit_id)
