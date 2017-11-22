import boto3
import json
import aws
import time

from collections import namedtuple

### NUMPY, SCIPY, SKLEARN MAGIC
import os
import ctypes

import platform
if platform.system() != 'Darwin': # don't do this on my local machine
    for d, _, files in os.walk('lib'):
        for f in files:
            if f.endswith('.a'):
                  continue
            ctypes.cdll.LoadLibrary(os.path.join(d, f))

import numpy as np
### NUMPY, SCIPY, SKLEARN MAGIC END

def handler(event, context):
  columns = event['columns']
  rows = event['rows']

  generation_start_time = time.time()
  matA = np.random.random_sample((columns, rows))
  matB = np.random.random_sample((columns, rows))
  generation_time = time.time() - generation_start_time

  calc_start_time = time.time()
  matA.dot(matB)
  calc_time = time.time() - calc_start_time

  event["generating matrices"] = int(generation_time * 1000)
  event["calculation"] = int(calc_time * 1000)
  return event

