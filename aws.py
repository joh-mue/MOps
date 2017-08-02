import numpy as np
import os

def write_to_s3(data, bucket, folder, key, s3_client):
  if not os.path.exists('/tmp/' + folder):
    os.mkdir('/tmp/' + folder)
  
  tmp_filepath = "/tmp/{folder}/{key}.npy".format(folder=folder, key=key)
  with open(tmp_filepath, 'wb') as tmp_file:
    np.save(tmp_filepath, data)

  s3_client.upload_file(tmp_filepath, bucket, folder + "/" + key)


def download_s3_file(bucket, folder, filename, s3_client):
  if not os.path.exists('/tmp/' + folder):
    os.mkdir('/tmp/' + folder)
  
  key = folder + "/" + filename # e.g. m_0_0.npy
  s3_client.download_file(bucket, key, '/tmp/' + key)
  return '/tmp/' + key
