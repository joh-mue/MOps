'''
Serverless Python Matrix Multiplication

{
  
}

'''
import boto3
import json

lambda_client = boto3.client('lambda')

def handler(event, context):
  matrix_a = event['matrix-a']
  matrix_b = event['matrix-b']

  load_matrices(matrix_a, matrix_b)

  for row in range(len(matrix_a)):
    for column in range(len(matrix_a[0])):
      # calculate cell
      cell = calculate_cell(row,column, matrix_a, matrix_b)
      # invoke the reducers asynchronously
      response = lambda_client.invoke(
                FunctionName="mmultiply-prod-cellcalc",
                InvocationType='RequestResponse',
                LogType='Tail',
                Payload=json.dumps({
                    "column": 4,
                    "row": 4,
                    "matrix_a": "test-matrix-C-100",
                    "matrix_b": "test-matrix-C-100",
                    "target": "jmue-matrixes"
                })
            )
      print resp
      print "[",cell,"]",
    print ""
  return []

def load_matrices(matrix_a, matrix_b):
  matrix_a_data = [[1,2,3],[4,5,6],[7,8,9]]
  matrix_b_data = [[1,2,3],[4,5,6],[7,8,9]]
  return matrix_a_data, matrix_b_data

def multiply_matrices(matrix_a, matrix_b):
  for row in range(len(matrix_a)):  
    for column in range(len(matrix_a[0])):
      cell = calculate_cell(row,column, matrix_a, matrix_b)
      print "[",cell,"]",
    print ""
  return []
