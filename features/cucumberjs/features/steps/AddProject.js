    module.exports = function () {
    this.World = require('../support/world.js').World;
    var assert = require("assert");

    var testProjectName = 'testProject9';
    var runID, currentField;

    this.Given('I create a new Add Project TestRail run', function(callback) {
        this.createTestRailTestRun(2, 7, function(x) {
            runID = x;
            console.log("The TestRail Run ID for this test run: "+runID);
            callback();
        });
    });  

    this.Given('I am logged in to RSR Admin', function(callback) {
        var browser = this.browser;

        browser.visit("/admin/", function() {
            browser.
            fill('username', 'AutomatedTestUser').
            fill('password', 'testpassword').
            pressButton('Log in', function() {
                assert.ok(browser.success);
                assert.equal(browser.text('#site-name'), 'Akvo RSR administration');
                callback();
            });  
        });
    });

    this.When('I click "add a project"', function(callback) {
        var browser = this.browser;

        browser.clickLink('Projects', function() {
            browser.clickLink('Add project', function() {
                callback();
            })
        });   
    });

    this.When('I create a new project', function(callback) {
        var browser = this.browser;

        browser.
        fill('title', testProjectName).
        fill('subtitle', 'test').
        fill('project_plan_summary', 'test').
        fill('background', 'test').
        fill('current_status', 'test').
        fill('sustainability', 'test').
        fill('goals_overview', 'test').
        select('partnerships-0-partner_type', 'field').
        select('categories', '22').
        pressButton('Save', function() {
            callback();
        });
    });

    this.When('I publish the project', function(callback) {
        var browser = this.browser;

        browser.clickLink('Home', function() {
            browser.clickLink('Publishing statuses', function() {
                browser.clickLink(testProjectName, function(){
                    browser.
                    select('status', 'published').
                    pressButton('Save', function() {
                        callback();
                    })
                });
            });
        });
    });

    this.Then('I can view the project on the main RSR page', function(callback) {
        var browser = this.browser;

        browser.visit('http://rsr.uat.akvo.org/projects/all/', function() {
            //Confirm that the project is present
            assert((browser.html().indexOf(testProjectName) > -1), true);
            callback();
        });
    });

    this.When('I fill out new project details', function(callback) {
        var browser = this.browser;

        browser.
        fill('title', testProjectName).
        fill('subtitle', 'test').
        fill('project_plan_summary', 'test').
        fill('background', 'test').
        fill('current_status', 'test').
        fill('sustainability', 'test').
        fill('goals_overview', 'test').
        select('partnerships-0-partner_type', 'field').
        select('categories', '22');
        callback();
    });

    this.When(/^I do not enter anything for "([^"]*)"$/, function(fieldNameSpaces, callback) {
        var fieldNameUnderscore = fieldNameSpaces.replace(/ /g,"_");
        var browser = this.browser;


        browser.
        fill(fieldNameUnderscore, '').
        pressButton('Save', function() {
            callback();
        });
    });

    this.When('I do not select a project partner', function(callback) {
        var browser = this.browser;

        browser.
        select('partnerships-0-organisation', '---------').
        pressButton('Save', function() {
            callback();
        });
    });

    this.When('I do not select a field partner', function(callback) {
        var browser = this.browser;

        browser.
        select('partnerships-0-partner_type', 'Funding partner').
        pressButton('Save', function() {
            callback();
        });
    });

    this.When('I do not enter a partner type which matches the partner', function(callback) {
        var browser = this.browser;

        browser.
        select('partnerships-0-organisation', 'Abdo').
        select('partnerships-0-partner_type', 'Sponsor partner').
        pressButton('Save', function() {
            callback();
        });
    });

    this.Then('I get an error', function(callback) {  
        var browser = this.browser;

        assert((browser.html().indexOf('This field is required.') > -1), true, 'Expected message: This field is required : was not found');   
        assert((browser.html().indexOf('Please correct the error below.') > -1), true, 'Expected message: Please correct the error below. : was not found'); 
        callback();
    });
};