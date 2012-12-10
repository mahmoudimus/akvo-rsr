# -*- coding: utf-8 -*-

from lettuce import step, world, before
from time import sleep


@before.each_feature
def log_in_to_paypal_test_environment(feature):
#    '''Figure out the URL to the project'''
#    world.browser.visit('http://%s' % world.SITE_UNDER_TEST)
#    element = world.browser.find_link_by_partial_href('donate').first
#    world.project_URL = '/'.join(element['href'].split('/')[:-2]) + '/'
    '''Log in to paypal to ensure the environment is active'''
    world.browser.visit('https://developer.paypal.com/')
    world.browser.fill('login_email', world.PAYPAL_MASTER_USER)
    world.browser.fill('login_password', world.PAYPAL_MASTER_PASSWORD)
    world.browser.check('cb_auto_login')
    world.browser.find_by_name('submit').first.click()

@before.each_scenario
def navigate_to_homepage(scenario):
    world.browser.visit('http://%s/rsr/projects/' % world.SITE_UNDER_TEST)

@step(u'When I go to project listing page')
def when_i_go_to_project_listing_page(step):
    "Each scenario starts by navigating to the project main page"
    world.browser.find_link_by_href('href="/rsr/projects/all/"')

@step(u'When I find the first project still to be funded in €')
def when_i_find_the_first_project_still_to_be_funded_in(step):
    project_table = world.browser.find_by_tag('tbody').first
    project_rows = project_table.find_by_tag('tr')
    count = 0
    while count < len(project_rows):
        if 'Donate' in project_rows[count].text and u"€" in project_rows[count].text:
            element = project_rows[count].find_by_css('a').last
            world.project_needing_euro_URL = '/'.join(element['href'].split('/')[:-2]) + '/'
            break
        count = count + 1

    row_text = project_rows[count].text.split('\n')

    last_word = len(row_text)-1

    world.percentage_raised_all_page = int(''.join([c for c in row_text[last_word-1] if c in '1234567890'])) 
    world.total_budget_all_page = int(''.join([c for c in row_text[last_word-2] if c in '1234567890'])) 
    world.browser.visit(world.project_needing_euro_URL)

@step(u'When I note how much has been raised and how much is still needed')
def when_i_note_how_much_has_been_raised_and_how_much_is_still_needed(step):
    element = world.browser.find_by_css('.fundingbox-table').first
    raised_text, still_needed_text = element.text.split('\n')
    total_budget_text = world.browser.find_by_css('.fundingbox-table').last.text

    #print "Original text: \n" + total_budget_text
    #raised_text, still_needed_text = element.text.split('\n')
    #print "Captured text: " + raised_text

    world.money_raised = int(raised_text.split(u"€")[-1].strip().replace(",", ""))
    world.money_still_needed = int(still_needed_text.split(u"€")[-1].strip().replace(",", ""))
    world.total_budget = int(total_budget_text.split(u"€")[-1].strip().replace(",", ""))
    #print world.total_budget

@step(u'Then these amounts should agree with those on the project listing page')
def then_these_amounts_should_agree_with_those_on_the_project_listing_page(step):
    assert world.total_budget_all_page == world.total_budget
    assert (world.total_budget - world.money_raised) == world.money_still_needed
    assert world.percentage_raised_all_page == world.money_raised * 100 / world.total_budget

@step(u'When I click on the "([^"]*)" link')
def when_i_click_on_the_group1_link(step, link_name):
    #world.browser.driver.execute_script('window.onbeforeunload = function() {}')
	world.browser.click_link_by_text(link_name)

@step(u'When I click on the link with "([^"]*)" in the URL for the project')
def when_i_click_on_the_link_with_group1_in_the_url_for_the_project(step, link_name):
    world.browser.click_link_by_partial_href(link_name)

@step(u'When I enter "([^"]*)" in the "([^"]*)" field')
def when_i_enter_group1_in_the_group2_field(step, input_value, field_name):
    world.browser.fill(field_name, input_value)

@step(u'When I click on the donate button')
def when_i_click_on_the_donate_button(step):
    world.browser.find_by_name('submit').first.click()

@step(u'When I enter the PayPal test username in the "([^"]*)" field')
def when_i_enter_the_paypal_test_username_in_the_group1_field(step, field_name):
    world.browser.fill(field_name, world.PAYPAL_TEST_USER)

@step(u'When I enter the PayPal test password in the "([^"]*)" field')
def when_i_enter_the_paypal_test_password_in_the_group1_field(step, field_name):
    world.browser.fill(field_name, world.PAYPAL_TEST_USER_PASSWORD)

@step(u'When I click on the PayPal login button')
def when_i_click_on_the_donate_button(step):
    world.browser.find_by_name('login.x').first.click()

@step(u'When I Click on the Continue button')
def when_i_click_on_the_continue_button_continue_x(step):
    world.browser.find_by_name('continue.x').first.click()

@step(u'When I click on the Back to Akvos test store button')
def when_i_click_on_the_back_to_akvo_s_test_store_button_merchant_return_link(step):
    world.browser.find_by_name('merchant_return_link').first.click()
    alert = world.browser.get_alert()
    alert.accept()
    #world.browser.visit(world.project_URL)

