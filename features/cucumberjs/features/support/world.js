var util = require('util');

try {
    var Spooky = require('spooky');
} catch (e) {
    var Spooky = require(__dirname+'/../../../../lib/spooky');
}

var World = function World(callback) {
    var spooky;
    var world = this;

    try {
        spooky = world.spooky = new Spooky({
            casper: {
                verbose: true,
                logLevel: 'debug'
            }
        }, onCreated);
    } catch (e) {
        console.dir(e);
        console.trace('Spooky.listen failed');
    }

    spooky.debug = true;

    spooky.errors = [];
    spooky.on('error', function (error) {
        error = error.data ? error.data : error;
        spooky.errors.push(error);
        if (spooky.debug) {
            console.error('spooky error', util.inspect(error));
        }
    });

    spooky.console = [];
    spooky.on('console', function (line) {
        spooky.console.push(line);
        if (spooky.debug) {
            console.log(line);
        }
    });

    function onCreated(error, response) {
        if (error) {
            console.dir(error);
            throw new Error('Failed to initialize context.spooky: ' +
                error.code + ' - '  + error.message);
        }

        callback(world);
    }
};
module.exports.World = World;
