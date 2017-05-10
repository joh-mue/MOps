```time sls invoke local -v --log --function serial-multiplication --data '{ "bucket": "jmue-matrix-tests", "matrix-a-key": "test-matrix-A-1000", "matrix-b-key": "test-matrix-B-1000" , "matrix-c-key": "result-matrix-C-1000" }'
{
    "status": "done",
    "result-bucket": "jmue-matrix-tests",
    "result-key": "result-matrix-C-1000"
}
      315.47 real       190.15 user         2.07 sys
```

```
time sls invoke local -v --log --function cellcalc --data '{ "matrix-a-key": "test-matrix-A-1000", "matrix-b-key": "test-matrix-B-1000", "matrix-c-key": "result-matrix-P-1000", "row": 1, "column": 1, "bucket": "jmue-matrix-tests" }'
{u'matrix-b-key': u'test-matrix-B-1000', u'bucket': u'jmue-matrix-tests', u'column': 1, u'matrix-c-key': u'result-matrix-P-1000', u'matrix-a-key': u'test-matrix-A-1000', u'row': 1}
{
    "cell-value": 500500,
    "bucket": "jmue-matrix-tests",
    "cell-key": "result-matrix-P-1000-1-1"
}
       12.56 real         6.44 user         0.54 sys
```


```
time sls invoke local -v --log --function parallel-multiplication --data '{ "bucket": "jmue-matrix-tests", "matrix-a-key": "test-matrix-A-1000", "matrix-b-key": "test-matrix-B-1000", "matrix-c-key": "result-matrix-P-1000", "matrix-a-size": "1000", "matrix-b-size": "1000" }'
```

serial-multiplication

Timeout for 1024MB

```
START RequestId: b35eaef4-2018-11e7-82a4-b58de9aa853a Version: $LATEST
END RequestId: b35eaef4-2018-11e7-82a4-b58de9aa853a
REPORT RequestId: b35eaef4-2018-11e7-82a4-b58de9aa853a  Duration: 219428.94 ms  Billed Duration: 219500 ms  Memory Size: 1536 MB  Max Memory Used: 149 MB 
```

cellcalc

```
START RequestId: f2407107-2019-11e7-b638-715cfc1ca55e Version: $LATEST
{u'matrix-b-key': u'test-matrix-B-1000', u'bucket': u'jmue-matrix-tests', u'column': 1, u'matrix-c-key': u'result-matrix-P-1000', u'matrix-a-key': u'test-matrix-A-1000', u'row': 1}
END RequestId: f2407107-2019-11e7-b638-715cfc1ca55e
REPORT RequestId: f2407107-2019-11e7-b638-715cfc1ca55e  Duration: 25275.26 ms Billed Duration: 25300 ms   Memory Size: 256 MB Max Memory Used: 99 MB 
```

```
START RequestId: 2e95d802-201a-11e7-964b-f75b1d83fab1 Version: $LATEST
{u'matrix-b-key': u'test-matrix-B-1000', u'bucket': u'jmue-matrix-tests', u'column': 2, u'matrix-c-key': u'result-matrix-P-1000', u'matrix-a-key': u'test-matrix-A-1000', u'row': 2}
END RequestId: 2e95d802-201a-11e7-964b-f75b1d83fab1
REPORT RequestId: 2e95d802-201a-11e7-964b-f75b1d83fab1  Duration: 25278.08 ms Billed Duration: 25300 ms   Memory Size: 256 MB Max Memory Used: 106 MB 
```

```
219428,94 / 25275,25 = 8,68
219500/25300 = 8,68
```

1000000 * 25300 * 256
Vendor      Request Cost  Compute Cost  Total
AWS Lambda  $0.20         $105.44       $105.64

1 * 219500 * 1536
Vendor      Request Cost  Compute Cost  Total
AWS Lambda  $0.00         $0.01         $0.01


```
{
  "cell-value": 1501500,
  "bucket": "jmue-matrix-tests",
  "timings": {
    "write-to-file": 0,
    "calculate-cell": 0,
    "write-to-s3": 232
  },
  "cell-key": "result-matrix-P-1000-3-3"
}

START RequestId: ebd032d1-201d-11e7-b8f9-219358045b87 Version: $LATEST
{u'matrix-b-key': u'test-matrix-B-1000', u'bucket': u'jmue-matrix-tests', u'column': 3, u'matrix-c-key': u'result-matrix-P-1000', u'matrix-a-key': u'test-matrix-A-1000', u'row': 3}
END RequestId: ebd032d1-201d-11e7-b8f9-219358045b87
REPORT RequestId: ebd032d1-201d-11e7-b8f9-219358045b87  Duration: 24660.42 ms Billed Duration: 24700 ms   Memory Size: 256 MB Max Memory Used: 97 MB 
```

```
{
  "cell-value": 2002000,
  "bucket": "jmue-matrix-tests",
  "timings": {
    "load-from-s3": 24401,
    "write-to-file": 0,
    "calculate-cell": 0,
    "write-to-s3": 232
  },
  "cell-key": "result-matrix-P-1000-4-4"
}
START RequestId: 8b9c66f9-201e-11e7-88ca-73cf503252ef Version: $LATEST
{u'matrix-b-key': u'test-matrix-B-1000', u'bucket': u'jmue-matrix-tests', u'column': 4, u'matrix-c-key': u'result-matrix-P-1000', u'matrix-a-key': u'test-matrix-A-1000', u'row': 4}
END RequestId: 8b9c66f9-201e-11e7-88ca-73cf503252ef
REPORT RequestId: 8b9c66f9-201e-11e7-88ca-73cf503252ef  Duration: 24680.55 ms Billed Duration: 24700 ms   Memory Size: 256 MB Max Memory Used: 99 MB
```
