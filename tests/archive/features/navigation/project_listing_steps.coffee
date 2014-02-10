root = exports ? this

util = require 'util'
chai = require 'chai'

expect = chai.expect
should = chai.should 

root.visit = (url) ->
	context = {}
	hooks = require './util/hooks'
	before hooks.before(context)
	
	context.spooky.start()
	context.spooky.open url
	context.spooky.then ->
		@echo @getCurrentUrl
	context.spooky.run()
	
	after hooks.after(context)
 
