import boto3
import json
import pickle
import time
from collections import namedtuple

import aws

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

deploy_nr = 'COL110'

s3_client = boto3.client('s3')

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
cached_files = 0
loaded_files = 0
m = {} # in memory cache for intermediate results

def handler(event, context):
    execution_start = context.get_remaining_time_in_millis()
    global s3_download_time
    global cached_files
    s3_download_time = 0
    cached_files = 0
    loaded_files = 0
    m = {}

    result = event['result']
    OperationMetaData = namedtuple('OperationMetaData', ['bucket', 'folder', 'split', 'unit'])
    op_meta_data = OperationMetaData(result['bucket'], result['folder'], event['split'], event['unit'])

    aws.cleanup_tmp()
    base = "S{}_X{}_U{}".format(event['split'], "{}", event['unit'])
    s3_upload_time = 0

    X = x_0_0(op_meta_data)
    start = context.get_remaining_time_in_millis()
    aws.write_to_s3(X, result['bucket'], result['folder'], base.format("00"), s3_client)
    end = context.get_remaining_time_in_millis()
    s3_upload_time += start - end
    aws.cleanup_tmp()

    X = x_0_1(op_meta_data)
    start = context.get_remaining_time_in_millis()
    aws.write_to_s3(X, result['bucket'], result['folder'], base.format("01"), s3_client)
    end = context.get_remaining_time_in_millis()
    s3_upload_time += start - end
    aws.cleanup_tmp()

    X = x_1_0(op_meta_data)
    start = context.get_remaining_time_in_millis()
    aws.write_to_s3(X, result['bucket'], result['folder'], base.format("10"), s3_client)
    end = context.get_remaining_time_in_millis()
    s3_upload_time += start - end
    aws.cleanup_tmp()


    X = x_1_1(op_meta_data)
    start = context.get_remaining_time_in_millis()
    aws.write_to_s3(X, result['bucket'], result['folder'], base.format("11"), s3_client)
    end = context.get_remaining_time_in_millis()
    s3_upload_time += start - end

    execution_time = execution_start - context.get_remaining_time_in_millis()

    return {
            'time-profile': {
                's3-up': s3_upload_time,
                's3-down': s3_download_time,
                'execution': execution_time,
                'lambda': 'collect'
            },
            'deploy-nr': deploy_nr,
            'remaining_time_at_exec_start': execution_start,
            'cached-files': cached_files,
            'loaded-files': loaded_files
    }


def load_interm_result(op_meta_data, x):
    global s3_download_time
    global cached_files
    global loaded_files

    filename = 'S{}_U{}_m{}'.format(op_meta_data.split, op_meta_data.unit, x)
    path = os.path.join('/tmp/', op_meta_data.folder, filename)
    if os.path.exists(path) | m.has_key(x):
        cached_files += 1
        return m[x]
    else:
        start = time.time()
        path = aws.download_s3_file(op_meta_data.bucket, op_meta_data.folder, filename, s3_client)
        end = time.time()
        s3_download_time = s3_download_time + int((end - start) * 1000)
        loaded_files += 1

    return np.load(path)


def x_0_0(op_meta_data):
    m[0] = load_interm_result(op_meta_data, 0)
    m[3] = load_interm_result(op_meta_data, 3)
    m[4] = load_interm_result(op_meta_data, 4)
    m[6] = load_interm_result(op_meta_data, 6)
    return m[0] + m[3] - m[4] + m[6]

def x_0_1(op_meta_data):
    m[2] = load_interm_result(op_meta_data, 2)
    m[4] = load_interm_result(op_meta_data, 4)
    return m[2] + m[4]

def x_1_0(op_meta_data):
    m[1] = load_interm_result(op_meta_data, 1)
    m[3] = load_interm_result(op_meta_data, 3)
    return m[1] + m[3]

def x_1_1(op_meta_data):
    m[0] = load_interm_result(op_meta_data, 0)
    m[2] = load_interm_result(op_meta_data, 2)
    m[1] = load_interm_result(op_meta_data, 1)
    m[5] = load_interm_result(op_meta_data, 5)
    return m[0] + m[2] - m[1] + m[5]
