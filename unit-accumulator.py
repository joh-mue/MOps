import boto3
import json
import aws

from collections import namedtuple

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

deploy_nr = 'ACC104'

s3_client = boto3.client('s3')

# HANDLERS

'''
accumulate.json
{
  'split': 3
}
'''
def accumulate(event, context):
    execution_start = context.get_remaining_time_in_millis()
    s3_download_time, s3_upload_time = 0, 0

    for block_index in ['00','01','10','11']:
        download_start = context.get_remaining_time_in_millis()
        partial_paths = load_all_partials(block_index, event['result'], event['split'])
        s3_download_time += download_start - context.get_remaining_time_in_millis()
        
        # add them up
        shape = (event['split-size']/2, event['split-size']/2)
        final_block = np.zeros(shape, dtype=np.float)
        for path in partial_paths:
            final_block += np.load(path)

        index = get_absolute_block_index(block_index, event['result']['split'], event['split-size'])

        upload_start = context.get_remaining_time_in_millis()
        aws.write_to_s3(
                data=final_block,
                bucket=event['result']['bucket'],
                folder=event['result']['folder'],
                key='m_{}_{}'.format(index.x, index.y),
                s3_client=s3_client)
        s3_upload_time += upload_start - context.get_remaining_time_in_millis()

    execution_time = execution_start - context.get_remaining_time_in_millis()
    return {
            'time-profile':{
                's3-up': s3_upload_time,
                's3-down': s3_download_time,
                'execution': execution_time,
                'lambda': 'accumulate'
            },
            'deploy-nr': deploy_nr,
            'remaining_time_at_exec_start': execution_start
    }

def load_all_partials(block_index, result, split):
    response = s3_client.list_objects_v2(
            Bucket=result['bucket'],
            Prefix='{}/S{}_X{}'.format(result['folder'], split, block_index))

    if not os.path.exists('/tmp/' + result['folder']):
        os.mkdir('/tmp/' + result['folder'])

    paths = []
    for item in response['Contents']:
        local_path = '/tmp/' + item['Key']
        s3_client.download_file(result['bucket'], item['Key'], local_path)
        paths.append(local_path)

    return paths

def get_absolute_block_index(block_index, split, split_size):
    x, y = int(block_index[0]), int(block_index[1])
    x += split['x']/1000
    y += split['y']/1000
    
    Index = namedtuple('Index', ['x','y'])
    block_size = split_size/2 # block is half as long as a split
    print("x:{}y:{}".format(x,y))
    return Index(x, y)
