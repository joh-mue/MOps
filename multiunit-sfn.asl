{
  "Comment": "Multi Unit Strassen Implementation",
  "StartAt": "Calculation",
  "Calculation": {
    "Type": "Parallel",
    "Branches": [{
        "Partials": {
          "Type": "Parallel",
          "Branches": [
            {
              "Intermediates":{},
              "Collect":{}
            },
            {
              "Intermediates":{},
              "Collect":{}
            }
          ]
        },
        "Accumulate": {}
      },      {
        "Partials": {
          "Type": "Parallel",
          "Branches": [
            {
              "Intermediates":{},
              "Collect":{}
            },
            {
              "Intermediates":{},
              "Collect":{}
            }
          ]
        },
        "Accumulate": {}
      },{
        "Partials": {
          "Type": "Parallel",
          "Branches": [
            {
              "Intermediates":{},
              "Collect":{}
            },
            {
              "Intermediates":{},
              "Collect":{}
            }
          ]
        },
        "Accumulate": { }
      },{
        "Partials": {
          "Type": "Parallel",
          "Branches": [
            {
              "Intermediates":{},
              "Collect":{}
            },
            {
              "Intermediates":{},
              "Collect":{}
            }
          ]
        },
        "Accumulate": {}
      }
    ]
  }
}
