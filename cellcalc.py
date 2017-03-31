'''
Python Cell Calculator for Matrix Multiplication
'''
import boto3
import json

def handler(event, context):
  column = event['column']
  row = event['row']
  matrix_a = event['matrix_a']
  matrix_b = event['matrix_b']
  print "I got" + ", " + str(column) + ", " + str(row) + ", " + matrix_a + ", " + matrix_b

  matrix_data = load_matrices(matrix_a, matrix_b)
  result = multiply_matrices(matrix_data[0],matrix_data[1])

  response = {
    "cell": 0,
    "target": "/path"
  };

  return response

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

def calculate_cell(row,column, matrix_a, matrix_b):
  cell = 0
  for y in range(len(matrix_a[0])):
    cell += matrix_a[row][y] * matrix_b[y][column]
  return cell
