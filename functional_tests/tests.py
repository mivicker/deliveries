import time
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from deliveries.models import Delivery

class FirstTest(StaticLiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		Delivery.objects.create(
			stop_num = 1,
			main_contact = 'Mark',
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
		self.browser.get(self.live_server_url)
		
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
		self.browser.get(self.live_server_url)
		
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

	def test_second_stop(self):
		self.browser.get(self.live_server_url)
		stop_num = self.browser.find_element_by_id('stop-num')
		self.assertIn(stop_num.text, ['Stop 2'])