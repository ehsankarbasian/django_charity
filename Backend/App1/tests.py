from django.test import TestCase
from rest_framework.test import APIRequestFactory
from App1.Components.helper_functions import client_post
from App1.Components.helper_functions import client_get
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

    def test_api_create_category(self):
        response_1 = client_post('CreateCategory', {})
        response_2 = client_post('CreateCategory', {"title": "food"})
        response_3 = client_post('CreateCategory', {"title": "vehicle"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('title',)]",
                             'success': '0'}
        response_2_result = {'status': 'notUniqueTitle',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_3_result = {'message': 'category created successfully',
                             'id': 5,
                             'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        category = Category.objects.get(id=5)
        self.assertEqual(category.title, "vehicle")

    def test_api_create_subcategory(self):
        category = Category.objects.create(title="vehicle")
        response_1 = client_post('CreateSubCategory', {})
        response_2 = client_post('CreateSubCategory', {"title": "car"})
        response_3 = client_post('CreateSubCategory', {"category_id": 2})
        response_4 = client_post('CreateSubCategory', {"title": "car", "category_id": 6})
        response_5 = client_post('CreateSubCategory', {"title": "car", "category_id": 5})
        response_6 = client_post('CreateSubCategory', {"title": "car", "category_id": 3})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('title',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('category_id',)]",
                             'success': '0'}
        response_3_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('title',)]",
                             'success': '0'}
        response_4_result = {'status': 'categoryNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = {'message': 'subcategory created successfully',
                             'id': 13,
                             'success': '1'}
        response_6_result = {'status': 'notUniqueTitle',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        subCategory = SubCategory.objects.get(id=13)
        self.assertEqual(subCategory.title, "car")
        self.assertEqual(subCategory.category, category)

    def test_api_create_product(self):
        category = Category.objects.create(title="vehicle")
        subCategory = SubCategory.objects.create(title="car", category=category)
        response_1 = client_post('CreateProduct', {})
        response_2 = client_post('CreateProduct', {"title": "saipa 151"})
        response_3 = client_post('CreateProduct', {"quantity": 50})
        response_4 = client_post('CreateProduct', {"subcategory_id": 13})
        response_5 = client_post('CreateProduct', {"title": "saipa 151", "quantity": 50})
        response_6 = client_post('CreateProduct', {"title": "saipa 151", "subcategory_id": 13})
        response_7 = client_post('CreateProduct', {"quantity": 50, "subcategory_id": 13})
        response_8 = client_post('CreateProduct', {"title": "saipa 151", "quantity": "three", "subcategory_id": 13})
        response_9 = client_post('CreateProduct', {"title": "saipa 151", "quantity": 50, "subcategory_id": 17})
        response_10 = client_post('CreateProduct', {"title": "gta sa", "quantity": 50, "subcategory_id": 13})
        response_11 = client_post('CreateProduct', {"title": "saipa 151", "quantity": 50, "subcategory_id": 13})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('title',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('quantity',)]",
                             'success': '0'}
        response_3_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('title',)]",
                             'success': '0'}
        response_4_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('title',)]",
                             'success': '0'}
        response_5_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('subcategory_id',)]",
                             'success': '0'}
        response_6_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('quantity',)]",
                             'success': '0'}
        response_7_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('title',)]",
                             'success': '0'}
        response_8_result = {'status': 'requiredParams',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'three\'",)]',
                             'success': '0'}
        response_9_result = {'status': 'subcategoryNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_10_result = {'status': 'notUniqueTitle',
                              'error_type': 'CUSTOM',
                              'error_on': 'CUSTOM',
                              'success': '0'}
        response_11_result = {'message': 'product created successfully',
                              'id': 53,
                              'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        self.assertEqual(response_7, response_7_result)
        self.assertEqual(response_8, response_8_result)
        self.assertEqual(response_9, response_9_result)
        self.assertEqual(response_10, response_10_result)
        self.assertEqual(response_11, response_11_result)
        product = Product.objects.get(id=53)
        self.assertEqual(product.title, "saipa 151")
        self.assertEqual(product.quantity, 50)
        self.assertEqual(product.subCategory, subCategory)
