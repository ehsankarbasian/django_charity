from django.test import TestCase
from App1.Components.init_test_db import *
from App1.models import *


class AuthAPIsTestCase(TestCase):
    pass


class EventAPIsTestCase(TestCase):
    pass


class ProfileAPIsTestCase(TestCase):
    pass


class StoreAPIsTestCase(TestCase):
    def setUp(self):
        init_db_storeManagement()

    def test_sample(self):
        result = "P"
        self.assertEqual(result, "P")

    def test_api_create_category(self):
        pass

    def test_api_create_subcategory(self):
        pass

    def test_api_create_product(self):
        pass
