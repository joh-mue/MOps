import boto3
import json
import pickle
import time
from collections import namedtuple

import aws
from split import Split

### NUMPY, SCIPY, SKLEARN MAGIC
import os
import ctypes

import platform
if platform.system() != 'Darwin': # don't do this on my local machine
    for d, _, files in os.walk('lib'):
        for f in files:
            if f.endswith('.a'):
                continue
            ctypes.cdll.LoadLibrary(os.path.join(d, f))

import numpy as np
### NUMPY, SCIPY, SKLEARN MAGIC END

deploy_nr = 'INT200'

s3_client = boto3.client('s3')

s3_upload_time = 0


# HANDLERS

'''
{
  "stateMachineArn": "state-machine-arn",
  "executionName": "execution-name",
  "matA": {
    "bucket": "jmue-matrix-tests",
    "folder": "sc4000",
    "rows": 4000,
    "columns": 4000,
    "split": {
      "x1": 0,
      "y1": 0,
      "x2":2000,
      "y2":2000
    }
  },
  "matB": {
      "bucket": "jmue-matrix-tests",
      "folder": "sc4000t",
      "rows": 4000,
      "columns": 4000,
      "split": {
        "x1": 0,
        "y1": 0,
        "x2":2000,
        "y2":2000
      }
  },
  "result": {
      "bucket": "jmue-matrix-tests",
      "folder": "sc4000-result"
  },
  "splitSizeLimit": 2000,
  "intermediate": "2"
}
'''

def upload_to_s3(result, event, context, key):
  global s3_upload_time
  s3_upload_time = 0
  start = context.get_remaining_time_in_millis()
  aws.write_to_s3(
          data=result,
          bucket=event['result']['bucket'],
          folder=event['result']['folder'],
          key=key,
          s3_client=Split.s3_client
  )
  s3_upload_time = start - context.get_remaining_time_in_millis()

def intermediate_0(event, context):
  execution_start = context.get_remaining_time_in_millis()

  result_split = Split(event['result'], event['result']['split'])
  left_split = Split.left_inputsplit_for(event['matA'], result_split, event['unit'])
  right_split = Split.right_inputsplit_for(event['matB'], result_split, event['unit'])

  result = m_0(left_split, right_split)
  upload_to_s3(result, event, context, key="S{}_U{}_m0".format(event['split'], event['unit']))

  return {
          'intermediate': 0,
          'split': event['split'],
          'unit': event['unit'] ,
          'time-profile': {
              's3-up': s3_upload_time,
              's3-down': left_split.s3_download_time + right_split.s3_download_time,
              'execution': execution_start - context.get_remaining_time_in_millis(),
              'lambda': 'intermediate'
          },
          'deploy-nr': deploy_nr,
          'remaining_time_at_exec_start': execution_start
  }


def intermediate_1(event, context):
  execution_start = context.get_remaining_time_in_millis()

  result_split = Split(event['result'], event['result']['split'])
  left_split = Split.left_inputsplit_for(event['matA'], result_split, event['unit'])
  right_split = Split.right_inputsplit_for(event['matB'], result_split, event['unit'])

  result = m_1(left_split, right_split)
  upload_to_s3(result, event, context, key="S{}_U{}_m1".format(event['split'], event['unit']))

  return {
          'intermediate': 1,
          'split': event['split'],
          'unit': event['unit'] ,
          'time-profile': {
              's3-up': s3_upload_time,
              's3-down': left_split.s3_download_time + right_split.s3_download_time,
              'execution': execution_start - context.get_remaining_time_in_millis(),
              'lambda': 'intermediate'
          },
          'deploy-nr': deploy_nr,
          'remaining_time_at_exec_start': execution_start
  }


def intermediate_2(event, context):
  execution_start = context.get_remaining_time_in_millis()

  result_split = Split(event['result'], event['result']['split'])
  left_split = Split.left_inputsplit_for(event['matA'], result_split, event['unit'])
  right_split = Split.right_inputsplit_for(event['matB'], result_split, event['unit'])

  result = m_2(left_split, right_split)
  upload_to_s3(result, event, context, key="S{}_U{}_m2".format(event['split'], event['unit']))

  return {
          'intermediate': 2,
          'split': event['split'],
          'unit': event['unit'] ,
          'time-profile': {
              's3-up': s3_upload_time,
              's3-down': left_split.s3_download_time + right_split.s3_download_time,
              'execution': execution_start - context.get_remaining_time_in_millis(),
              'lambda': 'intermediate'
          },
          'deploy-nr': deploy_nr,
          'remaining_time_at_exec_start': execution_start
  }


def intermediate_3(event, context):
  execution_start = context.get_remaining_time_in_millis()

  result_split = Split(event['result'], event['result']['split'])
  left_split = Split.left_inputsplit_for(event['matA'], result_split, event['unit'])
  right_split = Split.right_inputsplit_for(event['matB'], result_split, event['unit'])

  result = m_3(left_split, right_split)
  upload_to_s3(result, event, context, key="S{}_U{}_m3".format(event['split'], event['unit']))

  return {
          'intermediate': 3,
          'split': event['split'],
          'unit': event['unit'] ,
          'time-profile': {
              's3-up': s3_upload_time,
              's3-down': left_split.s3_download_time + right_split.s3_download_time,
              'execution': execution_start - context.get_remaining_time_in_millis(),
              'lambda': 'intermediate'
          },
          'deploy-nr': deploy_nr,
          'remaining_time_at_exec_start': execution_start
  }


