Feature: Interacting with RSR through a partner site
	In order for projects to be interacted with outside the Akvo website
	As a partner site user
	I want to be able to have most of the functionality available on the main RSR page

	Scenario: View a test project for my organisation on a partner site
		Given I have created an RSR test project associated with my organisation
		When I visit my Akvo partner site
		Then I can see this project listed

	Scenario: Log in to Akvo RSR through a partner site
		Given I have an Akvo RSR account
		When I visit a partner site
		Then I can log in to Akvo RSR

	Scenario: Register for Akvo RSR through a partner site
		Given I do not have an RSR account
		When I visit a partner site
		Then I can register for a user account

	Scenario: Add an update for a project from a partner site
		Given I am logged in viewing a test project page on my partner site
		When I click "add update"
			And I fill out a project update
			And I click "add update"
		Then the update should appear on the project page

	Scenario: Add an update for a project without a title from a partner site
		Given I am logged in viewing a test project page on my partner site
		When I click "add update"
			And I fill out a project update
			But I do not enter a title
			And I click "add update"
		Then I get an error

	Scenario: Add an update for a project with an invalid video URL from a partner site
		Given I am logged in viewing a test project page on my partner site
		When I click "add update"
			And I fill out a project update
			But I do not enter a valid video URL
			And I click "add update"
		Then I get an error

	Scenario: Add an update with a photo for a project from a partner site
		Given I am logged in viewing a test project page on my partner site
		When I click "add update"
			And I fill out a project update with a photo
			And I click "add update"
		Then the update and image should appear on the project page

	Scenario: Add an update with a YouTube video for a project from a partner site
		Given I am logged in viewing a test project page on my partner site
		When I click "add update"
			And I fill out a project update with a video
			And I click "add update"
		Then the update and video should appear on the project page

	# Perhaps move this in to separate file if other non update related fucntionality for project page comes along
	Scenario: Add a comment to a project page as a RSR user
		Given I am logged in viewing a test project page on RSR
		When I click "Add comment" or "Add first comment"
			And I fill out a comment
			And I click "Add comment"
		Then my comment appears on the test project page