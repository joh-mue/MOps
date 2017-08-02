import boto3
import json
import pickle
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
  key = "S{}_U{}_{}".format(event['split'], event['unit'], event['intermediate'])
  aws.write_to_s3(
    data=result,
    bucket=event['result']['bucket'],
    folder=event['result']['folder'],
    key=key,
    s3_client=s3_client
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
  print("Loading partition {}_{}_{}".format(matrix['folder'], x, y))
  split = matrix['split']
  x += split['x1']/1000
  y += split['y1']/1000
  partition_factor = ((split['x2']-split['x1'])/2)/1000 # length of split us twice the size of a partition

  filename = "m_{}_{}.npy".format(partition_factor*x, partition_factor*y)
  path = aws.download_s3_file(matrix['bucket'], matrix['folder'], filename, s3_client)
  return np.load(path)


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
  result = event['result']
  Q00 = q_0_0(result['bucket'], result['folder'], event['split'], event['unit'])
  Q01 = q_0_1(result['bucket'], result['folder'], event['split'], event['unit'])
  Q10 = q_1_0(result['bucket'], result['folder'], event['split'], event['unit'])
  Q11 = q_1_1(result['bucket'], result['folder'], event['split'], event['unit'])

  prefix = "S{}_U{}_".format(event['split'], event['unit'])
  aws.write_to_s3(Q00, result['bucket'], result['folder'], prefix + "X00", s3_client)
  aws.write_to_s3(Q01, result['bucket'], result['folder'], prefix + "X01", s3_client)
  aws.write_to_s3(Q10, result['bucket'], result['folder'], prefix + "X10", s3_client)
  aws.write_to_s3(Q11, result['bucket'], result['folder'], prefix + "X11", s3_client)

# COLLECTOR

def q_0_0(bucket, folder, split, unit):
  m_0 = load_interm_result(bucket, folder, split, unit, 'm_0')
  m_3 = load_interm_result(bucket, folder, split, unit, 'm_3')
  m_4 = load_interm_result(bucket, folder, split, unit, 'm_4')
  m_6 = load_interm_result(bucket, folder, split, unit, 'm_6')
  return m_0 + m_3 - m_4 + m_6

def q_0_1(bucket, folder, split, unit):
  m_2 = load_interm_result(bucket, folder, split, unit, 'm_2')
  m_4 = load_interm_result(bucket, folder, split, unit, 'm_4')
  return m_2 + m_4

def q_1_0(bucket, folder, split, unit):
  m_1 = load_interm_result(bucket, folder, split, unit, 'm_1')
  m_3 = load_interm_result(bucket, folder, split, unit, 'm_3')
  return m_1 + m_3

def q_1_1(bucket, folder, split, unit):
  m_0 = load_interm_result(bucket, folder, split, unit, 'm_0')
  m_2 = load_interm_result(bucket, folder, split, unit, 'm_2')
  m_1 = load_interm_result(bucket, folder, split, unit, 'm_1')
  m_5 = load_interm_result(bucket, folder, split, unit, 'm_5')
  return m_0 + m_2 - m_1 + m_5

def load_interm_result(bucket, folder, split, unit, m_x):
  filename = "S{}_U{}_{}.npy".format(split, unit, m_x)
  
  path = aws.download_s3_file(bucket, folder, filename, s3_client)
  return np.load(path)


# HELPERS

# def write_to_s3(data, bucket, folder, key):
#   if not os.path.exists('/tmp/' + folder):
#     os.mkdir('/tmp/' + folder)
  
#   tmp_filepath = "/tmp/{}/{}.npy".format(folder, key)
#   with open(tmp_filepath, 'wb') as tmp_file:
#     np.save(tmp_filepath, data)

#   s3_client.upload_file(tmp_filepath, bucket, folder + "/" + key)
