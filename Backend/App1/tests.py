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

    def test_api_category_list(self):
        response_1 = client_post('CategoryList', {})
        response_2 = client_post('CategoryList', {"search_key": ""})
        response_3 = client_post('CategoryList', {"search_key": "vehicle"})
        response_4 = client_post('CategoryList', {"search_key": "g"})
        response_5 = client_post('CategoryList', {"search_key": "oo"})
        response_6 = client_post('CategoryList', {"search_key": "clothes"})
        response_1_result = {'success': '1', 'empty': 0, 'count': 4,
                             'category_set': {1: {'id': 1, 'title': 'food'},
                                              2: {'id': 2, 'title': 'clothes'},
                                              3: {'id': 3, 'title': 'digital'},
                                              4: {'id': 4, 'title': 'video game'}}}
        response_2_result = response_1_result
        response_3_result = {'success': '1', 'empty': 1, 'count': 0, 'category_set': {}}
        response_4_result = {'success': '1', 'empty': 0, 'count': 2,
                             'category_set': {3: {'id': 3, 'title': 'digital'},
                                              4: {'id': 4, 'title': 'video game'}}}
        response_5_result = {'success': '1', 'empty': 0, 'count': 1,
                             'category_set': {1: {'id': 1, 'title': 'food'}}}
        response_6_result = {'success': '1', 'empty': 0, 'count': 1,
                             'category_set': {2: {'id': 2, 'title': 'clothes'}}}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)

    def test_api_subcategory_list(self):
        response_1 = client_post('SubCategoryList', {})
        response_2 = client_post('SubCategoryList', {"search_key": ""})
        response_3 = client_post('SubCategoryList', {"search_key": "car"})
        response_4 = client_post('SubCategoryList', {"search_key": "Gta"})
        response_5 = client_post('SubCategoryList', {"search_key": "ts"})
        response_6 = client_post('SubCategoryList', {"search_key": "p", "category_id": 3})
        response_7 = client_post('SubCategoryList', {"category_id": 4})
        response_8 = client_post('SubCategoryList', {"search_key": "", "category_id": 1})
        response_1_result = {'success': '1', 'empty': 0, 'count': 12,
                             'subcategory_set': {1: {'id': 1, 'title': 'oil', 'category_title': 'food', 'category_id': 1},
                                                 2: {'id': 2, 'title': 'rice', 'category_title': 'food', 'category_id': 1},
                                                 3: {'id': 3, 'title': 'fruit', 'category_title': 'food', 'category_id': 1},
                                                 4: {'id': 4, 'title': 'pants', 'category_title': 'clothes', 'category_id': 2},
                                                 5: {'id': 5, 'title': 'shirts', 'category_title': 'clothes', 'category_id': 2},
                                                 6: {'id': 6, 'title': 'socks', 'category_title': 'clothes', 'category_id': 2},
                                                 7: {'id': 7, 'title': 'hat', 'category_title': 'clothes', 'category_id': 2},
                                                 8: {'id': 8, 'title': 'mobile', 'category_title': 'digital', 'category_id': 3},
                                                 9: {'id': 9, 'title': 'printer', 'category_title': 'digital', 'category_id': 3},
                                                 10: {'id': 10, 'title': 'laptop', 'category_title': 'digital', 'category_id': 3},
                                                 11: {'id': 11, 'title': 'tmnt', 'category_title': 'video game', 'category_id': 4},
                                                 12: {'id': 12, 'title': 'GTA', 'category_title': 'video game', 'category_id': 4}}}
        response_2_result = response_1_result
        response_3_result = {'success': '1', 'empty': 1, 'count': 0,
                             'subcategory_set': {}}
        response_4_result = {'success': '1', 'empty': 0, 'count': 1,
                             'subcategory_set': {12: {'id': 12, 'title': 'GTA', 'category_title': 'video game', 'category_id': 4}}}
        response_5_result = {'success': '1', 'empty': 0, 'count': 2,
                             'subcategory_set': {4: {'id': 4, 'title': 'pants', 'category_title': 'clothes', 'category_id': 2},
                                                 5: {'id': 5, 'title': 'shirts', 'category_title': 'clothes', 'category_id': 2}}}
        response_6_result = {'success': '1', 'empty': 0, 'count': 2,
                             'subcategory_set': {9: {'id': 9, 'title': 'printer', 'category_title': 'digital', 'category_id': 3},
                                                 10: {'id': 10, 'title': 'laptop', 'category_title': 'digital', 'category_id': 3}}}
        response_7_result = {'success': '1', 'empty': 0, 'count': 2,
                             'subcategory_set': {11: {'id': 11, 'title': 'tmnt', 'category_title': 'video game', 'category_id': 4},
                                                 12: {'id': 12, 'title': 'GTA', 'category_title': 'video game', 'category_id': 4}}}
        response_8_result = {'success': '1', 'empty': 0, 'count': 3,
                             'subcategory_set': {1: {'id': 1, 'title': 'oil', 'category_title': 'food', 'category_id': 1},
                                                 2: {'id': 2, 'title': 'rice', 'category_title': 'food', 'category_id': 1},
                                                 3: {'id': 3, 'title': 'fruit', 'category_title': 'food', 'category_id': 1}}}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        self.assertEqual(response_7, response_7_result)
        self.assertEqual(response_8, response_8_result)

    def test_api_product_list(self):
        response_1 = client_post('ProductList', {})
        response_2 = client_post('ProductList', {"search_key": ""})
        response_3 = client_post('ProductList', {"search_key": "la"})
        response_4 = client_post('ProductList', {"search_key": "la", "subcategory_id": 1})
        response_5 = client_post('ProductList', {"search_key": "la", "category_id": 2})
        response_6 = client_post('ProductList', {"search_key": "la", "category_id": 2, "subcategory_id": 4})
        response_7 = client_post('ProductList', {"search_key": "gta", "category_id": 3})
        response_8 = client_post('ProductList', {"search_key": "gta"})
        response_9 = client_post('ProductList', {"category_id": 3, "subcategory_id": 2})
        response_10 = client_post('ProductList', {"category_id": 3, "subcategory_id": 8})
        response_1_result = {'success': '1', 'empty': 0, 'count': 52,
                             'product_set': {1: {'id': 1, 'title': 'ladan 1.5', 'quantity': 16, 'subcategory_title': 'oil', 'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                             2: {'id': 2, 'title': 'ladan 0.9', 'quantity': 12, 'subcategory_title': 'oil', 'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                             3: {'id': 3, 'title': 'aftab 1.5', 'quantity': 8, 'subcategory_title': 'oil', 'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                             4: {'id': 4, 'title': 'aftab 0.9', 'quantity': 24, 'subcategory_title': 'oil', 'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                             5: {'id': 5, 'title': 'bahar 1.5', 'quantity': 6, 'subcategory_title': 'oil', 'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                             6: {'id': 6, 'title': 'bahar 0.9', 'quantity': 36, 'subcategory_title': 'oil', 'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                             7: {'id': 7, 'title': 'mohsen', 'quantity': 20, 'subcategory_title': 'rice', 'subcategory_id': 2, 'category_title': 'food', 'category_id': 1},
                                             8: {'id': 8, 'title': 'khatere', 'quantity': 32, 'subcategory_title': 'rice', 'subcategory_id': 2, 'category_title': 'food', 'category_id': 1},
                                             9: {'id': 9, 'title': 'gtc', 'quantity': 28, 'subcategory_title': 'rice', 'subcategory_id': 2, 'category_title': 'food', 'category_id': 1},
                                             10: {'id': 10, 'title': 'benis', 'quantity': 40, 'subcategory_title': 'rice', 'subcategory_id': 2, 'category_title': 'food', 'category_id': 1},
                                             11: {'id': 11, 'title': 'orange', 'quantity': 400, 'subcategory_title': 'fruit', 'subcategory_id': 3, 'category_title': 'food', 'category_id': 1},
                                             12: {'id': 12, 'title': 'apple', 'quantity': 200, 'subcategory_title': 'fruit', 'subcategory_id': 3, 'category_title': 'food', 'category_id': 1},
                                             13: {'id': 13, 'title': 'banana', 'quantity': 100, 'subcategory_title': 'fruit', 'subcategory_id': 3, 'category_title': 'food', 'category_id': 1},
                                             14: {'id': 14, 'title': 'watermelon', 'quantity': 800, 'subcategory_title': 'fruit', 'subcategory_id': 3, 'category_title': 'food', 'category_id': 1},
                                             15: {'id': 15, 'title': 'carrot', 'quantity': 400, 'subcategory_title': 'fruit', 'subcategory_id': 3, 'category_title': 'food', 'category_id': 1},
                                             16: {'id': 16, 'title': 'tomato', 'quantity': 1200, 'subcategory_title': 'fruit', 'subcategory_id': 3, 'category_title': 'food', 'category_id': 1},
                                             17: {'id': 17, 'title': 'jeans', 'quantity': 50, 'subcategory_title': 'pants', 'subcategory_id': 4, 'category_title': 'clothes', 'category_id': 2},
                                             18: {'id': 18, 'title': 'slash', 'quantity': 80, 'subcategory_title': 'pants', 'subcategory_id': 4, 'category_title': 'clothes', 'category_id': 2},
                                             19: {'id': 19, 'title': 'sport', 'quantity': 300, 'subcategory_title': 'pants', 'subcategory_id': 4, 'category_title': 'clothes', 'category_id': 2},
                                             20: {'id': 20, 'title': 'blue t-shirt', 'quantity': 250, 'subcategory_title': 'shirts', 'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                             21: {'id': 21, 'title': 'white t-shirt', 'quantity': 200, 'subcategory_title': 'shirts', 'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                             22: {'id': 22, 'title': 'black t-shirt', 'quantity': 50, 'subcategory_title': 'shirts', 'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                             23: {'id': 23, 'title': 'white shirt', 'quantity': 300, 'subcategory_title': 'shirts', 'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                             24: {'id': 24, 'title': 'blue shirt', 'quantity': 400, 'subcategory_title': 'shirts', 'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                             25: {'id': 25, 'title': 'black', 'quantity': 350, 'subcategory_title': 'socks', 'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                             26: {'id': 26, 'title': 'white', 'quantity': 200, 'subcategory_title': 'socks', 'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                             27: {'id': 27, 'title': 'blue', 'quantity': 250, 'subcategory_title': 'socks', 'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                             28: {'id': 28, 'title': 'blue sport', 'quantity': 150, 'subcategory_title': 'socks', 'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                             29: {'id': 29, 'title': 'red sport', 'quantity': 100, 'subcategory_title': 'socks', 'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                             30: {'id': 30, 'title': 'red cap', 'quantity': 20, 'subcategory_title': 'hat', 'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2},
                                             31: {'id': 31, 'title': 'black cap', 'quantity': 25, 'subcategory_title': 'hat', 'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2},
                                             32: {'id': 32, 'title': 'green cap', 'quantity': 400, 'subcategory_title': 'hat', 'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2},
                                             33: {'id': 33, 'title': 'blue cap', 'quantity': 60, 'subcategory_title': 'hat', 'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2},
                                             34: {'id': 34, 'title': 'cowboy', 'quantity': 750, 'subcategory_title': 'hat', 'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2},
                                             35: {'id': 35, 'title': 'NOKIA 1200', 'quantity': 500, 'subcategory_title': 'mobile', 'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                             36: {'id': 36, 'title': 'NOKIA 1100', 'quantity': 500, 'subcategory_title': 'mobile', 'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                             37: {'id': 37, 'title': 'NOKIA 6600', 'quantity': 200, 'subcategory_title': 'mobile', 'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                             38: {'id': 38, 'title': 'galaxy star', 'quantity': 80, 'subcategory_title': 'mobile', 'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                             39: {'id': 39, 'title': 'NOKIA X2-00', 'quantity': 2000, 'subcategory_title': 'mobile', 'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                             40: {'id': 40, 'title': 'hp', 'quantity': 5, 'subcategory_title': 'printer', 'subcategory_id': 9, 'category_title': 'digital', 'category_id': 3},
                                             41: {'id': 41, 'title': 'hp big', 'quantity': 3, 'subcategory_title': 'printer', 'subcategory_id': 9, 'category_title': 'digital', 'category_id': 3},
                                             42: {'id': 42, 'title': 'acer', 'quantity': 20, 'subcategory_title': 'laptop', 'subcategory_id': 10, 'category_title': 'digital', 'category_id': 3},
                                             43: {'id': 43, 'title': 'asus', 'quantity': 15, 'subcategory_title': 'laptop', 'subcategory_id': 10, 'category_title': 'digital', 'category_id': 3},
                                             44: {'id': 44, 'title': 'hp', 'quantity': 25, 'subcategory_title': 'laptop', 'subcategory_id': 10, 'category_title': 'digital', 'category_id': 3},
                                             45: {'id': 45, 'title': 'tmnt 1', 'quantity': 20, 'subcategory_title': 'tmnt', 'subcategory_id': 11, 'category_title': 'video game', 'category_id': 4},
                                             46: {'id': 46, 'title': 'tmnt 2', 'quantity': 60, 'subcategory_title': 'tmnt', 'subcategory_id': 11, 'category_title': 'video game', 'category_id': 4},
                                             47: {'id': 47, 'title': 'tmnt 3', 'quantity': 10, 'subcategory_title': 'tmnt', 'subcategory_id': 11, 'category_title': 'video game', 'category_id': 4},
                                             48: {'id': 48, 'title': 'tmnt 4', 'quantity': 15, 'subcategory_title': 'tmnt', 'subcategory_id': 11, 'category_title': 'video game', 'category_id': 4},
                                             49: {'id': 49, 'title': 'gta sa', 'quantity': 2000, 'subcategory_title': 'GTA', 'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4},
                                             50: {'id': 50, 'title': 'gta vice city', 'quantity': 1500, 'subcategory_title': 'GTA', 'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4},
                                             51: {'id': 51, 'title': 'gta V', 'quantity': 500, 'subcategory_title': 'GTA', 'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4},
                                             52: {'id': 52, 'title': 'gta III', 'quantity': 1000, 'subcategory_title': 'GTA', 'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4}}}
        response_2_result = response_1_result
        response_3_result = {'success': '1', 'empty': 0, 'count': 7,
                             'product_set': {1: {'id': 1, 'title': 'ladan 1.5', 'quantity': 16, 'subcategory_title': 'oil', 'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                             2: {'id': 2, 'title': 'ladan 0.9', 'quantity': 12, 'subcategory_title': 'oil', 'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                             18: {'id': 18, 'title': 'slash', 'quantity': 80, 'subcategory_title': 'pants', 'subcategory_id': 4, 'category_title': 'clothes', 'category_id': 2},
                                             22: {'id': 22, 'title': 'black t-shirt', 'quantity': 50, 'subcategory_title': 'shirts', 'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                             25: {'id': 25, 'title': 'black', 'quantity': 350, 'subcategory_title': 'socks', 'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                             31: {'id': 31, 'title': 'black cap', 'quantity': 25, 'subcategory_title': 'hat', 'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2},
                                             38: {'id': 38, 'title': 'galaxy star', 'quantity': 80, 'subcategory_title': 'mobile', 'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3}}}
        response_4_result = {'success': '1', 'empty': 0, 'count': 2,
                             'product_set': {1: {'id': 1, 'title': 'ladan 1.5', 'quantity': 16, 'subcategory_title': 'oil', 'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                             2: {'id': 2, 'title': 'ladan 0.9', 'quantity': 12, 'subcategory_title': 'oil', 'subcategory_id': 1, 'category_title': 'food', 'category_id': 1}}}
        response_5_result = {'success': '1', 'empty': 0, 'count': 4,
                             'product_set': {18: {'id': 18, 'title': 'slash', 'quantity': 80, 'subcategory_title': 'pants', 'subcategory_id': 4, 'category_title': 'clothes', 'category_id': 2},
                                             22: {'id': 22, 'title': 'black t-shirt', 'quantity': 50, 'subcategory_title': 'shirts', 'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                             25: {'id': 25, 'title': 'black', 'quantity': 350, 'subcategory_title': 'socks', 'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                             31: {'id': 31, 'title': 'black cap', 'quantity': 25, 'subcategory_title': 'hat', 'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2}}}
        response_6_result = {'success': '1', 'empty': 0, 'count': 1,
                             'product_set': {18: {'id': 18, 'title': 'slash', 'quantity': 80, 'subcategory_title': 'pants', 'subcategory_id': 4, 'category_title': 'clothes', 'category_id': 2}}}
        response_7_result = {'success': '1', 'empty': 1, 'count': 0,
                             'product_set': {}}
        response_8_result = {'success': '1', 'empty': 0, 'count': 4,
                             'product_set': {49: {'id': 49, 'title': 'gta sa', 'quantity': 2000, 'subcategory_title': 'GTA', 'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4},
                                             50: {'id': 50, 'title': 'gta vice city', 'quantity': 1500, 'subcategory_title': 'GTA', 'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4},
                                             51: {'id': 51, 'title': 'gta V', 'quantity': 500, 'subcategory_title': 'GTA', 'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4},
                                             52: {'id': 52, 'title': 'gta III', 'quantity': 1000, 'subcategory_title': 'GTA', 'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4}}}
        response_9_result = {'success': '1', 'empty': 1, 'count': 0,
                             'product_set': {}}
        response_10_result = {'success': '1', 'empty': 0, 'count': 5,
                              'product_set': {35: {'id': 35, 'title': 'NOKIA 1200', 'quantity': 500, 'subcategory_title': 'mobile', 'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                              36: {'id': 36, 'title': 'NOKIA 1100', 'quantity': 500, 'subcategory_title': 'mobile', 'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                              37: {'id': 37, 'title': 'NOKIA 6600', 'quantity': 200, 'subcategory_title': 'mobile', 'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                              38: {'id': 38, 'title': 'galaxy star', 'quantity': 80, 'subcategory_title': 'mobile', 'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                              39: {'id': 39, 'title': 'NOKIA X2-00', 'quantity': 2000, 'subcategory_title': 'mobile', 'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3}}}
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
