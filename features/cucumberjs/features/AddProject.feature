Feature: Adding projects
	In order to bring my development aid project online and share progress with interested parties
	As a member/owner of the project
	I want to be able to add my project to Akvo RSR

	# Scenario: Set up a TestRail run for these tests
	# 	Given I create a new Add Project TestRail run

	Scenario: Add a project as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I create a new project
		  	And I publish the project
		 Then I can view the project on the main RSR page

	Scenario: Add a project without a title as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "title"
		Then I get an error

	Scenario: Add a project without a subtitle as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "subtitle"
		Then I get an error

	Scenario: Add a project without a project plan summary as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "project plan summary"
		Then I get an error

	Scenario: Add a project without background information as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "background"
		Then I get an error

	Scenario: Add a project without a current status description as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "current status"
		Then I get an error

	Scenario: Add a project without a sustainability description as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "sustainability"
		Then I get an error

	Scenario: Add a project without a goals overview as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter anything for "goals overview"
		Then I get an error