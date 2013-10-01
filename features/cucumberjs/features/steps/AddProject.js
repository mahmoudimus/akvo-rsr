module.exports = function () {
    this.World = require('../support/world.js').World;
   
    var adminUrl = 'http://rsr.test.akvo-ops.org/admin/';
    var testProjectName = 'testProject9';
    var runID;

    this.Given('I create a new Add Project TestRail run', function(callback){
        this.createTestRailTestRun(2, 7, function(x){
            runID = x;
            console.log("The TestRail Run ID for this test run: "+runID);
            callback();
        });
    });  

    this.Given('I am logged in to RSR Admin', function(callback){
        this.spooky.open(adminUrl);
        this.fillForm('form#login-form', 
                {
                    'username' : 'AutomatedTestUser',
                    'password' : 'testpassword'
                }, true);
        callback();
    });

    this.When('I click "add a project"', function(callback) {
       // There is presumably a better way of doing this - <a href="/admin/rsr/project/add/" class="addlink">Add</a>
        this.clickLink('a[href="/admin/rsr/project/add/"]');   
        callback();
    });

    this.When('I fill out new project details', function(callback) {
        this.fillForm('form#project_form', 
                {
                    'title' : testProjectName,
                    'subtitle' : 'test',
                    'project_plan_summary' : 'test',
                    'background' : 'test',
                    'current_status' : 'test',
                    'sustainability' : 'test',
                    'goals_overview': 'test',
                    'partnerships-0-partner_type' : 'field',
                    'categories' : '22'
                }, false);

        callback();
    });

    this.When('I click the save button', function(callback) {
        this.clickLink('input[name="_save"]');
        callback();
    });

    this.When('I publish the project', function(callback) {
        //Another way of doing this is by just appending the project ID to the below URLS
        this.clickLink('a[href="/admin/rsr/"]');

        //<a href="/admin/rsr/publishingstatus/">Publishing statuses</a>
        this.clickLink('a[href="/admin/rsr/publishingstatus/"]');

        //<a href="1102/">test</a>
        this.spooky.then([
            {
                testProjectName : testProjectName
            }, function(){
                this.clickLabel(testProjectName, 'a');
            }
        ]);

        this.fillForm('form#publishingstatus_form', 
                {
                    'status' : 'published'
                }, false);

        this.clickLink('input[name="_save"]');

        callback();
    });

    this.Then('I can view the project on the main RSR page', function(callback) {
        this.clickLink('a[href="/admin/rsr/"]');
        this.clickLink('a[href="/admin/rsr/project/"]');

        this.fillForm('form#changelist-search', 
                {
                    'q' : testProjectName
                }, true);

        this.takeScreenShot('projectSearch', testProjectName);

         this.spooky.then([
            {
              testProjectName : testProjectName
            }, function() {
                this.test.assertSelectorHasText('#result_list', testProjectName);
                this.test.assertResourceExists('icon-yes.gif');
            }
        ]);

        this.spooky.run();
        setTimeout(callback, 20000)
    });

    this.When(/^I do not enter anything for "([^"]*)"$/, function(fieldNameSpaces, callback) {
        var fieldNameUnderscore = fieldNameSpaces.replace(/ /g,"_");
        var formData = { };
        formData[fieldNameUnderscore] = '';

        this.fillForm('form#project_form', formData, false);
        callback();
    });

    this.Then('I get an error', function(callback) {  
        this.spooky.then(function() {
            this.test.assertTextExists('This field is required.', "RSR has thrown an error, as indicated by 'This field is required.' being present");
            this.test.assertTextExists('Please correct the error below.', "RSR has thrown an error, as indicated by 'Please correct the error below.' being present");
            this.test.assertExists('.errornote', 'Found errornote class element');
        });

        this.takeScreenShot('fieldError', testProjectName);

        this.spooky.run();
        setTimeout(callback, 20000)
    });
};