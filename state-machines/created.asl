{
  "StartAt": "Units",
  "States": {
    "Accumulate": {
      "End": true,
      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-unit-accumulator",
      "Type": "Task"
    },
    "Units": {
      "Branches": [
        {
          "StartAt": "unit0",
          "States": {
            "U0_Collect": {
              "End": true,
              "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-collector",
              "Type": "Task"
            },
            "U0_Intermediate": {
              "Branches": [
                {
                  "StartAt": "U0_m0",
                  "States": {
                    "U0_m0": {
                      "Next": "U0_m0_lambda",
                      "OutputPath": "$",
                      "Result": 0,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U0_m0_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                },
                {
                  "StartAt": "U0_m1",
                  "States": {
                    "U0_m1": {
                      "Next": "U0_m1_lambda",
                      "OutputPath": "$",
                      "Result": 1,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U0_m1_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                },
                {
                  "StartAt": "U0_m2",
                  "States": {
                    "U0_m2": {
                      "Next": "U0_m2_lambda",
                      "OutputPath": "$",
                      "Result": 2,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U0_m2_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                },
                {
                  "StartAt": "U0_m3",
                  "States": {
                    "U0_m3": {
                      "Next": "U0_m3_lambda",
                      "OutputPath": "$",
                      "Result": 3,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U0_m3_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                },
                {
                  "StartAt": "U0_m4",
                  "States": {
                    "U0_m4": {
                      "Next": "U0_m4_lambda",
                      "OutputPath": "$",
                      "Result": 4,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U0_m4_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                },
                {
                  "StartAt": "U0_m5",
                  "States": {
                    "U0_m5": {
                      "Next": "U0_m5_lambda",
                      "OutputPath": "$",
                      "Result": 5,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U0_m5_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                },
                {
                  "StartAt": "U0_m6",
                  "States": {
                    "U0_m6": {
                      "Next": "U0_m6_lambda",
                      "OutputPath": "$",
                      "Result": 6,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U0_m6_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                }
              ],
              "Next": "U0_Collect",
              "OutputPath": "$",
              "ResultPath": "$.responses",
              "Type": "Parallel"
            },
            "unit0": {
              "Next": "U0_Intermediate",
              "OutputPath": "$",
              "Result": "0",
              "ResultPath": "$.unit",
              "Type": "Pass"
            }
          }
        },
        {
          "StartAt": "unit1",
          "States": {
            "U1_Collect": {
              "End": true,
              "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-collector",
              "Type": "Task"
            },
            "U1_Intermediate": {
              "Branches": [
                {
                  "StartAt": "U1_m0",
                  "States": {
                    "U1_m0": {
                      "Next": "U1_m0_lambda",
                      "OutputPath": "$",
                      "Result": 0,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U1_m0_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                },
                {
                  "StartAt": "U1_m1",
                  "States": {
                    "U1_m1": {
                      "Next": "U1_m1_lambda",
                      "OutputPath": "$",
                      "Result": 1,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U1_m1_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                },
                {
                  "StartAt": "U1_m2",
                  "States": {
                    "U1_m2": {
                      "Next": "U1_m2_lambda",
                      "OutputPath": "$",
                      "Result": 2,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U1_m2_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                },
                {
                  "StartAt": "U1_m3",
                  "States": {
                    "U1_m3": {
                      "Next": "U1_m3_lambda",
                      "OutputPath": "$",
                      "Result": 3,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U1_m3_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                },
                {
                  "StartAt": "U1_m4",
                  "States": {
                    "U1_m4": {
                      "Next": "U1_m4_lambda",
                      "OutputPath": "$",
                      "Result": 4,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U1_m4_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                },
                {
                  "StartAt": "U1_m5",
                  "States": {
                    "U1_m5": {
                      "Next": "U1_m5_lambda",
                      "OutputPath": "$",
                      "Result": 5,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U1_m5_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                },
                {
                  "StartAt": "U1_m6",
                  "States": {
                    "U1_m6": {
                      "Next": "U1_m6_lambda",
                      "OutputPath": "$",
                      "Result": 6,
                      "ResultPath": "$.intermediate",
                      "Type": "Pass"
                    },
                    "U1_m6_lambda": {
                      "End": true,
                      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
                      "Type": "Task"
                    }
                  }
                }
              ],
              "Next": "U1_Collect",
              "OutputPath": "$",
              "ResultPath": "$.responses",
              "Type": "Parallel"
            },
            "unit1": {
              "Next": "U1_Intermediate",
              "OutputPath": "$",
              "Result": "1",
              "ResultPath": "$.unit",
              "Type": "Pass"
            }
          }
        }
      ],
      "Next": "Accumulate",
      "OutputPath": "$",
      "ResultPath": "$.responses",
      "Type": "Parallel"
    }
  }
}
