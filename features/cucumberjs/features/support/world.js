var util = require('util');

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

    //Helper functions
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
};
module.exports.World = World;
