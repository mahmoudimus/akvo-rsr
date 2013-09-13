module.exports = function () {
    this.World = require('../support/world.js').World;

    function go(url, callback) {
        this.spooky.thenOpen(url);
        callback();
    }

    this.Given('I go to "$url"', go);

    this.Then('I should be on "$url"', function shouldBeOn(url, callback) {
        this.spooky.then([{
            url: url
        }, function () {
            this.echo(this.getCurrentUrl());
            this.test.assertUrlMatch(new RegExp(url));
        }]);
        callback();
    });
};