'''
{
  "bucket": "bucket-name",
  "matrix-a-key": "matrix-a-key",
  "matrix-b-key": "matrix-b-key",
  "matrix-c-key": "matrix-c-key"
}
'''

import boto3
import json
import pickle

s3_client = boto3.client('s3')

def handler(event, context):
  bucket = event['bucket']
  matrix_a_key = event['matrix-a-key']
  matrix_b_key = event['matrix-b-key']
  matrix_c_key = event['matrix-c-key']

  matrix_a = load_matrix(bucket, matrix_a_key)
  matrix_b = load_matrix(bucket, matrix_b_key)
  matrix_c = multiply(matrix_a, matrix_b)

  write_to_s3(matrix_c, bucket, matrix_c_key)

  return { "status": "done", "result-bucket": bucket, "result-key": matrix_c_key }

def load_matrix(bucket, matrix_key):
  tmp_filename = '/tmp/' + matrix_key
  s3_client.download_file(bucket, matrix_key, tmp_filename)
  with open (tmp_filename, 'rb') as tmp_file:
    matrix_data = pickle.load(tmp_file)
  return matrix_data


def multiply(matrix_a, matrix_b):
  result_size = len(matrix_a)
  matrix_c = []

  for row in range(result_size):
    row_values = []
    for column in range(result_size):
      cell = calculate_cell(row, column, matrix_a, matrix_b)
      row_values.append(cell)
    matrix_c.append(row_values)
  return matrix_c

def calculate_cell(row, column, matrix_a, matrix_b):
  cell = 0
  for y in range(len(matrix_a[0])):
    cell += matrix_a[row][y] * matrix_b[y][column]
  return cell


def write_to_s3(matrix, bucket, key):
  tmp_filename = '/tmp/' + key
  with open(tmp_filename, "wb") as tmp_file:
    pickle.dump(result, file)
  s3_client.upload_file(tmp_filename, bucket, key)
