'''
Serverless Python Matrix Multiplication
'''
import boto3
import json

lambda_client = boto3.client('lambda')

def handler(event, context):
  matrix_a = 
  matrix_b = 

  load_matrices(matrix_a, matrix_b)

  for row in range(len(matrix_a)):  
    for column in range(len(matrix_a[0])):
      # calculate cell
      cell = calculate_cell(row,column, matrix_a, matrix_b)
      # invoke the reducers asynchronously
      resp = lambda_client.invoke( 
              FunctionName = r_function_name,
              InvocationType = 'Event',
              Payload =  json.dumps({
                  "bucket": bucket,
                  "keys": batch,
                  "jobBucket": bucket,
                  "jobId": job_id,
                  "nReducers": n_reducers, 
                  "stepId": step_id, 
                  "reducerId": i 
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
