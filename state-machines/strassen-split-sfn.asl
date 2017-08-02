{
  "Comment": "Strassen implemented with StepFunctions",
  "StartAt": "Intermediates",
  "States": {
    "Intermediates": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "m_0",
          "States": {
            "m_0": {
              "Type": "Pass",
              "Result": "m_0",
              "ResultPath": "$.intermediate",
              "OutputPath": "$",
              "Next": "m_0_lambda"
            },
            "m_0_lambda": {
              "Type": "Task",
              "Resource": 
                "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
              "End": true
            }
          }
        },
        {
          "StartAt": "m_1",
          "States": {
            "m_1": {
              "Type": "Pass",
              "Result": "m_1",
              "ResultPath": "$.intermediate",
              "OutputPath": "$",
              "Next": "m_1_lambda"
            },
            "m_1_lambda": {
              "Type": "Task",
              "Resource": 
                "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
              "End": true
            }
          }
        },
        {
          "StartAt": "m_2",
          "States": {
            "m_2": {
              "Type": "Pass",
              "Result": "m_2",
              "ResultPath": "$.intermediate",
              "OutputPath": "$",
              "Next": "m_2_lambda"
            },
            "m_2_lambda": {
              "Type": "Task",
              "Resource": 
                "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
              "End": true
            }
          }
        },
        {
          "StartAt": "m_3",
          "States": {
            "m_3": {
              "Type": "Pass",
              "Result": "m_3",
              "ResultPath": "$.intermediate",
              "OutputPath": "$",
              "Next": "m_3_lambda"
            },
            "m_3_lambda": {
              "Type": "Task",
              "Resource": 
                "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
              "End": true
            }
          }
        },
        {
          "StartAt": "m_4",
          "States": {
            "m_4": {
              "Type": "Pass",
              "Result": "m_4",
              "ResultPath": "$.intermediate",
              "OutputPath": "$",
              "Next": "m_4_lambda"
            },
            "m_4_lambda": {
              "Type": "Task",
              "Resource": 
                "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
              "End": true
            }
          }
        },
        {
          "StartAt": "m_5",
          "States": {
            "m_5": {
              "Type": "Pass",
              "Result": "m_5",
              "ResultPath": "$.intermediate",
              "OutputPath": "$",
              "Next": "m_5_lambda"
            },
            "m_5_lambda": {
              "Type": "Task",
              "Resource": 
                "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
              "End": true
            }
          }
        },
        {
          "StartAt": "m_6",
          "States": {
            "m_6": {
              "Type": "Pass",
              "Result": "m_6",
              "ResultPath": "$.intermediate",
              "OutputPath": "$",
              "Next": "m_6_lambda"
            },
            "m_6_lambda": {
              "Type": "Task",
              "Resource": 
                "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-intermediate",
              "End": true
            }
          }
        }
      ],
      "ResultPath": "$.responses",
      "OutputPath": "$",
      "Next": "Collect"
    },

    "Collect": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:eu-central-1:146904559692:function:mmultiply-prod-strassen-split-collector",
      "End": true
    }
  }
}
