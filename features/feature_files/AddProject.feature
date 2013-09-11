Feature: Adding projects
	In order to bring my development aid project online and share progress with interested parties
	As a member/owner of the project
	I want to be able to add my project to Akvo RSR

	# TODO: Need to provide a definition somewhere for re-usable steps such as "I fill out new project details"

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
			But I do not enter a title
			And I click the save button
		Then I get an error

	Scenario: Add a project without a subtitle as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter a subtitle
			And I click the save button
		Then I get an error

	Scenario: Add a project without a project plan summary as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter a project plan summary
			And I click the save button
		Then I get an error

	Scenario: Add a project without background information as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter background information
			And I click the save button
		Then I get an error

	Scenario: Add a project without a current status description as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter a current status description
			And I click the save button
		Then I get an error

	Scenario: Add a project without a sustainability description as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter a sustainability description
			And I click the save button
		Then I get an error

	Scenario: Add a project without a goals overview as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter a goals overview
			And I click the save button
		Then I get an error

	Scenario: Add a project without entering project partners as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter project partners
			And I click the save button
		Then I get an error

	Scenario: Add a project without a field partner as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter a field partner
			And I click the save button
		Then I get an error

	Scenario: Add a project without a sponsor or funding partner as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter a sponsor of funding partner
			And I click the save button
		Then I get an error

	Scenario: Add a project without a partner type which doesnt match the partner as an Administrator
		Given I am logged in to RSR Admin
		When I click "add a project"
			And I fill out new project details
			But I do not enter a partner type which matches the partner
			And I click the save button
		Then I get an error

	# Create new project:
	# Enter a project title (<= 45 chars)
	# Enter a subtitle (<=75 chars)
	# Select a project status
	# Select a project language
	# Enter a start date
	# Enter a completion date
	# Enter a project plan summary (<= 400 chars)
	# Enter background information (<= 1000 chars)
	# Enter a current status descirption (<= 600 chars)
	# Enter project plan
	# Enter sustainability description
	# Enter goals overview (<= 600 chars)
	# Enter goals
	# Upload a project photo
	# Enter a photo caption (<=50 chars)
	# Enter a photo credit (<= 50 chars)
	# Add a project location
	# Select currency
	# Enter budget items and amounts
	# Select project categories and focus areas
	# Add project partners and partner details
	# Enter any additional information
	# Add links
	