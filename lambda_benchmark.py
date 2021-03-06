import os
import boto3
import sys
import os
import time

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

def build_matrix(matrix_name, dimension, block_size):
    rows = []
    for i in range(0,dimension/block_size):
        blocks = []
        for j in range(0,dimension/block_size):
            blocks.append(np.load('/tmp/{}/m_{}_{}.npy'.format(matrix_name,i,j)))
        rows.append(np.vstack(blocks))
    return np.hstack(rows)

def download_s3_file(bucket, matrix_name, key):
    if not os.path.exists('/tmp/' + matrix_name):
        os.mkdir('/tmp/' + matrix_name)

    s3_client.download_file(bucket, key, '/tmp/' + key)
    return '/tmp/' + key


def download_all_matrix_parts(bucket, keys, matrix_name):
    paths = []
    for key in keys:
        paths.append(download_s3_file(bucket, matrix_name, key))
    return paths


def get_all_keys_for_matrix(matrix_name):
    response = s3_client.list_objects_v2(
        Bucket='jmue-multiplication-benchmarks',
        Delimiter='string',
        Prefix=matrix_name + '/'
    )

    keys = []
    print response
    for item in response['Contents']:
        keys.append(item['Key'])

    return keys


def benchmark(event, context):
    execution_start = time.time()
    dimension = event['dimension']
    block_size = event['block-size']

    matrix_A_name = 'sq_{}kx{}k_bs{}k'.format(dimension, dimension, block_size)
    matrix_B_name = 'sq_{}kx{}k_bs{}k-2'.format(dimension, dimension, block_size)

    bucket = 'jmue-multiplication-benchmarks'


    print("Getting all keys and download matrices")
    start = time.time()
    for matrix_name in [matrix_A_name, matrix_B_name]:
        keys = get_all_keys_for_matrix(matrix_name)
        download_all_matrix_parts(bucket, keys, matrix_name)

    end = time.time()
    download_time = end - start

    print("Building matrices")
    matA = build_matrix(matrix_name, dimension, block_size)
    matB = build_matrix(matrix_name, dimension, block_size)

    print("performing calculation")
    start = time.time()
    result = matA.dot(matB)
    end = time.time()
    calculation_time = end - start

    del matA
    del matB

    print("Splitting and uploading result")
    start = time.time()
    rows = np.hsplit(result, dimension/block_size)
    for i, row in enumerate(rows):
        blocks = np.vsplit(row, dimension/block_size)
        for j, block in enumerate(blocks):
            s3_client.put_object(Body=block.dumps(), Bucket=bucket, Key=matrix_name + '-lambda-result/' + 'm_{}_{}'.format(i,j))
    end = time.time()
    upload_time = end - start

    execution_end = time.time()
    execution_time = execution_end - execution_start

    print('download_time: ', int(download_time * 1000))
    print('calculation_time: ', int(calculation_time * 1000))
    print('upload_time: ', int(upload_time * 1000))
    print('execution_time: ', int(execution_time * 1000))

    call('rm -rf /tmp/*', shell=True)

    return {
        'download_time': int(download_time * 1000),
        'calculation_time': int(calculation_time * 1000),
        'upload_time': int(upload_time * 1000),
        'execution_time': int(execution_time * 1000),
    }

# sls invoke --function lambda_benchmark --path events/lambda_benchmark.json
# {
#     "execution_time": 49435,
#     "download_time": 3908,
#     "upload_time": 2930,
#     "calculation_time": 42168
# }
