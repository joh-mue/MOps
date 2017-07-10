import boto3
import json
import pickle

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
  "matA": {
    "bucket": "jmue-matrix-tests",
    "key": "sq-staircase1000"
  },
  "matB": {
      "bucket": "jmue-matrix-tests",
      "key": "sq-staircase1000"
  },
  "result": {
      "bucket": "jmue-matrix-tests",
      "key": "staircase1000-result"
  },
  "intermediate": "m_*"
}
'''
def intermediate(event, context):
  intermediate_method = globals()[event['intermediate']]
  matA = load_matrix(event['matA'])
  matB = load_matrix(event['matB'])
  result = intermediate_method(matA, matB)
  # print result
  write_to_s3(result, event['result']['bucket'], event['intermediate'])

'''
{
  "result": {
    "bucket": "jmue-matrix-tests",
    "key": "staircase1000-result"
  }
}
'''
def collect(event, context):
  Q00 = q_0_0(event['result']['bucket'])
  Q01 = q_0_1(event['result']['bucket'])
  Q10 = q_1_0(event['result']['bucket'])
  Q11 = q_1_1(event['result']['bucket'])

  top = np.concatenate((Q00, Q01), axis=1)
  bottom = np.concatenate((Q10,Q11), axis=1)
  S = np.concatenate((top, bottom), axis=0)

  write_to_s3(S, event['result']['bucket'], event['result']['key'])

# INTERMEDIATE

def m_0(X, Y):
  return (split4(X,0,0) + split4(X,1,1)).dot(split4(Y,0,0) + split4(Y,1,1))

def m_1(X, Y):
  return (split4(X,1,0) + split4(X,1,1)).dot(split4(Y,0,0))

def m_2(X, Y):
  return split4(X,0,0).dot(split4(Y,0,1) - split4(Y,1,1))

def m_3(X, Y):
  return split4(X,1,1).dot(split4(Y,1,0) - split4(Y,0,0))

def m_4(X, Y):
  return (split4(X,0,0) + split4(X,0,1)).dot(split4(Y,1,1))

def m_5(X, Y):
  return (split4(X,1,0) - split4(X,0,0)).dot(split4(Y,0,0) + split4(Y,0,1))

def m_6(X, Y):
  return (split4(X,0,1) - split4(X,1,1)).dot(split4(Y,1,0) + split4(Y,1,1))

# COLLECTOR

def q_0_0(bucket):
  m_0 = load_matrix({ 'bucket': bucket, 'key': 'm_0'})
  m_3 = load_matrix({ 'bucket': bucket, 'key': 'm_3'})
  m_4 = load_matrix({ 'bucket': bucket, 'key': 'm_4'})
  m_6 = load_matrix({ 'bucket': bucket, 'key': 'm_6'})
  return m_0 + m_3 - m_4 + m_6

def q_0_1(bucket):
  m_2 = load_matrix({ 'bucket': bucket, 'key': 'm_2'})
  m_4 = load_matrix({ 'bucket': bucket, 'key': 'm_4'})
  return m_2 + m_4

def q_1_0(bucket):
  m_1 = load_matrix({ 'bucket': bucket, 'key': 'm_1'})
  m_3 = load_matrix({ 'bucket': bucket, 'key': 'm_3'})
  return m_1 + m_3

def q_1_1(bucket):
  m_0 = load_matrix({ 'bucket': bucket, 'key': 'm_0'})
  m_2 = load_matrix({ 'bucket': bucket, 'key': 'm_2'})
  m_1 = load_matrix({ 'bucket': bucket, 'key': 'm_1'})
  m_5 = load_matrix({ 'bucket': bucket, 'key': 'm_5'})
  return m_0 + m_2 - m_1 + m_5

# HELPERS

def load_matrix(matrix):
  if matrix == 'dummy':
    return np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
  else:
    # TODO: use download_fileobj so no file has to be written
    s3_client.download_file(matrix['bucket'], matrix['key'], '/tmp/' + matrix['key'])
    return np.load('/tmp/' + matrix['key'])

def split4(array, col, row):
  cols, rows = array.shape
  return array[(cols/2)*col:(cols+cols*col)/2, (rows/2)*row:(rows+rows*row)/2]

def load_from_s3(bucket, matrix_key):
  tmp_filepath = '/tmp/' + matrix_key
  s3_client.download_file(bucket, matrix_key, tmp_filepath)
  with open(tmp_filepath, 'rb') as tmp_file:
    matrix_data = pickle.load(tmp_file)
  return matrix_data

def write_to_s3(data, bucket, key):
  tmp_filepath = '/tmp/' + key
  
  with open(tmp_filepath, 'wb') as tmp_file:
    pickle.dump(data, tmp_file)

  s3_client.upload_file(tmp_filepath, bucket, key)
