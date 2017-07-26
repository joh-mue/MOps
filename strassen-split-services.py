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
  "intermediate": "m_*"
}
'''
def intermediate(event, context):
  intermediate_method = globals()[event['intermediate']]
  result = intermediate_method(event['matA'], event['matB'])
  # print result
  write_to_s3(
    data=result,
    bucket=event['result']['bucket'],
    folder=event['result']['folder'],
    key=event['intermediate']
    )

# INTERMEDIATE METHODS

#  _ _  _ _ 
# |X00 |X01 |
# |_ _ |_ _ |
# |X10 |X11 |
# |_ _ |_ _ |
#

def m_0(X, Y):
  return (partition(X,0,0) + partition(X,1,1)).dot(partition(Y,0,0) + partition(Y,1,1))

def m_1(X, Y):
  return (partition(X,1,0) + partition(X,1,1)).dot(partition(Y,0,0))

def m_2(X, Y):
  return partition(X,0,0).dot(partition(Y,0,1) - partition(Y,1,1))

def m_3(X, Y):
  return partition(X,1,1).dot(partition(Y,1,0) - partition(Y,0,0))

def m_4(X, Y):
  return (partition(X,0,0) + partition(X,0,1)).dot(partition(Y,1,1))

def m_5(X, Y):
  return (partition(X,1,0) - partition(X,0,0)).dot(partition(Y,0,0) + partition(Y,0,1))

def m_6(X, Y):
  return (partition(X,0,1) - partition(X,1,1)).dot(partition(Y,1,0) + partition(Y,1,1))


def partition(matrix, x, y):
  print("Loading partition " + matrix['folder'] + "_" + str(x) + "_" + str(y))
  split = matrix['split']
  x += split['x1']/1000
  y += split['y1']/1000
  partition_factor = ((split['x2']-split['x1'])/2)/1000 # length of split us twice the size of a partition

  filename = "m_" + str(partition_factor*x) + "_" + str(partition_factor*y) + ".npy"
  key = matrix['folder'] + "/" + filename # e.g. m_0_0.npy

  if not os.path.exists('/tmp/' + matrix['folder']):
    os.mkdir('/tmp/' + matrix['folder'])
  
  s3_client.download_file(matrix['bucket'], key, '/tmp/' + key)
  return np.load('/tmp/' + key)


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
  Q00 = q_0_0(event['result']['bucket'])
  Q01 = q_0_1(event['result']['bucket'])
  Q10 = q_1_0(event['result']['bucket'])
  Q11 = q_1_1(event['result']['bucket'])

  top = np.concatenate((Q00, Q01), axis=1)
  bottom = np.concatenate((Q10,Q11), axis=1)
  S = np.concatenate((top, bottom), axis=0)

  write_to_s3(S, event['result']['bucket'], event['result']['folder'])

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

def write_to_s3(data, bucket, folder, key):
  if not os.path.exists('/tmp/' + folder):
    os.mkdir('/tmp/' + folder)
  
  tmp_filepath = '/tmp/' + folder + "/" + key + ".npy"
  with open(tmp_filepath, 'wb') as tmp_file:
    np.save(tmp_filepath, data)

  s3_client.upload_file(tmp_filepath, bucket, folder + "/" + key)
