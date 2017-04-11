'''
Python Cell Calculator for Matrix Multiplication
'''
import boto3
import json
import pickle

s3_client = boto3.client('s3')

def handler(event, context):
  matrix_a = event['matrix_a']
  matrix_b = event['matrix_b']
  column = event['column'] - 1
  row = event['row'] - 1
  print "I got" + ", " + str(column) + ", " + str(row) + ", " + matrix_a + ", " + matrix_b

  matrix_a_data = load_matrix(matrix_a)
  matrix_b_data = load_matrix(matrix_b)
  
  cell = calculate_cell(row, column, matrix_a_data, matrix_b_data)
  print cell
  
  bucket = event['target']
  key = "C_" + str(column) + "-" + str(row)
  write_to_s3(bucket, key, cell)

  response = {
    "cell": cell,
    "target": bucket
  }

  return response

def load_matrix(matrix):
  bucketName = 'jmue-matrixes'
  s3_client.download_file(bucketName, matrix, '/tmp/' + matrix)

  with open('/tmp/' + matrix, "rb") as file:
    matrix_data = pickle.load(file)
  return matrix_data

def calculate_cell(row,column, matrix_a, matrix_b):
  cell = 0
  for y in range(len(matrix_a[0])):
    cell += matrix_a[row][y] * matrix_b[y][column]
  return cell

def write_to_s3(bucket, key, result):
  with open("/tmp/cell.data", 'wb') as file:
    pickle.dump(result, file)
  s3_client.upload_file('/tmp/cell.data', 'jmue-matrixes', key)


'''
event
{
  matrix_a: "matrix_A001",
  matrib_b: "matrix_B001",
  row: 1, use matrix notation
  column: 1, use matrix notation
  target: "jmue-matrixes"
}
'''
