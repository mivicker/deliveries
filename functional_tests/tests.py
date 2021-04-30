import time
import os
import random
import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from deliveries.models import Delivery, Route, Token

class FirstTest(StaticLiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

		self.names = ['Mark', 'Melon', 'Nelly', 'Harvey', 'Susu']
		stops = [1, 2, 3, 1, 2]
		route_nums = [0, 0, 0, 1, 1]
		self.drivers = ['Lou', 'Kerry']

		for driver, route in zip(self.drivers, set(route_nums)):
			route = Route.objects.create(driver=driver)
			token = Token.objects.create(route=route)

		all_routes = Route.objects.all()
		routes = [all_routes[i] for i in route_nums]

		for name, stop, route in zip(self.names, stops, routes):
			Delivery.objects.create(
				route = route,
				stop_num = stop,
				main_contact = name,
				status = 1
				)

	def tearDown(self):
		self.browser.quit()

	def test_stop_view_success(self):
		"""
		The stop view will display basic stop information, allow
		drivers to mark the stop as delivered or failed, and allow the
		driver to add comments.
		"""

		token = Token.objects.first()

		stop_1_url = f'{self.live_server_url}/{token.value}/1'
		self.browser.get(stop_1_url)
		
		#check for stop number
		stop_num = self.browser.find_element_by_id('stop-num')
		self.assertRegex(stop_num.text, 'Stop [0-9]+')

		#check for name
		main_contact = self.browser.find_element_by_id('main-contact')
		self.assertIn(main_contact.text, ['Mark'])

		#Check that ths stop is marked as not complete
		delivered = self.browser.find_element_by_id('delivered')
		self.assertIn(delivered.text, ['Not delivered'])

		#Mark the stop as delivered
		delivered_button = self.browser.find_element_by_id('mark-complete')
		delivered_button.click()

		time.sleep(0.5)

		#Check if the stop is delivered.
		delivered = self.browser.find_element_by_id('delivered')
		self.assertIn(delivered.text, ['Delivered'])

	def test_stop_view_failed(self):
		"""
		The stop view will display basic stop information, allow
		drivers to mark the stop as delivered or failed, and allow the
		driver to add comments.
		"""
		token = Token.objects.first()
		stop_1_url = f'{self.live_server_url}/{token.value}/1'
		self.browser.get(stop_1_url)

		#check for stop number
		stop_num = self.browser.find_element_by_id('stop-num')
		self.assertRegex(stop_num.text, 'Stop [0-9]+')

		#check for name
		main_contact = self.browser.find_element_by_id('main-contact')
		self.assertIn(main_contact.text, ['Mark'])

		#Check that ths stop is marked as not complete
		delivered = self.browser.find_element_by_id('delivered')
		self.assertIn(delivered.text, ['Not delivered'])

		#Mark the stop as delivered
		delivered_button = self.browser.find_element_by_id('mark-failed')
		delivered_button.click()

		time.sleep(0.5)

		#Check if the stop is delivered.
		delivered = self.browser.find_element_by_id('delivered')
		self.assertIn(delivered.text, ['Failed'])

	def test_different_stops(self):
		token = Token.objects.first()
		stop_2_url = f'{self.live_server_url}/{token.value}/2'

		self.browser.get(stop_2_url)
		stop_num = self.browser.find_element_by_id('stop-num')
		self.assertIn(stop_num.text, ['Stop 2'])

		stop_3_url = f'{self.live_server_url}/{token.value}/3'
		self.browser.get(stop_3_url)
		stop_num = self.browser.find_element_by_id('stop-num')
		self.assertIn(stop_num.text, ['Stop 3'])

	def test_click_back_to_route(self):
		token = Token.objects.first()
		url = f'{self.live_server_url}/{token.value}/1'
		self.browser.get(url)
		self.browser.find_element_by_link_text('All Deliveries')

		time.sleep(0.5)

		stops = self.browser.find_elements_by_class_name('stop-num')

		self.assertIn('1', [stop.text for stop in stops])
		self.assertIn('2', [stop.text for stop in stops])
	
	def test_view_route(self):
		token = Token.objects.first()
		url = f'{self.live_server_url}/{token.value}'
		self.browser.get(url)

		date = self.browser.find_element_by_id('date')
		test_date = datetime.date.today().strftime('%B %d, %Y')
		self.assertIn(date.text, [str(test_date)])

		driver = self.browser.find_element_by_id('driver-name')
		self.assertIn(driver.text, self.drivers)

		stops = self.browser.find_elements_by_class_name('stop-num')

		self.assertIn('1', [stop.text for stop in stops])
		self.assertIn('2', [stop.text for stop in stops])

		#test click through to stop
		link = self.browser.find_element_by_link_text('1')
		link.click()
		
		time.sleep(0.5)

		contact = self.browser.find_element_by_id('main-contact')
		self.assertIn(contact.text, ['Mark'])

	#def test_inactive_route(self):
	#	self.fail("Test an inactive route!")

	#def test_out_of_order_tokens(self):
	#	pass

	#def test_create_routes(self):
	#	self.fail("Test creating a route!")
	#	self.fail("Test that the stops are ordering correctly.")