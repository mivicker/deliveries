import time
import os
import random
from urllib.parse import urljoin
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from deliveries.models import Delivery, Route

class FirstTest(StaticLiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.names = ['Mark', 'Harvey', 'Susu']

		names = ['Mark', 'Harvey', 'Susu']
		stops = [1, 2, 1]
		route_nums = [0, 0, 1]
		drivers = ['Lou', 'Kerry']

		for driver, route in zip(drivers, set(route_nums)):
			Route.objects.create(driver = driver)
		
		all_routes = Route.objects.all()
		routes = [all_routes[i] for i in route_nums]

		for name, stop, route in zip(names, stops, routes):
			Delivery.objects.create(
				route = route,
				stop_num = stop,
				main_contact = name,
				status = 1
				)

	def tearDown(self):
		self.browser.quit()

	def test_home_page(self):
		self.browser.get(self.live_server_url)
		contacts = self.browser.find_elements_by_class_name('main-contact')

		for name in self.names:
			self.assertIn(name, [contact.text for contact in contacts])

	def test_stop_view_success(self):
		"""
		The stop view will display basic stop information, allow
		drivers to mark the stop as delivered or failed, and allow the
		driver to add comments.
		"""
		stop_1_url = urljoin(self.live_server_url, '1')
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
		stop_1_url = urljoin(self.live_server_url, '1')
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

	def test_stop_nums(self):
		stop_2_url = urljoin(self.live_server_url, '2')

		self.browser.get(stop_2_url)
		stop_num = self.browser.find_element_by_id('stop-num')
		self.assertIn(stop_num.text, ['Stop 2'])

		stop_3_url = urljoin(self.live_server_url, '3')
		self.browser.get(stop_3_url)
		stop_num = self.browser.find_element_by_id('stop-num')
		self.assertIn(stop_num.text, ['Stop 3'])

	def test_view_route(self):
		token = Token.objects.first()
		url = urljoin(self.live_server_url, token.value)
		self.browser.get(url)

		stops = self.browser.find_elements_by_class_name('stop-num')

		self.assertIn(2, [stop.text for stop in stops])
