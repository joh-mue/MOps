### Matrix Operations on AWS Lambda with Serverles Framework

`serial-multiply.py` performs multiplication of matrix A and B on on worker and saves Result to S3

`parallel-multiplication.py` performs multiplication of matrix A and B by calling many `cellcalc.py` lambdas which calculate a partial result and save it to S3
