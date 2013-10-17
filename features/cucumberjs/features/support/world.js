var Browser = require("zombie");

var World = function World(callback) {
    this.browser = new Browser({ debug: true });
    this.browser.site = "http://rsr.uat.akvo.org/";

    var resetBrowser;
    resetBrowser = this.resetBrowser = function(){
        console.log("RESET BROWSER");
        this.browser = new Browser({ debug: true });
        this.browser.site = "http://rsr.uat.akvo.org/";
    }

    // TestRail helper functions
    var baseCurlCommand = "curl -H \"Content-Type: application/json\" -u 'devops@akvo.org:R4inDr0p!' "

    var submitPassFailToTestRail, submitIndividualTestStep, createTestRailTestRun, testRailResponse;

    createTestRailTestRun = this.createTestRailTestRun = function(projectId, suiteId, callback){
        var command = baseCurlCommand + "-d '{\"suite_id\":"+suiteId+"}' \"https://akvo.testrail.com/index.php?/api/v2/add_run/"+projectId+"\"";
        exec(command, function (error, stdout, stderr) { 
            return callback(getTestRunIdFromResponse(stdout));
        });
    }

    submitPassFailToTestRail = this.submitPassFailToTestRail = function(testRunStatus, testRunId, testCaseId){
        var command = baseCurlCommand + "-d '{\"status_id\":"+testRunStatus+"}' \"https://akvo.testrail.com/index.php?/api/v2/add_result_for_case/"+testRunId+"/"+testCaseId+"\"";
        exec(command, function (error, stdout, stderr) {});
    }

    // {"custom_step_results": [{"content": "Step 1","expected": "Expected Result 1","actual": "Actual Result 1","status_id": 1}]}
    submitIndividualTestSteps = this.submitIndividualTestSteps = function(testStepResults, testRunId, testCaseId){
        // make sure there's no unnecessary commas floating around
        if(testStepResults.charAt(testStepResults.length-1) == ','){
            testStepResults = testStepResults.substring(0,testStepResults.length-1);
        }
        var command = baseCurlCommand + "-d '{\"custom_step_results\": ["+testStepResults+"]}' \"https://akvo.testrail.com/index.php?/api/v2/add_result_for_case/"+testRunId+"/"+testCaseId+"\"";
        exec(command, function (error, stdout, stderr) {});
    }

    // Takes the JSON response from testrail and breaks it down to get the test run ID from the end URL. Example response:
    // {"id":8,"suite_id":7,"name":"Project Administration","description":null,"milestone_id":null,"assignedto_id":null,"include_all":true,"is_completed":false,"completed_on":null,"config":null,"passed_count":0,"blocked_count":0,"untested_count":19,"retest_count":0,"failed_count":0,"custom_status1_count":0,"custom_status2_count":0,"custom_status3_count":0,"custom_status4_count":0,"custom_status5_count":0,"custom_status6_count":0,"custom_status7_count":0,"project_id":2,"plan_id":null,"url":"https:\/\/akvo.testrail.com\/index.php?\/runs\/view\/8"}
    function getTestRunIdFromResponse(response){
        response = JSON.stringify(response);
        var strippedResponse = response.substring(1,response.length-1);
        var responseBits = strippedResponse.split(",");
        var testRunURL = responseBits[responseBits.length-1].split(":")[2];
        var testRunURLBits= testRunURL.split("/");
        var testRunId = testRunURLBits[testRunURLBits.length-1];
        this.globalTestRunID = testRunId.replace(/"|\\|}+/g,"");
        return globalTestRunID;
    }

    callback();
};

exports.World = World;