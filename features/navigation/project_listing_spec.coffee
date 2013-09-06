require 'mocha-cakes'

Feature "Project listing",
  "As an RSR user",
  "I would like to view a list of all the projects",
  "So that I can view various projects details", ->

    Scenario "Full project listing", ->
      When "I visit rsr.akvo.org", ->
      Then "I should see a list of all the projects in RSR"
