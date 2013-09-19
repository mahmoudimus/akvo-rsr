module.exports = function () {
    this.World = require('../support/world.js').World;
    this.Chai = require('../../../node_modules/chai');
   
    var adminUrl = 'http://rsr.test.akvo-ops.org/admin/';
    var testProjectName = 'testProject9';

    this.Given('I am logged in to RSR Admin', function(callback){
        this.spooky.open(adminUrl);

        this.spooky.then(function(){ 
            this.fill('form#login-form', 
                {
                    'username' : 'AutomatedTestUser',
                    'password' : 'testpassword'
                }, true);
        });

        callback();
    });

    this.When('I click "add a project"', function(callback) {
       // There is presumably a better way of doing this - <a href="/admin/rsr/project/add/" class="addlink">Add</a>
       this.spooky.then(function(){
            this.click('a[href="/admin/rsr/project/add/"]');
        })
        
        callback();
    });

    this.When('I fill out new project details', function(callback) {

        this.spooky.then([
            {
                testProjectName : testProjectName
            }, function(){
                this.fill('form#project_form', 
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
            }
        ]);

        this.spooky.then(function(){
            this.click('input[name="_save"]');
        });

       callback();
    });

    this.When('I publish the project', function(callback) {
        //Another way of doing this is by just appending the project ID to the below URLS

        this.spooky.then(function(){
            this.click('a[href="/admin/rsr/"]');
        });

        //<a href="/admin/rsr/publishingstatus/">Publishing statuses</a>
        this.spooky.then(function(){
            this.click('a[href="/admin/rsr/publishingstatus/"]');
        });

        //<a href="1102/">test</a>
        this.spooky.then([
            {
                testProjectName : testProjectName
            }, function(){
                this.clickLabel(testProjectName, 'a');
            }
        ]);

        this.spooky.then(function(){
            this.fill('form#publishingstatus_form', 
                {
                    'status' : 'published'
                }, false);
        })

        this.spooky.then(function(){
            this.click('input[name="_save"]');
        })

        callback();
    });

    this.Then('I can view the project on the main RSR page', function(callback) {
        this.spooky.then(function(){
            this.click('a[href="/admin/rsr/"]');
        });

        this.spooky.then(function(){
            this.click('a[href="/admin/rsr/project/"]');
        });

        this.spooky.then([
            {
                testProjectName : testProjectName
            }, function () {
                this.fill('form#changelist-search', 
                {
                    'q' : testProjectName
                }, true);
            }
        ]);

        this.spooky.then([
            {
                renderName: 'test.png',
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
};