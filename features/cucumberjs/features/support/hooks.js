module.exports = function () {
    this.Before(function (callback) {
    	console.log("Before hook: starting spooky");
        this.spooky.start();
        callback();
    });

    this.After(function (callback) {
    	console.log("After hook: destorying spooky")
        this.spooky.destroy();
        callback();
    });
};
