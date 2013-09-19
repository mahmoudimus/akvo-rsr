Feature: Adding project updates
	In order for information to be distributed via RSR about how a project is progressing
	As a member of the project
	I want to be able to add project updates for projects I have created

	# Feature assumes that one or more test projects have been created in RSR to test against
	# TODO: Need to provide a definition somewhere for re-usable steps such as "I fillout a project update"

	Scenario: Add an update as a project administrator
		Given I am logged in to RSR Admin
		When I click "add a project update"
			And I choose a project
			And I select a user
			And I fill out a project update
			And I click save
		Then the update should appear on the project page

	Scenario: Add an update without selecting a project as a project administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I select a user
			And I fill out a project update
			But I do not choose a project
			And I click save
		Then I get an error

	Scenario: Add an update without selecting a user as a project administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I choose a project
			And I fill out a project update
			But I do not select a user
			And I click save
		Then I get an error

	Scenario: Add an update without entering a title as a project administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I choose a project
			And I select a user
			And I fill out a project update
			But I do not enter a title
			And I click save
		Then I get an error

	Scenario: Add an update without entering a photo location as a project administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I choose a project
			And I select a user
			And I fill out a project update
			But I do not add a photo location
			And I click save
		Then I get an error

	Scenario: Add an update without an invalid video URL as a project administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I choose a project
			And I select a user
			And I fill out a project update
			But I do not enter a valid video URL
			And I click save
		Then I get an error

	Scenario: Add an update as an RSR user
		Given I am viewing a test project page on RSR
		When I click "add update"
			And I log in
			And I fill out a project update
			And I click "add update"
		Then the update should appear on the project page

	Scenario: Add an update without a title as an RSR User
		Given I am viewing a test project page on RSR
		When I click "add update"
			And I log in
			And I fill out a project update
			But I do not enter a title
			And I click "add update"
		Then I get an error

	Scenario: Add an update with an invalid video URL as an RSR User
		Given I am viewing a test project page on RSR
		When I click "add update"
			And I log in
			And I fill out a project update
			But I do not enter a valid video URL
			And I click "add update"
		Then I get an error

	Scenario: Add a comment to a project page as an RSR user
		Given I am viewing a test project page on RSR
			And I am signed in
		When I click "Add comment" or "Add first comment"
			And I fill out a comment
			And I click "Add comment"
		Then my comment appears on the test project page

	# Project update:
	# If admin -> Select project MANDATORY: ADMIN
	# If admin -> Select user MANDATORY: ADMIN
	# Enter title (<= 50 chars) MANDATORY: ADMIN + USERS
	# Enter update text
	# Select language
	# Add photo
	# Add photo caption (<=75 chars)
	# Add photo credit (<=25 chars)
	# If admin -> Select photo location MANDATORY: ADMIN
	# Add video URL
	# Add video caption (<=75 chars)
	# Add video credit (<=25 chars)
	# Select update method/text placement


