Feature: Adding projects
	In order to bring my development aid project online and share progress with interested parties
	As a member/owner of the project
	I want to be able to add my project to Akvo RSR

	Scenario: Set up a TestRail run for these tests
		Given I create a new Add Project TestRail run

	Scenario: Add a project as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details 
			And I click the save button
		 	And I publish the project
		Then I can view the project on the main RSR page

	Scenario: Add a project without a title as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "title"
			And I click the save button
		Then I get an error

	Scenario: Add a project without a subtitle as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "subtitle"
			And I click the save button
		Then I get an error

	Scenario: Add a project without a project plan summary as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "project plan summary"
			And I click the save button
		Then I get an error

	Scenario: Add a project without background information as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "background"
			And I click the save button
		Then I get an error

	Scenario: Add a project without a current status description as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "current status"
			And I click the save button
		Then I get an error

	Scenario: Add a project without a sustainability description as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "sustainability"
			And I click the save button
		Then I get an error

	Scenario: Add a project without a goals overview as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "goals overview"
			And I click the save button
		Then I get an error