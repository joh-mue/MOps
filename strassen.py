'''
event[''
{
  "method": "m_0",
  "matrix-X": "/strassen-test/X",
  "matrix-Y": "/strassen-test/Y",
  "bucket": "bucket-name"
}
'''

import boto3
import json
import pickle

### NUMPY, SCIPY, SKLEARN MAGIC
import os
import ctypes

for d, _, files in os.walk('lib'):
    for f in files:
        if f.endswith('.a'):
            continue
        ctypes.cdll.LoadLibrary(os.path.join(d, f))

import sklearn
import numpy as np
### NUMPY, SCIPY, SKLEARN MAGIC END

lambda_client = boto3.client('lambda')
s3_client = boto3.client('s3')

def handler(event, context):
  matX = load_matrix(event['matrix-X'])
  matY = load_matrix(event['matrix-Y'])
  # method = globals()[event['method']]

  intermediates = ["m_" + str(x) for x in range(0,7)]
  m = []
  for intermediate in intermediates:
    intermediate_method = globals()[intermediate]
    m.append(intermediate_method(matX, matY.transpose()))
    # print(partial)

  Q00 = m[0] + m[3] - m[4] + m[6]
  Q01 = m[2] + m[4]
  Q10 = m[1] + m[3]
  Q11 = m[0] + m[2] - m[1] + m[5]

  result = np.array([np.append(Q00[0], Q01[0]),
  np.append(Q00[1], Q01[1]),
  np.append(Q10[0], Q11[0]),
  np.append(Q10[1], Q11[1])])

  print(result)
  return { "Strassen correct": np.array_equal(result, matX.dot(matX.transpose())) }

  # write_to_s3(data, bucket, key, context)
  
  '''
  SYNTAX for modules:
  import foo
  method_to_call = getattr(foo, 'bar')
  result = method_to_call()
  '''

def load_matrix(matrix):
  return np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])

def split4(array, col, row):
  cols, rows = array.shape
  return array[(cols/2)*col:(cols+cols*col)/2, (rows/2)*row:(rows+rows*row)/2]

# INTERMEDIATE CALCULATIONS

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

# RESULT COLLECTION 

def q_0_0():
  m_0 = load_matrix(m_0)
  m_3 = load_matrix(m_3)
  m_4 = load_matrix(m_4)
  m_6 = load_matrix(m_6)
  return m_0 + m_3 - m_4 + m_6

def q_0_1():
  m_2 = load_matrix(m_2)
  m_4 = load_matrix(m_4)
  return m_2 + m_4

def q_1_0():
  m_1 = load_matrix(m_1)
  m_3 = load_matrix(m_3)
  return m_1 + m_3

def q_1_1():
  m_0 = load_matrix(m_0)
  m_2 = load_matrix(m_2)
  m_1 = load_matrix(m_1)
  m_5 = load_matrix(m_5)
  return m_0 + m_2 - m_1 + m_5

def load_from_s3(bucket, matrix_key):
  tmp_filepath = '/tmp/' + matrix_key
  s3_client.download_file(bucket, matrix_key, tmp_filepath)
  with open(tmp_filepath, 'rb') as tmp_file:
    matrix_data = pickle.load(tmp_file)
  return matrix_data

def write_to_s3(data, bucket, key, context):
  tmp_filepath = '/tmp/' + key
  
  with open(tmp_filepath, 'wb') as tmp_file:
    pickle.dump(data, tmp_file)

  s3_client.upload_file(tmp_filepath, bucket, key)
