var _ = require('underscore');
var util = require('util');
var Spooky = require('spooky');

function setup (context, done) {
    var spooky;

    try {
        spooky = context.spooky = new Spooky(context.config, onCreated);
    } catch (e) {
        console.log(util.inspect(e, false, 3));
        console.log(e.stack);
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
            console.trace(error);
            console.dir(error);
            throw new Error('Failed to initialize context.spooky: ' +
                error.code + ' - '  + error.message);
        }

        done();
    }
}

module.exports.FIXTURE_URL = 'http://localhost:8080';

module.exports.before = function (context) {
    context.config = _.defaults(context.config || {}, {
        child: {
            port: 8081,
            script: './node_modules/spooky/lib/bootstrap.js',
            spooky_lib: './node_modules/spooky/',
            transport: 'stdio'
        },
        casper: {
            verbose: true,
            logLevel: 'debug'
        },
        PageSettings: {
            javascriptEnabled: true,
            loadImages: true,
            laodPlugins: false,     
            userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
        }
    });

    return function (done) {
        setup(context, done);
    };
};

module.exports.after = function (context) {
    return function (done) {
        context.spooky.removeAllListeners();
        context.spooky.destroy();
        done();
    };
};