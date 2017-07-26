import boto3
import json

import os

sfn_client = boto3.client('stepfunctions')

'''
{
  "stateMachineArn": "state-machine-arn",
  "executionName": "execution-name",
  "matA": {
    "bucket": "jmue-matrix-tests",
    "key": "sc4000",
    "rows": 4000,
    "columns": 4000
  },
  "matB": {
      "bucket": "jmue-matrix-tests",
      "key": "sc4000t",
      "rows": 4000,
      "columns": 4000
  },
  "result": {
      "bucket": "jmue-matrix-tests",
      "key": "sc4000-result"
  },
  "splitSizeLimit": 2000
}
'''

def handler(event, context):
  # divide work into portions
  # matA_splits = (m, n) 
  # matB_splits = (n, p)
  matA_splits = (event['matA']['rows']/ssl, event['matA']['columns']/ssl) # (2, 2)
  matB_splits = (event['matB']['rows']/ssl, event['matB']['columns']/ssl) # (2, 2)
  # TODO: always round up! padding zeroes will be added

  m = matA_splits[0]
  n = matA_splits[1]
  p = matB_splits[1]

  matC_splits = (m,p)
  
  # start x many stepfunction executions
 for i in range(m):
    for j in range(n):
        for k in range(p):
          print "A" + str(i) + str(k) + "*" + "B" + str(k) + str(j), "+",
          start_execution(i,k,j,event)
        print ""

def start_execution(i, j, k, event):
  ssl = event['splitSizeLimit']
  sfn_input = event
  sfn_input['matA']['split'] = { "x1": i*ssl, "y1": k*ssl, "x2": (i+1)*ssl, "y2": (k+1)*ssl }
  sfn_input['matB']['split'] = { "x1": k*ssl, "y1": j*ssl, "x2": (k+1)*ssl, "y2": (j+1)*ssl }
  response = sfn_client.start_execution(
    stateMachineArn=event['stateMachineArn'],
    name=event['executionName'],
    input=sfn_input
  )
  print response['executionArn']
