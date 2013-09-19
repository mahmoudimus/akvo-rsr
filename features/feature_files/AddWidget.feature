Feature: Adding widgets
	In order to display information about an RSR project on my own site
	As an interested party with their own website
	I want to be able to create widgets with project information	

	#TODO: Add subset of html for widget which should be verified

	Scenario Outline: Adding widgets with RSR project information
		Given I am viewing a test project page on RSR
		When I click "Get a widget"
			And I choose a <Widget Name> widget
			And I fill out the embed URL & proceed
		Then I should be able to view correct HTML for the widget
			And when I click "Done" I am returned to the test project page

	  Examples:
	    | Widget Name																				|
	    | "Project widget with donation link (170 pixels wide by 840 pixels high)"  				|
	    | "Cobranded narrow project widget with Donation link (170 pixels wide by 911 pixels high)" |
	    | "Cobranded short project widget with Donation link (170 pixels wide by 627 pixels high)"  |
	    | "Cobranded banner widget (468 pixels wide by 234 pixels high)"  							|
	    | "Cobranded leader widget (728 pixels wide by 207 pixels high)"  							|
	    | "Project widget with Donation link (202 pixels wide by 840 pixels high)"  				|
	    | "Project widget with updates (202 pixels wide by 900 pixels high)"  						|
	    | "Project with Donation Link (202 pixels wide by 570 pixels high)"  						|
	    | "Small project (170 pixels wide by 312 pixels high)"  									|
	    