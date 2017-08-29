import boto3
import json
import aws

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

  time = context.get_remaining_time_in_millis()
  matA = np.random.random_sample((columns, rows))
  matB = np.random.random_sample((columns, rows))
  time -= context.get_remaining_time_in_millis()

  event["generating matrices"] = time

  time = context.get_remaining_time_in_millis()
  matA.dot(matB)
  time -= context.get_remaining_time_in_millis()

  event["calculation"] = time
  event["remaining"] = context.get_remaining_time_in_millis()

  return event

