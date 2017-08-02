{
  "States": {
    "Accumulate": {
      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-unit-accumulate",
      "End": true,
      "Type": "Task"
    },
    "Units": {
      "Branches": [
        {
          "States": {
            "0Intermediates": {
              "Branches": [
                {
                  "States": {
                    "0_m0": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "0_m0",
                      "Next": "0_m0_lambda"
                    },
                    "0_m0_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    }
                  },
                  "StartAt": "0_m0"
                },
                {
                  "States": {
                    "0_m1": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "0_m1",
                      "Next": "0_m1_lambda"
                    },
                    "0_m1_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    }
                  },
                  "StartAt": "0_m1"
                },
                {
                  "States": {
                    "0_m2": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "0_m2",
                      "Next": "0_m2_lambda"
                    },
                    "0_m2_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    }
                  },
                  "StartAt": "0_m2"
                },
                {
                  "States": {
                    "0_m3_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    },
                    "0_m3": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "0_m3",
                      "Next": "0_m3_lambda"
                    }
                  },
                  "StartAt": "0_m3"
                },
                {
                  "States": {
                    "0_m4": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "0_m4",
                      "Next": "0_m4_lambda"
                    },
                    "0_m4_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    }
                  },
                  "StartAt": "0_m4"
                },
                {
                  "States": {
                    "0_m5": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "0_m5",
                      "Next": "0_m5_lambda"
                    },
                    "0_m5_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    }
                  },
                  "StartAt": "0_m5"
                },
                {
                  "States": {
                    "0_m6": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "0_m6",
                      "Next": "0_m6_lambda"
                    },
                    "0_m6_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    }
                  },
                  "StartAt": "0_m6"
                }
              ],
              "Type": "Parallel",
              "Next": "0Collect"
            },
            "0Collect": {
              "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-collector",
              "End": true,
              "Type": "Task"
            }
          },
          "StartAt": "0Intermediates"
        },
        {
          "States": {
            "1Collect": {
              "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-collector",
              "End": true,
              "Type": "Task"
            },
            "1Intermediates": {
              "Branches": [
                {
                  "States": {
                    "1_m0_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    },
                    "1_m0": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "1_m0",
                      "Next": "1_m0_lambda"
                    }
                  },
                  "StartAt": "1_m0"
                },
                {
                  "States": {
                    "1_m1": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "1_m1",
                      "Next": "1_m1_lambda"
                    },
                    "1_m1_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    }
                  },
                  "StartAt": "1_m1"
                },
                {
                  "States": {
                    "1_m2": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "1_m2",
                      "Next": "1_m2_lambda"
                    },
                    "1_m2_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    }
                  },
                  "StartAt": "1_m2"
                },
                {
                  "States": {
                    "1_m3": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "1_m3",
                      "Next": "1_m3_lambda"
                    },
                    "1_m3_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    }
                  },
                  "StartAt": "1_m3"
                },
                {
                  "States": {
                    "1_m4": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "1_m4",
                      "Next": "1_m4_lambda"
                    },
                    "1_m4_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    }
                  },
                  "StartAt": "1_m4"
                },
                {
                  "States": {
                    "1_m5": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "1_m5",
                      "Next": "1_m5_lambda"
                    },
                    "1_m5_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    }
                  },
                  "StartAt": "1_m5"
                },
                {
                  "States": {
                    "1_m6": {
                      "OutputPath": "$",
                      "ResultPath": "$.intermediate",
                      "Type": "Pass",
                      "Result": "1_m6",
                      "Next": "1_m6_lambda"
                    },
                    "1_m6_lambda": {
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-intermediate",
                      "End": true,
                      "Type": "Task"
                    }
                  },
                  "StartAt": "1_m6"
                }
              ],
              "Type": "Parallel",
              "Next": "1Collect"
            }
          },
          "StartAt": "1Intermediates"
        }
      ],
      "Type": "Parallel",
      "Next": "Accumulate"
    }
  },
  "StartAt": "Units"
}
