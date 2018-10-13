
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
