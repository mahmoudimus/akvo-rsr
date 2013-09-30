// Method:	add_result
// HTTP:	POST
// URL:	index.php?/miniapi/add_result/<test_id>
// Result:	ID of the test change

// Post arguments:
// status_id
//    1 = Passed
//    2 = Blocked
//    4 = Retest
//    5 = Failed
// comment
// version
// elapsed
// defects
// assignedto_id
// custom fields can be added with their system names, prefixed with 'custom_'

// 'custom_steps_separated':[
//   {
//     "status_id": 1,
//     "content": "Step 1", 
//     "expected": "Result 1",
//     "actual": "Actual Result 1"
//   },
//   {
//     "status_id": 5,
//     "content": "Step 2",
//     "expected": "Result 2",
//     "actual": "Actual Result 2"
//   }
// ]

// The curl script I've been using:
// curl -H "Content-Type: application/json" -u 'devops@akvo.org:R4inDr0p!' -d '{"status_id":1}' "https://akvo.testrail.com/index.php?/api/v2/add_result_for_case/7/68"
// response: {"id":31,"test_id":73,"status_id":1,"created_by":1,"created_on":1380533401,"assignedto_id":null,"comment":null,"version":null,"elapsed":null,"defects":null,"custom_step_results":null}

var casper = require('casper');

casper.start();

//change this to a util method which takes a result and a test_id
casper.open('https://akvo.testrail.com/index.php?/api/v2/add_result_for_case/<run_id>/<test_id>', {
    method: 'post',
    data:   {
    	//insert test result here
    },
    headers: {
        'Content-type': 'application/json'
    }
});

casper.run();