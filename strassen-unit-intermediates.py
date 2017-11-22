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

deploy_nr = 'INT202'

s3_client = boto3.client('s3')

s3_upload_time = 0


# HANDLERS

'''
{
    "state-machine-name": "v4_to10_bs4k-8kx8k",
    "executionName": "v4_to10_bs4k-8kx8k",
    "matA": {
        "bucket": "jmue-multiplication-benchmarks",
        "folder": "sq_8kx8k_bs2k",
        "block-size": 2000,
        "columns": 8000,
        "rows": 8000
    },
    "matB": {
        "bucket": "jmue-multiplication-benchmarks",
        "folder": "sq_8kx8k_bs2k-2",
        "block-size": 2000,
        "columns": 8000,
        "rows": 8000
    },
    "result": {
        "bucket": "jmue-multiplication-benchmarks",
        "folder": "sq_8kx8k_bs2k-result",
        "block-size": 2000,
        "split": {
            "x": 0,
            "y": 0
        }
    },
    "split": 0,
    "unit": 0,
    "split-size": 4000
}


'''

def intermediate_0(event, context):
    return execute(m_0, 0, event, context)

def intermediate_1(event, context):
    return execute(m_1, 1, event, context)

def intermediate_2(event, context):
    return execute(m_2, 2, event, context)

def intermediate_3(event, context):
    return execute(m_3, 3, event, context)

def intermediate_4(event, context):
    return execute(m_4, 4, event, context)

def intermediate_5(event, context):
    return execute(m_5, 5, event, context)

def intermediate_6(event, context):
    return execute(m_6, 6, event, context)

def execute(intermediate_method, intermediate_index, event, context):
    execution_start = context.get_remaining_time_in_millis()

    result_split = Split(event['result'], event['result']['split'], event['split-size'])
    left_split = Split.left_inputsplit_for(event['matA'], result_split, event['unit'])
    right_split = Split.right_inputsplit_for(event['matB'], result_split, event['unit'])

    result = intermediate_method(left_split, right_split)
    upload_to_s3(result, event, context, key="S{}_U{}_m{}".format(event['split'], event['unit'], intermediate_index))

    aws.cleanup_tmp()
    return {
            'intermediate': intermediate_index,
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