@step(u'When I note the new values of how much has been raised and how much is still needed')
def when_i_note_how_much_has_been_raised_and_how_much_is_still_needed(step):
    element = world.browser.find_by_css('.fundingbox-table').first
    raised_text, still_needed_text = element.text.split('\n')
    world.new_money_raised = int(raised_text.split(u"€")[-1].strip().replace(",", ""))
    world.new_money_still_needed = int(still_needed_text.split(u"€")[-1].strip().replace(",", ""))

@step(u'Then I see that the amount raised has been incremented by "([^"]*)" and the amount left to raise decremented by the same amount')
def then_i_see_that_the_amount_raised_has_been_incremented_by_group1_and_the_amount_left_to_raise_decremented_by_the_same_amount(step, amount):
    assert world.new_money_raised == (world.money_raised + int(amount))
    assert world.new_money_still_needed == (world.money_still_needed - int(amount))

@step(u'Then I see this error message "([^"]*)"')
def then_i_see_this_error_message_group1(step, expected_error):
    element = world.browser.find_by_css('.errorlist').first
    errortext = element.find_by_tag('li').first.text
    assert errortext == expected_error

@step(u'When I enter more funds than are needed in the "([^"]*)" field')
def when_i_enter_more_funds_than_are_needed_in_the_group1_field(step, field_name):
    input_value = (world.money_still_needed * 2)
    world.browser.fill(field_name, input_value)

@step(u'When I enter the remaining amount needed in the "([^"]*)" field')
def when_i_enter_the_remaining_amount_needed_in_the_group1_field(step, field_name):
    input_value = world.money_still_needed
    world.browser.fill(field_name, input_value)

@step(u'Then I see that the amount raised and the amount left to raise are unchanged')
def then_i_see_that_the_amount_raised_and_the_amount_left_to_raise_are_unchanged(step):
    assert world.new_money_raised == world.money_raised
    assert world.new_money_still_needed == world.money_still_needed

@step(u'When I return to the euro project requiring funding')
def when_i_return_to_the_euro_project_requiring_funding(step):
    world.browser.visit(world.project_needing_euro_URL)

@step(u'When I wait "([^"]*)" minutes')
def when_i_wait_group1_minutes(step, minutes):
    wait_seconds = float(minutes) * 60
    sleep(wait_seconds)

@step(u'When I take note of the invoice number')
def when_i_take_note_of_the_invoice_number(step):
    world.paypal_invoice_number = world.browser.find_by_css('.donate_details_right').first.text

@step(u'When I log in to RSR admin')
def when_i_log_in_to_rsr_admin(step):
    world.browser.find_link_by_text('Akvo RSR login').first.click()
    world.browser.fill('username', world.AKVO_ADMIN_USER)
    world.browser.fill('password', world.AKVO_ADMIN_PASSWORD)
    world.browser.find_by_xpath('//*[@id="login-form"]/div[4]/input').first.click()

@step(u'Then I see the error message "([^"]*)" each time I leave one of the fields blank')
def then_i_see_the_error_message_group1_each_time_i_leave_one_of_the_fields_blank(step, expected_error):
    world.browser.fill('name', 'Akvo Test')
    world.browser.fill('email', 'test@akvo.org')
    world.browser.fill('email2', 'test@akvo.org')
    world.browser.click_link_by_partial_href('donate_form')
    world.browser.click_link_by_partial_href('donate_form')
    element = world.browser.find_by_css('.errorlist').first
    errortext = element.find_by_tag('li').first.text
    assert errortext == expected_error

    world.browser.fill('amount', '10')
    world.browser.fill('name', '')
    world.browser.fill('email', 'test@akvo.org')
    world.browser.fill('email2', 'test@akvo.org')
    world.browser.click_link_by_partial_href('donate_form')
    element = world.browser.find_by_css('.errorlist').first
    errortext = element.find_by_tag('li').first.text
    assert errortext == expected_error

    world.browser.fill('amount', '10')
    world.browser.fill('name', 'Akvo Test')
    world.browser.fill('email', '')
    world.browser.fill('email2', 'test@akvo.org')
    world.browser.click_link_by_partial_href('donate_form')
    element = world.browser.find_by_css('.errorlist').first
    errortext = element.find_by_tag('li').first.text
    assert errortext == expected_error

    world.browser.fill('amount', '10')
    world.browser.fill('name', 'Akvo Test')
    world.browser.fill('email', 'test@akvo.org')
    world.browser.fill('email2', '')
    world.browser.click_link_by_partial_href('donate_form')
    element = world.browser.find_by_css('.errorlist').first
    errortext = element.find_by_tag('li').first.text
    assert errortext == expected_error

@step(u'When I enter the information to make an anonymous donation')
def when_i_enter_the_information_to_make_an_anonymous_donation(step):
    world.browser.select('country_code', 'IE')
    world.browser.fill('first_name', 'Akvo')
    world.browser.fill('last_name', 'Test')
    world.browser.fill('expdate_month', world.PAYPAL_TEST_VISA_EXP_MONTH)
    world.browser.fill('expdate_year', world.PAYPAL_TEST_VISA_EXP_YEAR)
    world.browser.fill('address1', '180 Akvo central')
    world.browser.fill('city', 'Amsterdam')


@step(u'Then I see that the invoice is present and is in the "([^"]*)" state')
def then_i_see_that_the_invoice_is_present_and_is_in_the_group1_state(step, group1):
    world.browser.click_link_by_text('Invoices')
    world.browser.find_link_by_text(world.paypal_invoice_number).first

@step(u'Then I see the error message <error>')
def then_i_see_the_error_message_error(step):
    assert False, 'This step must be implemented'

    

