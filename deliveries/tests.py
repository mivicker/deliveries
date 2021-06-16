import os
from django.test import TestCase
from django.conf import settings
from .models import Route, Delivery, Token

class TokenTest(TestCase):
	def setUp(self):
		self.route = Route.objects.create(driver="Test")
		self.old_token = Token.objects.create(route=self.route)
		self.new_token = Token.objects.create(route=self.route)

	def test_latest_token(self):
		first_token = self.route.token_set.first().value
		self.assertEqual(first_token, self.new_token.value)
		self.assertNotEqual(first_token, self.old_token.value)

		response = self.client.get(f'/{first_token}')
		self.assertEqual(response.status_code, 200)

	def test_old_token_breaks(self):
		stale_token = self.route.token_set.order_by('created').first()
		response = self.client.get(f'/{stale_token.value}')
		self.assertRedirects(response, '/stale-token/')

class CsvUploadTest(TestCase):
	def setUp(self):
		pass

	def test_upload_script(self):
		csv_path = os.path.join(
			settings.BASE_DIR, 'deliveries', 'fixtures', 'test.csv')
		
		#post to the page the file
		self.client.post()

		#check that anything is uploaded.
		self.assertTrue(bool(Route.objects.all()))
		self.assertTrue(bool(Delivery.objects.all()))