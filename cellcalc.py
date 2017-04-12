'''
Python Cell Calculator for Matrix Multiplication

{
  "matrix-a-key": "matrix_A001",
  "matrix-b-key": "matrix_B001",
  "matrix-c-key": "matrix_C001",
  "row": 1, use matrix notation
  "column": 1, use matrix notation
  "bucket": "jmue-matrix-tests"
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

  print event
  
  # column and row are given in Matrixnotation, not array notation
  row = event['row']
  column = event['column']
  
  matrix_a = load_from_s3(bucket, matrix_a_key)
  matrix_b = load_from_s3(bucket, matrix_b_key)
  
  cell_value = calculate_cell(row, column, matrix_a, matrix_b)
  
  bucket = event['bucket']
  cell_key = matrix_c_key + "-" + str(row) + "-" + str(column)
  write_to_s3(cell_value, bucket, cell_key)

  return { "cell-value": cell_value, "cell-key": cell_key, "bucket": bucket }


def load_from_s3(bucket, matrix_key):
  tmp_filepath = '/tmp/' + matrix_key
  s3_client.download_file(bucket, matrix_key, tmp_filepath)
  with open(tmp_filepath, "rb") as tmp_file:
    matrix_data = pickle.load(tmp_file)
  return matrix_data


def calculate_cell(row, column, matrix_a, matrix_b):
  cell = 0
  row = row - 1 # translate to matrix notation
  column = column - 1 # translate to matrix notation
  for y in range(len(matrix_a[0])):
    cell += matrix_a[row][y] * matrix_b[y][column]
  return cell


def write_to_s3(data, bucket, key):
  tmp_filepath = "/tmp/" + key
  with open(tmp_filepath, 'wb') as tmp_file:
    pickle.dump(data, tmp_file)
  s3_client.upload_file(tmp_filepath, bucket, key)
