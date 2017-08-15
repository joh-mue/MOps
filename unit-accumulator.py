import boto3
import json
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

s3_client = boto3.client('s3')

# HANDLERS

'''
accumulate.json
{
  "split": 3
}
'''
def accumulate(event, context):
    for block_index in ["00","01","10","11"]:
        partial_paths = load_all_partials(block_index, event['result'], event['split'])
        
        # add them up
        final_block = np.zeros(shape=(1000,1000), dtype=np.int)
        for path in partial_paths:
          final_block += np.load(path)

        index = get_absolute_block_index(block_index, event['result']['split'])

        aws.write_to_s3(
                data=final_block,
                bucket=event['result']['bucket'],
                folder=event['result']['folder'],
                key="X{}{}".format(index[0], index[1]),
                s3_client=s3_client)

def load_all_partials(block_index, result, split):
    response = s3_client.list_objects_v2(
            Bucket=result['bucket'],
            Prefix="{}/S{}_X{}".format(result['folder'], split, block_index))

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
    x += split['x1']/1000
    y += split['y1']/1000
    block_size = split_size/2 # block is half as long as a split
    return (block_size*x, block_size*y)
