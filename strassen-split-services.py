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

deploy_nr = 'UNI102'

s3_client = boto3.client('s3')

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
def intermediate(event, context):
    result_split = Split(event['result'], event['result']['split'])

    left_split = Split.left_inputsplit_for(event['matA'], result_split, event['unit'])
    right_split = Split.right_inputsplit_for(event['matB'], result_split, event['unit'])

    intermediate_method = globals()["m_" + str(event['intermediate'])]
    result = intermediate_method(left_split, right_split)
    key = "S{}_U{}_m{}".format(event['split'], event['unit'], event['intermediate'])
    
    start = context.get_remaining_time_in_millis()
    aws.write_to_s3(
            data=result,
            bucket=event['result']['bucket'],
            folder=event['result']['folder'],
            key=key,
            s3_client=Split.s3_client
    )
    s3_upload_time = start - context.get_remaining_time_in_millis()

    return {
            'intermediate': event['intermediate'],
            'split': event['split'],
            'unit': event['unit'] ,
            'time-profile': {
                's3-up': s3_upload_time,
                's3-down': left_split.s3_download_time + right_split.s3_download_time,
                'execution': 300000 - context.get_remaining_time_in_millis(),
                'lambda': 'intermediate'
            },
            'deploy-nr': deploy_nr
    }

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

'''
### COLLECTOR
{
  "result": {
    "bucket": "jmue-matrix-tests",
    "folder": "staircase1000-result"
  }
}
'''
s3_download_time = 0

def collect(event, context):
    s3_upload_time = 0
    result = event['result']

    OperationMetaData = namedtuple('OperationMetaData', ['bucket', 'folder', 'split', 'unit'])
    op_meta_data = OperationMetaData(result['bucket'], result['folder'], event['split'], event['unit']) 

    X00 = x_0_0(op_meta_data)
    X01 = x_0_1(op_meta_data)
    X10 = x_1_0(op_meta_data)
    X11 = x_1_1(op_meta_data)

    base = "S{}_X{}_U{}".format(event['split'], "{}", event['unit'])
    start = context.get_remaining_time_in_millis()
    aws.write_to_s3(X00, result['bucket'], result['folder'], base.format("00"), s3_client)
    aws.write_to_s3(X01, result['bucket'], result['folder'], base.format("01"), s3_client)
    aws.write_to_s3(X10, result['bucket'], result['folder'], base.format("10"), s3_client)
    aws.write_to_s3(X11, result['bucket'], result['folder'], base.format("11"), s3_client)
    end = context.get_remaining_time_in_millis()
    s3_upload_time = start - end
    
    return {
            'time-profile': {
                's3-up': s3_upload_time,
                's3-down': s3_download_time,
                'execution': 300000 - context.get_remaining_time_in_millis(),
                'lambda': 'collect'
            },
            'deploy-nr': deploy_nr
    }

# COLLECTOR

def x_0_0(op_meta_data):
    m_0 = load_interm_result(op_meta_data, 0)
    m_3 = load_interm_result(op_meta_data, 3)
    m_4 = load_interm_result(op_meta_data, 4)
    m_6 = load_interm_result(op_meta_data, 6)
    return m_0 + m_3 - m_4 + m_6

def x_0_1(op_meta_data):
    m_2 = load_interm_result(op_meta_data, 2)
    m_4 = load_interm_result(op_meta_data, 4)
    return m_2 + m_4

def x_1_0(op_meta_data):
    m_1 = load_interm_result(op_meta_data, 1)
    m_3 = load_interm_result(op_meta_data, 3)
    return m_1 + m_3

def x_1_1(op_meta_data):
    m_0 = load_interm_result(op_meta_data, 0)
    m_2 = load_interm_result(op_meta_data, 2)
    m_1 = load_interm_result(op_meta_data, 1)
    m_5 = load_interm_result(op_meta_data, 5)
    return m_0 + m_2 - m_1 + m_5
  
def load_interm_result(op_meta_data, x):
    filename = 'S{}_U{}_m{}'.format(op_meta_data.split, op_meta_data.unit, x)
    
    start = time.time()
    path = aws.download_s3_file(op_meta_data.bucket, op_meta_data.folder, filename, s3_client)
    end = time.time()
    s3_download_time += int((end - start) * 1000)

    return np.load(path)
