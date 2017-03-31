'''
Serverless Python Matrix Multiplication
'''
import boto3
import json

lambda_client = boto3.client('lambda')

def handler(event, context):
  for row in range(len(matrix_a)):  
    for column in range(len(matrix_a[0])):
      cell = calculate_cell(row,column, matrix_a, matrix_b)
      print "[",cell,"]",
    print ""
  return []
