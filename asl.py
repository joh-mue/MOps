# asl helper module

import boto3
import json

INTERMEDIATE_ARN = "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate"
COLLECTOR_ARN = "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-collector"
ACCUMULATOR_ARN = "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-unit-accumulator"

def _task_state(resource, next_state=None):
    task_state = {
            "Type": "Task",
            "Resource": resource,
            "End": True
    }
    if next_state is not None:
        task_state["End"] = False
        task_state["Next"] = next_state
    return task_state

def _pass_state(next_state, result=None, resultPath=None, outputPath=None):
    return {
            "Type": "Pass",
            "Result": result,
            "ResultPath": resultPath,
            "OutputPath": outputPath,
            "Next": next_state
    }

def _parallel_state(branches, next_state, resultPath=None, outputPath=None):
    parallel_state = {
            "Type": "Parallel",
            "Next": next_state,
            "Branches": branches
    }
    if resultPath is not None:
        parallel_state["ResultPath"] = resultPath
    
    if outputPath is not None:
        parallel_state["OutputPath"] = outputPath
    
    return parallel_state

def _branch(startAt, states):
    return {
            "StartAt": startAt,
            "States": states
    }

def _create_strassen_sfn(unit):
    branches = []
    for index in range(0,7):
        unit_m = "U{}_m{}".format(unit, index) # U0_m_0
        unit_m_lambda = "U{}_m{}_lambda".format(unit, index) # U0_m_0_lambda
        states = {
            unit_m: _pass_state(next_state=unit_m_lambda, result=index, resultPath="$.intermediate", outputPath="$"),
            unit_m_lambda: _task_state(resource=INTERMEDIATE_ARN)
        }
        branches.append(_branch(states=states, startAt=unit_m))

    unit_name = "unit" + str(unit)
    i_name = "U{}_Intermediate".format(unit)
    c_name = "U{}_Collect".format(unit)
    
    unit_setup = _pass_state(next_state=i_name, result=unit, resultPath="$.unit", outputPath="$")
    intermediates = _parallel_state(branches=branches, next_state=c_name, resultPath="$.responses", outputPath="$")
    collect = _task_state(resource=COLLECTOR_ARN)
        
    states = { unit_name: unit_setup, i_name: intermediates, c_name: collect }
    return _branch(startAt=unit_name, states=states)

def create_multi_unit_stepfunction(nr_of_units):
    unit_branches = []
    for i in range(0, nr_of_units):
        unit_branches.append(_create_strassen_sfn(unit=i))

    states = {
            "Accumulate": _task_state(resource=ACCUMULATOR_ARN),
            "Units": _parallel_state(branches=unit_branches, next_state="Accumulate", resultPath="$.responses", outputPath="$")
    }
    asl = _branch(startAt="Units", states=states)
    return json.dumps(asl)
