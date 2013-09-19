module.exports = function () {
    this.Before(function (callback) {
        this.spooky.start();
        callback();
    });

    this.After(function (callback) {
    	this.spooky.wait(1000, function() {
    		this.echo("I've waited for a second.");
		});
        this.spooky.destroy();
        callback();
    });
};
