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

class Split(object):
    'Class that represents a matrix split'

    s3_client = boto3.client('s3')
    split_size = 2000
    s3_download_time = 0

    def __init__(self, matrix, split):
        self.x = split['x']
        self.y = split['y']
        self.bucket = matrix['bucket']
        self.folder = matrix['folder']

    def block(self, x, y):
        '''
        Load block m_{x}_{y} from s3 and return it as numpy matrix, x and y can be
        0 or 1 and indicate relative position within the split. Absolute block index and filename
        are calculated and used to download from s3.
        '''
        block_x = (self.x + x * (self.split_size/2)) / self.split_size/2
        block_y = (self.y + y * (self.split_size/2)) / self.split_size/2
        filename = "m_{}_{}.npy".format(block_x, block_y)
        
        start = time.time()
        path = aws.download_s3_file(self.bucket, self.folder, filename, self.s3_client)
        end = time.time()
        self.s3_download_time += end - start

        return np.load(path)

    @classmethod                                                        # alternative constuctor
    def left_inputsplit_for(cls, matrix, result_split, unit):
        input_split = { 'x': result_split.x, 'y': unit*cls.split_size }
        return cls(matrix, input_split)

    @classmethod                                                        # alternative constuctor
    def right_inputsplit_for(cls, matrix, result_split, unit):
        input_split = { 'x': unit*cls.split_size, 'y': result_split.y }
        return cls(matrix, input_split)
