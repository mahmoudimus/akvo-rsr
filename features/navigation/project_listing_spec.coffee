#run from features dir folder with mocha navigation/project_list_spec.coffee -R spec -r mocha-cakes --compilers coffee:coffee-script

require 'mocha-cakes'
steps = require './project_listing_steps'

Feature "Project listing",
  "As an RSR user",
  "I would like to view a list of all the projects",
  "So that I can view various projects details", ->

    Scenario "Full project listing", ->
      When "I visit rsr.akvo.org", ->
      	steps.visit 'http://rsr.test.akvo.org'
      Then "I should see a list of all the projects in RSR", ->
      	return