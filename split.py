'''
Class that represents a split. Any split consists of 4 blocks which are stored as S3 objects.
Splits always belong to a matrix, identified by bucket and folder.

  _ _  _ _
 |X00 |X01 |
 |_ _ |_ _ |
 |X10 |X11 |
 |_ _ |_ _ |

'''

import aws
import numpy as np
import boto3
import time
import json

class Split(object):
    'Class that represents a matrix split'

    s3_client = boto3.client('s3')
    s3_download_time = 0
    def __init__(self, matrix, split, split_size):
        self.x = split['x']
        self.y = split['y']
        self.bucket = matrix['bucket']
        self.folder = matrix['folder']
        self.split_size = split_size
        self.block_size = matrix['block-size']

    def __str__(self):
        return json.dumps({
            'x': self.x,
            'y': self.y,
            'matrix': "{}/{}".format(self.bucket, self.folder),
            'split_size': self.split_size,
            'block_size': self.block_size
            })

    def block(self, x, y):
        '''
        Load block m_{x}_{y} from s3 and return it as numpy matrix, x and y can be
        0 or 1 and indicate relative position within the split. Absolute block index and filename
        are calculated and used to download from s3.
        '''
        block_x = (self.x + x * (self.block_size)) / self.block_size
        block_y = (self.y + y * (self.block_size)) / self.block_size
        filename = "m_{}_{}.npy".format(block_x, block_y)

        print filename

        start = time.time()
        path = aws.download_s3_file(self.bucket, self.folder, filename, self.s3_client)
        end = time.time()
        self.s3_download_time += int((end - start) * 1000)

        print self.split_size
        print np.load(path).shape

        return np.load(path)

    @classmethod                                                        # alternative constructor
    def left_inputsplit_for(cls, matrix, result_split, unit):
        input_split = { 'x': result_split.x, 'y': unit*result_split.split_size }
        return cls(matrix, input_split, result_split.split_size)

    @classmethod                                                        # alternative constructor
    def right_inputsplit_for(cls, matrix, result_split, unit):
        input_split = { 'x': unit*result_split.split_size, 'y': result_split.y }
        return cls(matrix, input_split, result_split.split_size)
