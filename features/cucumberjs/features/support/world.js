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
    
        spooky.on('error', function(e) {
            console.error('spooky error', util.inspect(e));
        });

        spooky.on('console', function (line) {
            console.log(line);
        });

        callback(world);
       }); 

    // Spooky utility functions
    var fillForm, clickLink, takeScreenShot;

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

    // TestRail helper functions
    var submitResultsToTestRail, createTestRailTestRun;

    // /api/v2/add_run/<project_id>
    // args:
    // suited_id    int     required
    // name         string  
    // description  string
    // milestone_id int
    // case_ids     array

    // should return a run id, need to grab this somehow
    createTestRailTestRun = world.createTestRailTestRun = function(projectId){
        var command = "curl -H 'Content-Type: application/json' -u 'devops@akvo.org:R4inDr0p!' -d '{'status_id':1}' 'https://akvo.testrail.com/index.php?/api/v2//api/v2/add_run/"+projectId+"'";
        exec(command, puts);
    }

    // /api/v2/add_result_for_case/<test_run_id>/<test_case_id>
    // args:
    // status_id    int     required
    // comment      string  
    // version      string
    // elapsed      timespan e.g. "30s" or "1m 45s"
    // defects      string (comma seperated list of github issues?)
    // custom_ste_results     array

    // status ids 1 = passed, 2 = blocked, 4 = retest, 5 = failed
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
    submitResultsToTestRail = world.submitResultsToTestRail = function(testRunId, testCaseId){
        var command = "curl -H 'Content-Type: application/json' -u 'devops@akvo.org:R4inDr0p!' -d '{'status_id':1}' 'https://akvo.testrail.com/index.php?/api/v2/add_result_for_case/"+testRunId+"/"+testCaseId+"'";
        exec(command, puts);
    }

    function puts(error, stdout, stderr) { sys.puts(stdout) }
};
module.exports.World = World;
