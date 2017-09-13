from collections import namedtuple
from collections import defaultdict
from datetime import datetime
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import os
import boto3
import json
import base64
import csv

import pdb


########################
###   NAMED TUPLES   ###
########################
MatrixDimensions = namedtuple('MatrixDimensions', ['height', 'width'])
Timings = namedtuple('Timings', ['down','up','calculation'])


########################
###     CLIENTS      ###
########################
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')
sfn_client = boto3.client('stepfunctions')


########################
###     METHODS      ###
########################

def _log(message):
    timestamp = datetime.now().strftime('%d.%m.%y %H:%M:%S > ')
    print timestamp + message


def write_block_to_file(block, directory, row, column):
    if not os.path.exists(directory):
        os.mkdir(directory)
    path = os.path.join(directory, 'm_' + str(row) + '_' + str(column))
    _log('Writing block to file: {}'.format(path))
    np.save(path, block)

def get_block_with_random(height, width):
    return np.random.random_sample((height,width))

def create_blocks_with_random(x, y, block_height, block_width, matrix_name):
    for i in range(0,x):
        for j in range(0,y):
            block = get_block_with_random(block_height, block_width)
            directory = '/tmp/' + matrix_name
            write_block_to_file(block, directory, i, j)

def create_matrices(matrix_dimensions, matrix_name):
    x = matrix_dimensions.height/BLOCK_SIZE
    y = matrix_dimensions.width/BLOCK_SIZE
    _log('Creating matrix: {}'.format(matrix_name))
    create_blocks_with_random(x, y, BLOCK_SIZE, BLOCK_SIZE, matrix_name)
    _log('Creating matrix: {}'.format(matrix_name + '-2'))
    create_blocks_with_random(x, y, BLOCK_SIZE, BLOCK_SIZE, matrix_name + '-2')



def upload_blocks(matrix_name, bucket, s3_matrix_name=None):
    localpath = '/tmp/' + matrix_name
    filenames = os.listdir(localpath)

    s3_folder = matrix_name
    if s3_matrix_name is not None:
        s3_folder = s3_matrix_name
    
    for filename in filenames:
        _log('Uploading to s3: {}'.format(filename))
        s3_client.upload_file(
            Filename=os.path.join(localpath,filename),
            Bucket=bucket,
            Key=os.path.join(s3_folder,filename)
        )

def deploy_matrices(matrix_name):
    _log('Uploading matrix to s3: {}'.format(matrix_name))
    upload_blocks(matrix_name, BUCKET)
    _log('Uploading matrix to s3: {}'.format(matrix_name + '-2'))
    upload_blocks(matrix_name, BUCKET, s3_matrix_name=matrix_name + '-2')



def create_input(state_machine_name, executionName, name_matrixA, name_matrixB):
    input = {
            'state-machine-name': state_machine_name,
            'executionName': executionName,
            'matA': {
            'bucket': BUCKET,
            'folder': name_matrixA,
            'rows': matrix_dimensions.height,
            'columns': matrix_dimensions.width
            },
            'matB': {
              'bucket': BUCKET,
              'folder': name_matrixB,
              'rows': matrix_dimensions.height,
              'columns': matrix_dimensions.height
            },
            'result': {
              'bucket': BUCKET,
              'folder': matrix_name + '-result'
            },
            'split-size': BLOCK_SIZE * 2
        }
    return input

def invoke_matrix_multiplication(state_machine_name, executionName, name_matrixA, name_matrixB):
    """ execution_info.keys() :> ['deploy-nr', 'split-executions', 'split'] """
    sfn_input = create_input(state_machine_name, executionName, name_matrixA, name_matrixB)
    _log("Invoking matrix multiplication with input: {}".format(sfn_input))
    response = lambda_client.invoke(

        FunctionName='mmultiply-prod-multi-unit-multiplication',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps(sfn_input)
    )
    _log('LogResult: \n{}'.format(base64.b64decode(response['LogResult'])))
    return json.loads(response['Payload'].read())



def executions_pending(executionARNs):
    """ Checks if all executions have either succeeded or failed yet.
    Failed executions are skipped. """
    for executionARN in executionARNs:
        last_event = sfn_client.get_execution_history(
            executionArn=executionARN,
            maxResults=1,
            reverseOrder=True
        )['events'][0]

        if last_event['type'] == 'ExecutionFailed':
            _log('Execution {} failed.'.format(executionARN))
            pass
        elif last_event['type'] != 'ExecutionSucceeded':
            return True # Executions still pending
    _log('All executions finished(failed/succeeded).')
    return False



def extract_time_profiles(events):
    """ Time profiles are part of the lambda output which is returned as a json formated string """
    _log("Extracting time profiles")
    lambda_outputs = [x['lambdaFunctionSucceededEventDetails']['output'] for x in events if x['type'] == 'LambdaFunctionSucceeded']
    time_profiles = [json.loads(x)['time-profile'] for x in lambda_outputs]

    time_profiles_by_lambda = defaultdict(list)
    for profile in time_profiles:
        time_profiles_by_lambda[profile['lambda']].append(profile)

    return time_profiles_by_lambda

def get_all_events(executionARNs):
    events = []
    for executionARN in executionARNs:
        _log('Retrieving execution history for {}'.format(executionARN))
        response = sfn_client.get_execution_history(executionArn=executionARN)
        events.extend(response['events'])

        while response.has_key('nextToken'):
            _log('Loading further events')
            response = sfn_client.get_execution_history(
                executionArn=executionARN,
                nextToken=response['nextToken']
            )
            events.extend(response['events'])

    return events

