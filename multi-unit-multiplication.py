import boto3
import json

import os

import asl

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
    ssl = event['splitSizeLimit']
    # divide work into portions
    matA_splits = (event['matA']['rows']/ssl, event['matA']['columns']/ssl) # (2, 2) -> (m, n) 
    matB_splits = (event['matB']['rows']/ssl, event['matB']['columns']/ssl) # (2, 2) -> (n, p)
    # TODO: always round up! padding zeroes will be added
    m, n, p = matA_splits[0], matA_splits[1], matB_splits[1]
    matC_splits = (m, p)

    # create multi-unit-stepfunction asl code
    state_machine = asl.create_multi_unit_stepfunction(nr_of_units=n)
    # deploy asl
    stateMachineArn = deploy_statemachine(state_machine)

    # start m*p many split calculation stepfunction-executions with n units each
    for i in range(m):
        for j in range(n):
            for k in range(p):
                print "A{}{}*B{}{}+".format(i,j,j,k),
                start_execution(i,k,j, event, stateMachineArn)
            print ""


def deploy_statemachine(asl):
    # arn = 'arn:aws:iam::146904559692:role/StepFunctionRole'
    arn = "arn:aws:iam::146904559692:role/mmultiply-prod-eu-central-1-lambdaRole"
    sfn_client = boto3.client('stepfunctions')
    response = sfn_client.create_state_machine(name="dual-unit-mmultiply", definition=asl, roleArn=arn)
    return response['stateMachineArn']

def start_execution(i, j, k, event, stateMachineArn):
    ssl = event['splitSizeLimit']
    sfn_input = event
    sfn_input['matA']['split'] = { "x1": i*ssl, "y1": k*ssl, "x2": (i+1)*ssl, "y2": (k+1)*ssl }
    sfn_input['matB']['split'] = { "x1": k*ssl, "y1": j*ssl, "x2": (k+1)*ssl, "y2": (j+1)*ssl }
    sfn_input['result']['split'] = { "x1": i*ssl, "y1": k*ssl, "x2": (k+1)*ssl, "y2": (j+1)*ssl }
    print("i:{}, j:{}, k:{}".format(i,j,k))
    sfn_input['split'] = i + i * k
    response = sfn_client.start_execution(
            stateMachineArn=stateMachineArn,
            name="{}-split{}-partial-{}".format(event['executionName'], i + i*k, j),
            input=json.dumps(sfn_input)
    )
    print response['executionArn']
