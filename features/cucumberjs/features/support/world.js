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
    
        console.log('spooky initialised');

        spooky.on('error', function(e) {
            console.error('spooky error', util.inspect(e));
        });

        spooky.on('console', function (line) {
            console.log(line);
        });

        callback(world);
       }); 
};
module.exports.World = World;
