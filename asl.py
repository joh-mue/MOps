# asl helper module

def task_state(resource, next_state=None):
    task_state = {
            "Type": "Task",
            "Resource": resource,
            "End": True
    }
    if next_state is not None:
        task_state["End"] = False
        task_state["Next"] = next_state
    return task_state

def pass_state(next_state, result=None, resultPath=None, outputPath=None):
    return {
              "Type": "Pass",
              "Result": result,
              "ResultPath": resultPath,
              "OutputPath": outputPath,
              "Next": next_state
    }

def parallel_state(branches, next_state, resultPath=None, outputPath=None):
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

def branch(startAt, states):
    return {
        "StartAt": startAt,
        "States": states
    }

def create_strassen_sfn(unit=""):
    branches = []
    for index in range(0,7):
        unit_m = "U{}_m{}".format(unit, index) # U0_m_0
        unit_m_lambda = "U{}_m{}_lambda".format(unit, index) # U0_m_0_lambda
        states = {
            unit_m: pass_state(next_state=unit_m_lambda, result=index, resultPath="$.intermediate", outputPath="$"),
            unit_m_lambda: task_state(resource="arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate")
        }
        branches.append(branch(states=states, startAt=unit_m))

    unit_name = "unit" + unit
    i_name = "U{}_Intermediate".format(unit)
    c_name = "U{}_Collect".format(unit)
    
    unit_setup = pass_state(next_state=i_name, result=unit, resultPath="$.unit", outputPath="$")
    intermediates = parallel_state(branches=branches, next_state=c_name, resultPath="$.responses", outputPath="$")
    collect = task_state(resource="arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-collector")
        
    states = { unit_name: unit_setup, i_name: intermediates, c_name: collect }
    return branch(startAt=unit_name, states=states)