def parse_time_profiles(executionARNs):
    events = get_all_events(executionARNs)
    time_profiles_by_lambda = extract_time_profiles(events)
    return time_profiles_by_lambda



def plot_timing_profile(timings, lambda_type, state_machine_name, folder):
    # e.g. './block_size_1000/sq_2kx2k_intermediate.png'
    plot_path = '{}/{}_{}.png'.format(folder, state_machine_name, lambda_type)
    _log('Creating plot {}'.format(plot_path))
    
    N = len(timings.down)
    index = np.arange(N)    # the x locations for the groups
    width = 0.5           # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    p1 = plt.bar(index, timings.down, width, color='b')
    p2 = plt.bar(index, timings.up, width, color='c', bottom=timings.down)
    p3 = plt.bar(index, timings.calculation, width, color='m', bottom=np.add(timings.down,timings.up))

    # ax.set_ybound() # take the max value of execution plus 100
    # ax.set_xbound() # number of intermediate lambdas?

    ax.set_ylabel('time in ms')
    ax.set_xlabel('execution index, 0 is averages across executions')
    ax.set_title('Timing profiles for {}-lambda executions.'.format(lambda_type))
    ax.legend((p3, p2, p1), ('Calculation', 'S3 upload','S3 download'), loc=4)

    plt.savefig(os.path.join(BENCHMARKS_FOLDER, plot_path), dpi=500)
    # plt.show()

def collect_values(time_profiles_by_lambda, add_average=True):
    """collect values into arrays and return them as a timings tuple"""
    s3_down ,s3_up ,calcs = [], [] ,[]
    for item in time_profiles_by_lambda:
        s3_down.append(item['s3-down'])
        s3_up.append(item['s3-up'])
        calcs.append(item['execution']-item['s3-down']-item['s3-up'])
    
    if add_average:
        # add the average as the first value
        s3_down = np.append(np.average(s3_down), s3_down)
        s3_up = np.append(np.average(s3_up), s3_up)
        calcs = np.append(np.average(calcs), calcs)
      
    return Timings(s3_down, s3_up, calcs)

def plot_time_profiles(time_profiles_by_lambda, state_machine_name, folder):
    _log("Plotting time profiles for {}".format(state_machine_name))

    for lambda_type in time_profiles_by_lambda.keys():
        timings = collect_values(time_profiles_by_lambda[lambda_type], add_average=True)
        plot_timing_profile(timings, lambda_type, state_machine_name, folder)



def save_raw_data(time_profiles_by_lambda, csv_path):
    _log("Writing time profiles to file: {}".format(csv_path))
    with open(csv_path, 'wb') as file:
        writer =  csv.writer(file, delimiter=',')
        writer.writerow(['type','down','up','execution'])
        for lambda_type in time_profiles_by_lambda.keys():
            timings = time_profiles_by_lambda[lambda_type]
            for t in timings:
                writer.writerow([lambda_type, t['s3-down'], t['s3-up'], t['execution']])


def compare_time_profiles():
    pass




########################
### GLOBAL CONSTANTS ###
########################

BLOCK_SIZE = 1000
BUCKET = 'jmue-multiplication-benchmarks'
PREFIX = 'sq'
BENCHMARKS_FOLDER = '/Users/Johannes/Uni/Master/Master Arbeit/repos/matrix-operations/benchmarks/'
SFN_PREFIX = 'dual-impr-timing-benchmark'

########################
###   Main Programm  ###
########################

_log('benchmark parameters:\n  BLOCK_SIZE:{}\n  BUCKET:{}\n  PREFIX:{}\n  BENCHMARKS_FOLDER:{}\n  SFN_PREFIX'.format(
    BLOCK_SIZE, BUCKET, PREFIX, BENCHMARKS_FOLDER, SFN_PREFIX))

matrix_dimension_sets = [
        MatrixDimensions(height=2000, width=2000),
        # MatrixDimensions(height=3000, width=3000),
        MatrixDimensions(height=4000, width=4000)
        # MatrixDimensions(height=5000, width=5000)
]

_log(str(matrix_dimension_sets))

for matrix_dimensions in matrix_dimension_sets:
    matrix_name = '{}_{}kx{}k'.format(PREFIX, matrix_dimensions.height/1000, matrix_dimensions.width/1000)
    _log('Benchmarking {}'.format(matrix_name))

    # create_matrices(matrix_dimensions, matrix_name)
    # deploy_matrices(matrix_name)

    state_machine_name = '{}-{}kx{}k'.format(SFN_PREFIX, matrix_dimensions.height/1000, matrix_dimensions.width/1000)
    execution_info = invoke_matrix_multiplication(
            state_machine_name=state_machine_name,
            executionName=state_machine_name,
            name_matrixA=matrix_name,
            name_matrixB=matrix_name + '-2'
    )
    split_executionARNs = [x['executionARN'] for x in execution_info['split-executions']]
    _log("Waiting for pending executions to finish...")
    while executions_pending(split_executionARNs):
        sleep(2)
    
    folder = os.path.join(BENCHMARKS_FOLDER,'block_size_{}'.format(BLOCK_SIZE), SFN_PREFIX)
    if not os.path.exists(folder):
        os.mkdir(folder)

    time_profiles_by_lambda = parse_time_profiles(split_executionARNs)
    save_raw_data(time_profiles_by_lambda, csv_path=os.path.join(folder, state_machine_name + '.csv'))
    plot_time_profiles(time_profiles_by_lambda, state_machine_name, folder)

# compare_time_profiles()
