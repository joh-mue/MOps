import boto3
import json
import os

import asl

deploy_nr = 'MUM101'

sfn_client = boto3.client('stepfunctions')

'''
{
    "state_machine_name": "multiplication-name",
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
    "split_size": 2000
}
'''

def handler(event, context):
    split_size = event['split-size']

    # analyze operations
    # TODO: always round up! padding zeroes will be added
    m = event['matA']['rows'] / split_size
    n = event['matA']['columns'] / split_size # = event['matB']['rows']
    p = event['matB']['columns'] / split_size

    # create and deploy multi-unit-stepfunction asl code
    state_machine = asl.create_multi_unit_stepfunction(nr_of_units=n)
    state_machine_Arn = deploy_state_machine(state_machine, event['state-machine-name'])

    # start m*p many split calculation stepfunction-executions with n units each
    executions = []
    for i in range(m):
        for k in range(p):
            print "Split_{} (x:{} y:{})".format(i*p+k, i, k),
            executionARN = start_execution(i,k,p, event, state_machine_Arn)           
            executions.append({'split': i*p+k, 'executionARN': executionARN })
        print ""

    return { 'split-executions': executions, 'state-machine-arn': state_machine_Arn, 'deploy-nr': deploy_nr }

def deploy_state_machine(asl, state_machine_name):
    # arn = 'arn:aws:iam::146904559692:role/StepFunctionRole'
    arn = 'arn:aws:iam::146904559692:role/mmultiply-prod-eu-central-1-lambdaRole'
    sfn_client = boto3.client('stepfunctions')
    response = sfn_client.create_state_machine(name=state_machine_name, definition=asl, roleArn=arn)
    return response['stateMachineArn']


def start_execution(i, k, p, event, state_machine_Arn):
    split_size = event['split-size']
    sfn_input = event
    sfn_input['result']['split'] = { 'x': i*split_size, 'y': k*split_size }
    split = i*p + k
    sfn_input['split'] = split
    response = sfn_client.start_execution(
            stateMachineArn=state_machine_Arn,
            name="{}-split{}".format(event['executionName'], split),
            input=json.dumps(sfn_input)
    )
    return response['executionArn']
