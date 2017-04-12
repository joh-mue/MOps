'''
setup test matrixes

{
  "matrix-size": 100,
  "bucket": "jmue-matrixes",
  "key": "matrix-C"
}

'''

import boto3
import json
import pickle

s3_client = boto3.client('s3')

def handler(event, context):
  bucket = event['bucket']
  matrix_size = event['matrix-size']
  key = event['key'] + "-" + str(matrix_size)

  test_matrix = []
  
  for i in range(matrix_size):
    row = [x for x in range(1, matrix_size + 1)] # from 1,....,matrix_size
    test_matrix.append(row)

  write_to_s3(test_matrix, bucket, key)

  response = {
    "number-of-rows": len(test_matrix),
    "number-of-columns": len(test_matrix[0]),
    "key": key
  }

  return response

def write_to_s3(data, bucket, key):
  with open("/tmp/" + key, "wb") as file:
    pickle.dump(data, file)
  s3_client.upload_file("/tmp/" + key, bucket, key)
