import boto3
import json

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
  "matrix-X": "matrix-X",
  "matrix-Y": "matrix-Y",
  "result-bucket": "result-bucket"
}
'''
def master(event, context):
  lambda_client = boto3.client('lambda')
  intermediates = ["m_" + str(x) for x in range(0,7)]
    for intermediate in intermediates:
      lambda_client.invoke(
        FunctionName="mmultiply-prod-strassen",
            InvocationType='Event',
            LogType='Tail',
            Payload=json.dumps({
                "op": "intermediate",
                "intermediate": intermediate,
                "matrix-X": event['matrix-X'],
                "matrix-Y": event['matrix-Y'],
                "result-bucket": event['result-bucket']
            })
        )


'''
{
  "matrix-X": "matrix-X",
  "matrix-Y": "matrix-Y",
  "result-bucket": "result-bucket",
  "intermediate": "m_0"
}
'''
def intermediate(event, context):
  intermediate_method = globals()[event['intermediate']]
  matX = load_matrix(event['matrix-X'])
  matY = load_matrix(event['matrix-Y'])
  result = intermediate_method(matX, matY)
  # print result
  write_to_s3(result, event['result-bucket'], event['intermediate'])

'''
{
  "result-bucket": "result-bucket",
  "result-name": "result-name"
}
'''
def collect(event, context):
  Q00 = q_0_0()
  Q01 = q_0_1()
  Q10 = q_1_0()
  Q11 = q_1_1()

  S = np.array([np.append(Q00[0], Q01[0]),
                np.append(Q00[1], Q01[1]),
                np.append(Q10[0], Q11[0]),
                np.append(Q10[1], Q11[1])])

  write_to_s3(S, event['result-bucket'], event['result-name'])

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

def q_0_0():
  m_0 = load_matrix('m_0')
  m_3 = load_matrix('m_3')
  m_4 = load_matrix('m_4')
  m_6 = load_matrix('m_6')
  return m_0 + m_3 - m_4 + m_6

def q_0_1():
  m_2 = load_matrix('m_2')
  m_4 = load_matrix('m_4')
  return m_2 + m_4

def q_1_0():
  m_1 = load_matrix('m_1')
  m_3 = load_matrix('m_3')
  return m_1 + m_3

def q_1_1():
  m_0 = load_matrix('m_0')
  m_2 = load_matrix('m_2')
  m_1 = load_matrix('m_1')
  m_5 = load_matrix('m_5')
  return m_0 + m_2 - m_1 + m_5

# HELPERS

def load_matrix(matrix):
  if matrix == 'dummy':
    return np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
  else:
    # TODO: use download_fileobj so no file has to be written
    s3_client.download_file('jmue-matrix-tests', matrix, '/tmp/' + matrix)
    return np.load('/tmp/' + matrix)

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
