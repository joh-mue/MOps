import os
import boto3
import numpy as np
import sys
import os
import time


s3_client = boto3.client('s3')

def build_matrix(paths, dimension):
    m_0_0 = np.load(paths[0])
    m_1_0 = np.load(paths[1])
    m_0_1 = np.load(paths[2])
    m_1_1 = np.load(paths[3])

    top = np.hstack((m_0_0, m_0_1))
    del m_0_0
    del m_0_1
    bottom =  np.hstack((m_1_0, m_1_1))
    del m_1_0
    del m_1_1
    return np.vstack((top, bottom))

def download_s3_file(bucket, matrix_name, key):
    if not os.path.exists('/tmp/' + matrix_name):
        os.mkdir('/tmp/' + matrix_name)

    s3_client.download_file(bucket, key, '/tmp/' + key)
    return '/tmp/' + key


def download_all_matrix_parts(keys, matrix_name):
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
    for item in response['Contents']:
        keys.append(item['Key'])

    return keys


if __name__ == "__main__":
    execution_start = time.time()
    dimension = sys.argv[1]
    dimension = sys.argv[2]

    matrix_A_name = 'sq_{}kx{}k_bs{}k'.format(dimension, dimension, blocksize)
    matrix_B_name = 'sq_{}kx{}k_bs{}k-2'.format(dimension, dimension, blocksize)

    bucket = 'jmue-multiplication-benchmarks'

    print("Getting all keys")
    keys_A = get_all_keys_for_matrix(matrix_A_name)
    keys_B = get_all_keys_for_matrix(matrix_B_name)

    print(keys_A)
    print(keys_B)

    print("Downloading matrix A")
    start = time.time()
    paths_A = download_all_matrix_parts(keys_A, matrix_A_name)

    print("Downloading matrix B")
    paths_B = download_all_matrix_parts(keys_B, matrix_B_name)
    end = time.time()
    download_time = end - start

    print("Building matrices")
    matA = build_matrix(paths_A, dimension)
    matB = build_matrix(paths_B, dimension)

    print("performing calculation")
    start = time.time()
    result = matA.dot(matB)
    end = time.time()
    calculation_time = end - start

    del matA
    del matB

    print("Splitting result")
    top, bottom = np.vsplit(result,2)
    del result
    m_0_0, m_0_1 = np.hsplit(top, 2)
    del top
    m_1_0, m_1_1 = np.hsplit(bottom, 2)
    del bottom

    print("uploading results")
    start = time.time()
    s3_client.put_object(Body=m_0_0.dumps(), Bucket=bucket, Key=os.path.join(matrix_A_name+'-ec2result', 'm_0_0'))
    s3_client.put_object(Body=m_0_1.dumps(), Bucket=bucket, Key=os.path.join(matrix_A_name+'-ec2result', 'm_0_1'))
    s3_client.put_object(Body=m_1_0.dumps(), Bucket=bucket, Key=os.path.join(matrix_A_name+'-ec2result', 'm_1_0'))
    s3_client.put_object(Body=m_1_1.dumps(), Bucket=bucket, Key=os.path.join(matrix_A_name+'-ec2result', 'm_1_1'))
    end = time.time()
    upload_time = end - start

    execution_end = time.time()
    execution_time = execution_end - execution_start

    print('download_time: ', int(download_time * 1000))
    print('calculation_time: ', int(calculation_time * 1000))
    print('upload_time: ', int(upload_time * 1000))
    print('execution_time: ', int(execution_time * 1000))
