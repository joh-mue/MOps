'''
{
  "bucket": "bucket-name",
  "matrix-a-key": "matrix-a-key",
  "matrix-b-key": "matrix-b-key",
  "matrix-c-key": "matrix-c-key",
  "matrix-a-size": matrix-a-size,
  "matrix-b-size": matrix-b-size
}
'''

import boto3
import json
import pickle

lambda_client = boto3.client('lambda')

def handler(event, context):
  bucket = event['bucket']
  matrix_a_key = event['matrix-a-key']
  matrix_b_key = event['matrix-b-key']
  matrix_c_key = event['matrix-c-key']
  matrix_a_size = event['matrix-a-size']

  result_size = matrix_a_size
  for row in range(result_size):
    for column in range(result_size):
      calculate_cell(row, column, matrix_a_key, matrix_b_key, matrix_c_key, bucket)

def calculate_cell(row, column, matrix_a_key, matrix_b_key, matrix_c_key, bucket):
  response = lambda_client.invoke(
      FunctionName="mmultiply-prod-cellcalc",
      InvocationType='Event',
      Payload=json.dumps({
          "matrix-a-key": matrix_a_key,
          "matrix-b-key": matrix_b_key,
          "matrix-c-key": matrix_c_key,
          "row": row,
          "column": column,
          "bucket": bucket
      })
  )