def intermediate_4(event, context):
  execution_start = context.get_remaining_time_in_millis()

  result_split = Split(event['result'], event['result']['split'])
  left_split = Split.left_inputsplit_for(event['matA'], result_split, event['unit'])
  right_split = Split.right_inputsplit_for(event['matB'], result_split, event['unit'])

  result = m_4(left_split, right_split)
  upload_to_s3(result, event, context, key="S{}_U{}_m4".format(event['split'], event['unit']))

  return {
          'intermediate': 4,
          'split': event['split'],
          'unit': event['unit'] ,
          'time-profile': {
              's3-up': s3_upload_time,
              's3-down': left_split.s3_download_time + right_split.s3_download_time,
              'execution': execution_start - context.get_remaining_time_in_millis(),
              'lambda': 'intermediate'
          },
          'deploy-nr': deploy_nr,
          'remaining_time_at_exec_start': execution_start
  }


def intermediate_5(event, context):
  execution_start = context.get_remaining_time_in_millis()

  result_split = Split(event['result'], event['result']['split'])
  left_split = Split.left_inputsplit_for(event['matA'], result_split, event['unit'])
  right_split = Split.right_inputsplit_for(event['matB'], result_split, event['unit'])

  result = m_5(left_split, right_split)
  upload_to_s3(result, event, context, key="S{}_U{}_m5".format(event['split'], event['unit']))

  return {
          'intermediate': 5,
          'split': event['split'],
          'unit': event['unit'] ,
          'time-profile': {
              's3-up': s3_upload_time,
              's3-down': left_split.s3_download_time + right_split.s3_download_time,
              'execution': execution_start - context.get_remaining_time_in_millis(),
              'lambda': 'intermediate'
          },
          'deploy-nr': deploy_nr,
          'remaining_time_at_exec_start': execution_start
  }


def intermediate_6(event, context):
  execution_start = context.get_remaining_time_in_millis()

  result_split = Split(event['result'], event['result']['split'])
  left_split = Split.left_inputsplit_for(event['matA'], result_split, event['unit'])
  right_split = Split.right_inputsplit_for(event['matB'], result_split, event['unit'])

  result = m_6(left_split, right_split)
  upload_to_s3(result, event, context, key="S{}_U{}_m6".format(event['split'], event['unit']))

  return {
          'intermediate': 6,
          'split': event['split'],
          'unit': event['unit'] ,
          'time-profile': {
              's3-up': s3_upload_time,
              's3-down': left_split.s3_download_time + right_split.s3_download_time,
              'execution': execution_start - context.get_remaining_time_in_millis(),
              'lambda': 'intermediate'
          },
          'deploy-nr': deploy_nr,
          'remaining_time_at_exec_start': execution_start
  }



# def intermediate(event, context):
#     execution_start = context.get_remaining_time_in_millis()

#     result_split = Split(event['result'], event['result']['split'])

#     left_split = Split.left_inputsplit_for(event['matA'], result_split, event['unit'])
#     right_split = Split.right_inputsplit_for(event['matB'], result_split, event['unit'])

#     intermediate_method = globals()["m_" + str(event['intermediate'])]
#     result = intermediate_method(left_split, right_split)
#     key = "S{}_U{}_m{}".format(event['split'], event['unit'], event['intermediate'])

#     start = context.get_remaining_time_in_millis()
#     aws.write_to_s3(
#             data=result,
#             bucket=event['result']['bucket'],
#             folder=event['result']['folder'],
#             key=key,
#             s3_client=Split.s3_client
#     )
#     s3_upload_time = start - context.get_remaining_time_in_millis()
#     execution_time = execution_start - context.get_remaining_time_in_millis()

#     return {
#             'intermediate': event['intermediate'],
#             'split': event['split'],
#             'unit': event['unit'] ,
#             'time-profile': {
#                 's3-up': s3_upload_time,
#                 's3-down': left_split.s3_download_time + right_split.s3_download_time,
#                 'execution': execution_time,
#                 'lambda': 'intermediate'
#             },
#             'deploy-nr': deploy_nr,
#             'remaining_time_at_exec_start': execution_start
#     }

# INTERMEDIATE METHODS
# x is left input split, y is the right input split

def m_0(x, y):
    return (x.block(0,0) + x.block(1,1)).dot(y.block(0,0) + y.block(1,1))

def m_1(x, y):
    return (x.block(1,0) + x.block(1,1)).dot(y.block(0,0))

def m_2(x, y):
    return x.block(0,0).dot(y.block(0,1) - y.block(1,1))

def m_3(x, y):
    return x.block(1,1).dot(y.block(1,0) - y.block(0,0))

def m_4(x, y):
    return (x.block(0,0) + x.block(0,1)).dot(y.block(1,1))

def m_5(x, y):
    return (x.block(1,0) - x.block(0,0)).dot(y.block(0,0) + y.block(0,1))

def m_6(x, y):
    return (x.block(0,1) - x.block(1,1)).dot(y.block(1,0) + y.block(1,1))

