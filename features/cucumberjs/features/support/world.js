var Browser = require("zombie");

var World = function World(callback) {
    this.browser = new Browser({ debug: true });
    this.browser.site = "http://rsr.uat.akvo.org/";
    this.browser.on('error',function(e){
        console.log("Error: " +e.message); 
        console.log(e.stack);
    });

    // TestRail case IDs - temp location
    var addProjectTestCaseIdMap = {};

    addProjectTestCaseIdMap['project_added'] = 44;
    addProjectTestCaseIdMap['title'] = 45;
    addProjectTestCaseIdMap['subtitle'] = 46;
    addProjectTestCaseIdMap['project_plan_summary'] = 47;
    addProjectTestCaseIdMap['background'] = 48;
    addProjectTestCaseIdMap['current_status'] = 92;
    addProjectTestCaseIdMap['sustainability'] = 49;
    addProjectTestCaseIdMap['goals_overview'] = 50;

    // TestRail helper functions
    var baseCurlCommand = "curl -H \"Content-Type: application/json\" -u 'devops@akvo.org:R4inDr0p!' "

    var submitResultsToTestRail, createTestRailTestRun, testRailResponse;

    createTestRailTestRun = World.createTestRailTestRun = function(projectId, suiteId, callback){
        var command = baseCurlCommand + "-d '{\"suite_id\":"+suiteId+"}' \"https://akvo.testrail.com/index.php?/api/v2/add_run/"+projectId+"\"";
        exec(command, function (error, stdout, stderr) { 
            return callback(getTestRunIdFromResponse(stdout));
        });
    }

    submitResultsToTestRail = World.submitResultsToTestRail = function(testRunStatus, testRunId, testCaseId){
        var command = baseCurlCommand + "-d '{\"status_id\":"+testRunStatus+"}' \"https://akvo.testrail.com/index.php?/api/v2/add_result_for_case/"+testRunId+"/"+testCaseId+"\"";
        console.log(command);
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