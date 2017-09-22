import numpy as np
import os

def write_to_s3(data, bucket, folder, key, s3_client):
    s3_client.put_object(Body=data.dumps(), Bucket=bucket, Key=folder + '/' + key)


def download_s3_file(bucket, folder, filename, s3_client):
    if not os.path.exists('/tmp/' + folder):
        os.mkdir('/tmp/' + folder)

    key = folder + "/" + filename # e.g. 'S3_U0_m2'
    s3_client.download_file(bucket, key, '/tmp/' + key)
    return '/tmp/' + key
