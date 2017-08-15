import boto3
import json
import pickle

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
    aws.write_to_s3(
            data=result,
            bucket=event['result']['bucket'],
            folder=event['result']['folder'],
            key=key,
            s3_client=Split.s3_client
    )

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
def collect(event, context):
    result = event['result']

    X00 = x_0_0(result['bucket'], result['folder'], event['split'], event['unit'])
    X01 = x_0_1(result['bucket'], result['folder'], event['split'], event['unit'])
    X10 = x_1_0(result['bucket'], result['folder'], event['split'], event['unit'])
    X11 = x_1_1(result['bucket'], result['folder'], event['split'], event['unit'])

    base = "S{}_X{}_U{}".format(event['split'], "{}", event['unit'])
    aws.write_to_s3(X00, result['bucket'], result['folder'], base.format("00"), s3_client)
    aws.write_to_s3(X01, result['bucket'], result['folder'], base.format("01"), s3_client)
    aws.write_to_s3(X10, result['bucket'], result['folder'], base.format("10"), s3_client)
    aws.write_to_s3(X11, result['bucket'], result['folder'], base.format("11"), s3_client)

# COLLECTOR

def x_0_0(bucket, folder, split, unit):
    m_0 = load_interm_result(bucket, folder, split, unit, 0)
    m_3 = load_interm_result(bucket, folder, split, unit, 3)
    m_4 = load_interm_result(bucket, folder, split, unit, 4)
    m_6 = load_interm_result(bucket, folder, split, unit, 6)
    return m_0 + m_3 - m_4 + m_6

def x_0_1(bucket, folder, split, unit):
    m_2 = load_interm_result(bucket, folder, split, unit, 2)
    m_4 = load_interm_result(bucket, folder, split, unit, 4)
    return m_2 + m_4

def x_1_0(bucket, folder, split, unit):
    m_1 = load_interm_result(bucket, folder, split, unit, 1)
    m_3 = load_interm_result(bucket, folder, split, unit, 3)
    return m_1 + m_3

def x_1_1(bucket, folder, split, unit):
    m_0 = load_interm_result(bucket, folder, split, unit, 0)
    m_2 = load_interm_result(bucket, folder, split, unit, 2)
    m_1 = load_interm_result(bucket, folder, split, unit, 1)
    m_5 = load_interm_result(bucket, folder, split, unit, 5)
    return m_0 + m_2 - m_1 + m_5
  
def load_interm_result(bucket, folder, split, unit, x):
    filename = "S{}_U{}_m{}".format(split, unit, x)

    path = aws.download_s3_file(bucket, folder, filename, s3_client)
    return np.load(path)
