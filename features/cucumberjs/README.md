# Akvo RSR CucumberJS Test Suite

This is the starting point for what will hopefully be an expansive CucumberJS test suite which will provide regression coverage for the Akvo RSR application. In order to get up and running there are couple of pernickety steps to get out of the way - this should hopefully be streamlined as we go, there is an issue with a 3rd Party Library at the moment which is the source of the problem. Set up steps as follows:

* Node - this can be installed easily on Mac OSX using "brew install node"
* CasperJs - again this can be easily installed on OSX by using "brew install casperjs --devel"
* CucumberJS - to install this use "npm install -g cucumber" which will give a global installation and allow usage in other projects
* Run "npm install" when in the akvo-rsr/features directory which will install everything contained within the package.json file
* SpookyJS - there is an issue with the latest release of SpookyJS which prevents it from working with the latest CasperJS. I've raised an issue to fix this, but in the mean time I've forked the repo. Navigate to the "akvo-rsr/features/node_modules" directory and remove the "spooky" folder then run the following commands "git clone https://github.com/rumca/SpookyJS.git" and "mv SpookyJS/ spooky". Finally "cd spooky" and "npm install"

Once all the set up is out of the way you can run the current CucumberJS tests by navigating to "akvo-rsr/features/cucumberjs" and running the "cucumber.js" command. Provided something hasn't horrifically broke in the set up procedure then you should be greeted with some test output.

##Urgent areas of focus

* Test reporter format - would be nice to see something like mocha's whereby each step is clearly documented [investigate this](https://github.com/cucumber/cucumber-js/pull/104)
* Script up step files for the feature files found [here](https://github.com/akvo/akvo-rsr/tree/feature/navigation_tests/features/feature_files)
* Find some sort of test runner to incorporate into Team City deployments
* Investigate if it is possible to add the "--post=./postResults.js" into the spooky call somewhere in order to post results to TestRail

##Useful Links

[SpookyJS functionality overview](https://github.com/WaterfallEngineering/SpookyJS/wiki/Introduction)
[CasperJS tester module overview](http://docs.casperjs.org/en/latest/modules/tester.html)
[CucumberJS ]
