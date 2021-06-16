import time
import os
import random
import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from deliveries.models import Delivery, Route, Token
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select

def test_order(lst):
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    return True

class RouteStopPagesTests(StaticLiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

		self.names = ['Mark', 'Melon', 'Nelly', 'Harvey', 'Susu']
		stops = [1, 2, 3, 2, 1]
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

		test_route = Route.objects.get(driver = 'Lou')
		self.test_token = test_route.token_set.first()

	def tearDown(self):
		self.browser.quit()

	def check_stop_list(self):
		stops = self.browser.find_elements_by_class_name('stop-num')

		self.assertIn('1', [stop.text for stop in stops])
		self.assertIn('2', [stop.text for stop in stops])

		nums = [int(stop.text) for stop in stops]
		self.assertTrue(test_order(nums))

	def test_stop_view_success(self):
		"""
		The stop view will display basic stop information, allow
		drivers to mark the stop as delivered or failed, and allow the
		driver to add comments.
		"""

		token = self.test_token

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
		token = self.test_token
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
		token = self.test_token
		stop_2_url = f'{self.live_server_url}/{token.value}/2'

		self.browser.get(stop_2_url)
		stop_num = self.browser.find_element_by_id('stop-num')
		self.assertIn(stop_num.text, ['Stop 2'])

		stop_3_url = f'{self.live_server_url}/{token.value}/3'
		self.browser.get(stop_3_url)
		stop_num = self.browser.find_element_by_id('stop-num')
		self.assertIn(stop_num.text, ['Stop 3'])

	def test_click_back_to_route(self):
		token = self.test_token
		url = f'{self.live_server_url}/{token.value}/1'
		self.browser.get(url)
		link = self.browser.find_element_by_link_text('All Deliveries')
		link.click()

		time.sleep(0.5)

		#ordered list test
		self.check_stop_list()
	
	def test_view_route(self):
		token = self.test_token
		url = f'{self.live_server_url}/{token.value}'
		self.browser.get(url)

		date = self.browser.find_element_by_id('date')
		test_date = datetime.date.today().strftime('%B %-d, %Y')
		self.assertIn(date.text, [str(test_date)])

		driver = self.browser.find_element_by_id('driver-name')
		self.assertIn(driver.text, self.drivers)

		self.check_stop_list()

		#test click through to stop
		link = self.browser.find_element_by_link_text('1')
		link.click()
		
		time.sleep(0.5)

		contact = self.browser.find_element_by_id('main-contact')
		self.assertIn(contact.text, ['Mark'])

	def test_stop_order(self):
		token = self.test_token
		url = f'{self.live_server_url}/{token.value}'
		self.browser.get(url)

		self.check_stop_list()

class RouteUploadTest(StaticLiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def check_stop_list(self):
		stops = self.browser.find_elements_by_class_name('stop-num')

		self.assertIn('1', [stop.text for stop in stops])
		self.assertIn('2', [stop.text for stop in stops])

		nums = [int(stop.text) for stop in stops]
		self.assertTrue(test_order(nums))

	def test_csv_upload(self):
		#Put up the upload page at home. This will be password 
		#protected later.

		self.browser.get(self.live_server_url)
		
		#selecting the correct date
		test_date = '2021-05-03'

		date_box = self.browser.find_element_by_id('id_date')
		date_box.send_keys(test_date)

		#inputting the file to be uploaded
		uploader = self.browser.find_element_by_id('upload-csv')
		csv_path = os.path.join(settings.BASE_DIR, 'functional_tests', 'test.csv')
		
		uploader.send_keys(csv_path)
		button = self.browser.find_element_by_id('upload')
		button.click()

		time.sleep(0.5)

		success = self.browser.find_element_by_id('success-message')
		self.assertIn(success.text, ['CSV successfully uploaded'])

		time.sleep(0.5)

		route = Route.objects.first()
		token = Token.objects.create(route=route)

		route_url = f'{self.live_server_url}/{token.value}'
		self.browser.get(route_url)
		self.check_stop_list()

		test_date = datetime.date.fromisoformat(test_date)
		date = self.browser.find_element_by_id('date')
		self.assertIn(date.text, [test_date.strftime('%B %-d, %Y')])

class RouteAssignmentTest(StaticLiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		

	def tearDown(self):
		self.browser.quit()

	def test_route_assignment(self):
		pass

class AllRouteViewTest(StaticLiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		date = '2021-06-21'
		self.drivers = ['Harvey', 'Susu', 'Kristyn', 'Penelope']
		routes = [Route(driver=driver, date=date) for driver in self.drivers]
		Route.objects.create(routes)

	def tearDown(self):
		self.browser.quit()

	def test_all_route_view(self):
		self.browser.get(f'{self.live_server_url}/routes')

		names = self.browser.find_elements_by_class_name('driver-name')
		names = [driver.text for driver in names]

		for name in names:
			self.assertIn(name, self.drivers)
