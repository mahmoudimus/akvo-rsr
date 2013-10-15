var util = require('util');
var sys = require('sys')
var exec = require('child_process').exec;

try {
    var Spooky = require('spooky');
} catch (e) {
    var Spooky = require(__dirname+'/../../../../lib/spooky');
}

var World = function World(callback) {
    var spooky;
    var world = this;

    spooky = world.spooky = new Spooky({
        child: {
            "web-security": false,
            "ignore-ssl-errors": true
        },
        casper: {
            logLevel: 'debug',
            verbose: true,
            timeout: 30000,
            stepTimeout: 15000
        }
    }, function(error) {
        if (error) {
            console.dir(error);
            throw new Error('Failed to initialize context.spooky: ' +
                error.code + ' - '  + error.message);
            callback.fail();
        }
        
        // Expects errors like below:
        // {"success":false,"type":"assertTextExists","standard":"Found expected text within the document body","message":"RSR has thrown an error, as indicated by 'This field is required.' being present","file":null,"doThrow":true,"values":{"subject":false,"text":"This field is required."},"suite":"Untitled suite in null","time":5133}
        spooky.on('test.has.failed', function (error) {
            console.log("Caught failing test step: "+error);
            globalIsFailedStep = true;
            processTestResult(error, 5);
            spooky.destroy();
        });


        spooky.on('test.has.passed', function () {
            processTestResultSimple();
        });

        spooky.on('error', function(e) {
            console.error('spooky error', util.inspect(e));
        });

        spooky.on('console', function (line) {
            console.log(line);
        });

        callback(world);
       }); 

    var globalTestRunID = world.globalTestRunID;
    var globalCurrentField = world.globalCurrentField;
    var globalIsFailedStep = world.globalIsFailedStep = false;

    function processTestResultSimple(){
        if(!this.globalIsFailedStep){
            submitIfTestCaseExists(globalCurrentField,1, this.globalTestRunID);
        }
    }

    function processTestResult(result, passFail){
        result = JSON.stringify(result);
        var strippedResponse = result.substring(1,result.length-1);
        var responseBits = strippedResponse.split(",");
        var testMessage = responseBits[3].split(":")[1];
        var resultFor=testMessage.match(/\*([^}]+)\*/g);
        resultFor = JSON.stringify(resultFor);
        resultFor = resultFor.substring(3,resultFor.length-3);
        submitIfTestCaseExists(resultFor, passFail, this.globalTestRunID);
    }

    var submitIfTestCaseExists;
    submitIfTestCaseExists = world.submitIfTestCaseExists = function(testCase, statusId, testRunId){
        if (testCase in addProjectTestCaseIdMap) {
            submitResultsToTestRail(statusId, testRunId, addProjectTestCaseIdMap[testCase]);
        }
    }

    // Spooky utility functions
    var fillForm, clickLink, takeScreenShot, setUpTestingLog;

    takeScreenShot = world.takeScreenShot = function(screenName, testProjectName){
        spooky.then([
            {
                renderName: screenName + testProjectName +'.png',
                width: 1280,
                height: 10024,
                delay: 100
            }, function() {
                this.viewport(width, height);
                this.capture(renderName, {
                    top: 0,
                    left: 0,
                    width: width,
                    height: height
                });
            }
        ]);
    }
    clickLink = world.clickLink = function(linkSelector){
        spooky.then([
            {
                linkSelector : linkSelector
            }, function(){
                this.click(linkSelector);
            }
        ]);
    }
    fillForm = world.fillForm = function(formName, formData, submit){
        spooky.then([
            {
                formName : formName,
                formData : formData,
                submit : submit
            }, function(){
                this.fill(formName, formData, submit);
            }
        ]);
    }
    setUpTestingLog = world.setUpTestingLog = function(){
        spooky.then(function(){
            var casper = this;
            this.test.on('fail', function(error){
                casper.emit('test.has.failed', JSON.stringify(error));
            });
            this.test.on('success', function(error){
                casper.emit('test.has.passed');
            });
        });
    }
    // TestRail helper functions
    var baseCurlCommand = "curl -H \"Content-Type: application/json\" -u 'devops@akvo.org:R4inDr0p!' "

    var addProjectTestCaseIdMap = {};

    addProjectTestCaseIdMap['project_added'] = 44;
    addProjectTestCaseIdMap['title'] = 45;
    addProjectTestCaseIdMap['subtitle'] = 46;
    addProjectTestCaseIdMap['project_plan_summary'] = 47;
    addProjectTestCaseIdMap['background'] = 48;
    addProjectTestCaseIdMap['current_status'] = 92;
    addProjectTestCaseIdMap['sustainability'] = 49;
    addProjectTestCaseIdMap['goals_overview'] = 50;

    var submitResultsToTestRail, createTestRailTestRun, testRailResponse;

    createTestRailTestRun = world.createTestRailTestRun = function(projectId, suiteId, callback){
        var command = baseCurlCommand + "-d '{\"suite_id\":"+suiteId+"}' \"https://akvo.testrail.com/index.php?/api/v2/add_run/"+projectId+"\"";
        exec(command, function (error, stdout, stderr) { 
            return callback(getTestRunIdFromResponse(stdout));
        });
    }

    submitResultsToTestRail = world.submitResultsToTestRail = function(testRunStatus, testRunId, testCaseId){
        var command = baseCurlCommand + "-d '{\"status_id\":"+testRunStatus+"}' \"https://akvo.testrail.com/index.php?/api/v2/add_result_for_case/"+testRunId+"/"+testCaseId+"\"";
        console.log(command);
        exec(command, function (error, stdout, stderr) { 
        });
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

    // Setter functions

    var setFieldName;
    setFieldName = world.setFieldName = function(fieldName){
        scopedFieldNameSetter(fieldName);
    }

    function scopedFieldNameSetter(fieldName){
        globalCurrentField = fieldName;
    }
};
module.exports.World = World;