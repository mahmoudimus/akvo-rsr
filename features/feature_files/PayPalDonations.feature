Feature: Donating to projects via PayPal
	In order for projects to receive funding through RSR
	As an RSR user
	I want to be able to donate to selected projects using PayPal

	# Feature assumes that a selection of test projects have been set up in RSR - this should be created as a BACKGROUND step
	# There is so much repetition on some of these validation checks - perhaps a better way of doing it?

	Scenario: Donate to a project as a PayPal user
		Given I am on a project page for a test project
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			And I log in to a pay pal account to complete my donation
		Then I receive an invoice number notifying me that the donation is complete
			And I can return to the project page
			And the project totals update accordingly

	Scenario: Donate to a project but let the transaction time out
		Given I am on a project page for a test project
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			And I log in to a pay pal account to complete my donation
			But I let the transaction time out
		Then the project funding totals remain unchanged

	Scenario: Complete funding of project with one donation as a PayPal user
		Given I am on a project page for a test project
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			And I enter the full amount required to complete funding
			And I log in to a PayPal account to complete my donation
		Then I receive an invoice number notifying me that the donation is complete
			And I can return to the project page
			And the project funding shows as complete

	Scenario: Donate to a project as a PayPal user and complete 100% funding
		Given I am on a project page for a test project which already has some donations # Should re-use project from first donation test
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			And I enter the remaining amount required to complete funding
			And I log in to a PayPal account to complete my donation
		Then I receive an invoice number notifying me that the donation is complete
			And I can return to the project page
			And the project funding shows as complete

	Scenario: Donate to a project as a PayPal user and over-fund it # System allows for donations over funding by 1%
		Given I am on a project page for a test project 
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			And I enter the enter an amount 1% greater than the funding total
			And I log in to a PayPal account to complete my donation
		Then I receive an invoice number notifying me that the donation is complete
			And I can return to the project page
			And the project funding shows as complete
			And there is some indication the project is over-funded 

	# Amount field validation tests
	Scenario: Donate to a project without entering an amount
		Given I am on a project page for a test project
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			But I do not enter a donation amount
		Then I get an error

	Scenario: Donate more than needed to a project # Spec mentions concept of "over-funding" over donating by more than 2% - more details needed
		Given I am on a project page for a test project
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			But I enter a donation value greater than the project requires
		Then I get an error

	Scenario: Donate a negative amount to a project
		Given I am on a project page for a test project
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			But I enter a negative donation amount
		Then I get an error

	Scenario: Donate a decimal amount to a project
		Given I am on a project page for a test project
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			But I enter a decimal value for the donation amount
 		Then I get an error

	# Remaining field validation tests
	Scenario: Donate to a project without entering a name
		Given I am on a project page for a test project
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			But I do not enter my name
		Then I get an error

	Scenario: Donate to a project without entering an email address
		Given I am on a project page for a test project
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			But I do not enter an email address
		Then I get an error

	Scenario: Donate to a project without confirming my email address
		Given I am on a project page for a test project
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			But I do not confirm my email address
		Then I get an error

	Scenario: Donate to a project without specifying matching email addresses
		Given I am on a project page for a test project
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			But the email addresses I enter do not match
		Then I get an error

	Scenario: Make an anonymous donation to a project
		Given I am on a project page for a test project
		When I click on the "Donate" link
			And I select "Use PayPal"
			And I fill out my details
			And I uncheck the "List name next to donation" box
		Then I receive an invoice number notifying me that the donation is complete
			And I can return to the project page
			And the project totals update accordingly
			And my name is not listed in current funders

	# Scenario assumes that a donation has been made against a specified project
	Scenario: Review pending invoices as an RSR Admin
		Given I am logged in to RSR Admin
		When A donation against a certain project is made
		Then I can view the invoice
			And the invoice has a status of "pending"
