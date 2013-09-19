module.exports = function () {
    this.World = require('../support/world.js').World;
    this.Chai = require('../../../node_modules/chai');
   
    var adminUrl = 'http://rsr.test.akvo-ops.org/admin/';

    this.When('I am logged in to RSR Admin', function(callback){
        console.log('hello from 1');
        this.spooky.open(adminUrl);
        console.log('hello from 2');
        this.spooky.then(function(){ 
            this.fill('form#login-form', {'username' : 'AutomatedTestUser','password' : 'testpassword'}, true)
        });
        console.log('hello from 3');
        this.spooky.then(function () {
            this.clickLabel('Projects', 'a');
        });
        console.log('hello from 4');
        this.spooky.then([
            {
                renderName: 'test.png',
                width: 1280,
                height: 1024,
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

        callback();
    });

    this.When(/^I click "([^"]*)"$/, function(arg1, callback) {
        callback.pending();
    });

    this.When(/^I fill out new project details$/, function(callback) {
        callback.pending();
    });

    this.When(/^I click the save button$/, function(callback) {
        callback.pending();
    });

    this.When(/^I publish the project$/, function(callback) {
        callback.pending();
    });

    this.Then(/^I can view the project on the main RSR page$/, function(callback) {
        console.log('hello from 5');
        this.spooky.then([{
                url: adminUrl + 'rsr/project/'
            }, function () {
                this.test.assertEquals(this.getCurrentUrl(),url,"Currently on: "+this.getCurrentUrl()+" Expected: "+ url);
            }]
        );

        this.spooky.run();
        //callback();
    });
};