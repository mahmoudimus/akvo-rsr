Feature: RSR Map Views
	In order to get a visual representation of RSR projects and organisations
	As a user visiting the site
	I want to be able to view Google Maps with these locations

	Scenario: View map of all projects
		Given I am on the Akvo RSR home page (rsr.akvo.org)
		When I click on "map of all projects"
		Then I see a map with all the project locations

	Scenario: Opening project summaries from map
		Given I am on the all projects map page (rsr.akvo.org/maps/projects/all)
		When I click on a project pinpoint
		Then the project summary should open
			And the link in the summmary should connect to the correct project page

	Scenario: View map of all organisations
		Given I am on the Akvo RSR home page (rsr.akvo.org)
		When I click on the organistion map link
		Then I see a map with all the organisation locations

	Scenario: Opening organisation summaries from map
		Given I am on the all organisations map page (rsr.akvo.org/maps/organisations/all)
		When I click on an organisation pinpoint
		Then the organisation summary should open
			And the link in the summary should connect to the correct organisation page

	Scenario: View individual project location on map
		Given I am on the Akvo RSR homepage (rsr.akvo.org)
		When I select a project from the list
		Then the matching project page should open
			And the map should show the project location