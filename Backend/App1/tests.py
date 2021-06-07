import datetime
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from App1.Components.helper_functions import set_email_verified
from App1.Components.helper_functions import client_post
from App1.Components.helper_functions import client_get
from django.contrib.auth import authenticate
from App1.Components.init_test_db import *
from Backend.settings import HOST, PORT
from App1.models import *

from App1.passed_tests import *


class EventAPIsTestCase(TestCase):
    def setUp(self):
        init_db_user()
        init_db_profile()
        init_db_event()

    def test_api_createEvent(self):
        response_1 = client_post('CreateEvent', {})
        response_2 = client_post('CreateEvent', {"TOKEN_ID": "defaultDonator_1"})
        response_3 = client_post('CreateEvent', {"TOKEN_ID": "defaultDonator_1",
                                                 "title": "earthquake 16",
                                                 "description": "an STRONG earthquake 2"})
        response_4 = client_post('CreateEvent', {"TOKEN_ID": "defaultDonator_1",
                                                 "title": "earthquake 16",
                                                 "description": "an STRONG earthquake 2",
                                                 "money_target": "one hundred"})
        response_5 = client_post('CreateEvent', {"TOKEN_ID": "defaultDonator_1",
                                                 "title": "earthquake 16",
                                                 "description": "an STRONG earthquake 2",
                                                 "money_target": "one hundred",
                                                 "list_of_needs": "oil,rice,car"})
        response_6 = client_post('CreateEvent', {"TOKEN_ID": "defaultDonator_1",
                                                 "title": "earthquake 16",
                                                 "description": "an STRONG earthquake 2"})
        response_7 = client_post('CreateEvent', {"TOKEN_ID": "defaultDonator_1",
                                                 "title": "earthquake 16",
                                                 "description": "an STRONG earthquake 2",
                                                 "money_target": "5000 Dollar"})
        response_8 = client_post('CreateEvent', {"TOKEN_ID": "defaultDonator_1",
                                                 "title": "earthquake 16",
                                                 "description": "an STRONG earthquake 16",
                                                 "money_target": 5000})
        response_9 = client_post('CreateEvent', {"TOKEN_ID": "defaultDonator_1",
                                                 "title": "earthquake 17",
                                                 "description": "an STRONG earthquake 17",
                                                 "money_target": 8000})
        response_10 = client_post('CreateEvent', {"TOKEN_ID": "defaultNeedy_1",
                                                  "title": "earthquake 18",
                                                  "description": "a weak earthquake 18",
                                                  "list_of_needs": "mobile,rice,car",
                                                  "image_url": "https://i.pinimg.com/originals/14/6d/23/146d2364c3350bed70b3572a165f77cf.jpg"})
        response_11 = client_post('CreateEvent', {"TOKEN_ID": "defaultNeedy_1",
                                                  "title": "earthquake 19",
                                                  "description": "a weak earthquake 19",
                                                  "money_target": 50000,
                                                  "image_url": "https://images.squarespace-cdn.com/content/v1/580fa3f23e00bed1077047c5/1541363996794-UH93PW4LCUZF17NTJP8A/ke17ZwdGBToddI8pDm48kCKTt8a7LIDpOpilsEC_saVZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpwiQ_SjicWDOsmMxZh_9pyyk2aewuef7oulj76CCF4kB9EEgvOQWMXJy9ISpWkqViM/eq.png"})
        response_12 = client_post('CreateEvent', {"TOKEN_ID": "defaultNeedy_1",
                                                  "title": "earthquake 20",
                                                  "description": "a weak earthquake 20",
                                                  "list_of_needs": "mobile,rice",
                                                  "image_url": "https://images.squarespace-cdn.com/content/v1/580fa3f23e00bed1077047c5/1541363996794-UH93PW4LCUZF17NTJP8A/ke17ZwdGBToddI8pDm48kCKTt8a7LIDpOpilsEC_saVZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpwiQ_SjicWDOsmMxZh_9pyyk2aewuef7oulj76CCF4kB9EEgvOQWMXJy9ISpWkqViM/eq.png"})
        response_13 = client_post('CreateEvent', {"TOKEN_ID": "defaultDonator_2",
                                                  "title": "earthquake 21",
                                                  "description": "a weak earthquake 21",
                                                  "money_target": 60,
                                                  "image_url": "https://i.pinimg.com/originals/14/6d/23/146d2364c3350bed70b3572a165f77cf.jpg"})
        response_14 = client_post('CreateEvent', {"TOKEN_ID": "defaultDonator_2",
                                                  "title": "earthquake 22",
                                                  "description": "an STRONG earthquake 22",
                                                  "list_of_needs": "mobile,rice,car,oil",
                                                  "image_url": "https://images.squarespace-cdn.com/content/v1/580fa3f23e00bed1077047c5/1541363996794-UH93PW4LCUZF17NTJP8A/ke17ZwdGBToddI8pDm48kCKTt8a7LIDpOpilsEC_saVZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpwiQ_SjicWDOsmMxZh_9pyyk2aewuef7oulj76CCF4kB9EEgvOQWMXJy9ISpWkqViM/eq.png"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('TOKEN_ID',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('title',)]",
                             'success': '0'}
        response_3_result = {'status': 'ListAndTargetAreNone',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'status': 'MoneyTargetIntError',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'one hundred\'",)]',
                             'success': '0'}
        response_5_result = {'status': 'MoneyTargetIntError',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'one hundred\'",)]',
                             'success': '0'}
        response_6_result = {'status': 'ListAndTargetAreNone',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_7_result = {'status': 'MoneyTargetIntError',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'5000 Dollar\'",)]',
                             'success': '0'}
        response_8_result = {'message': 'event created', 'success': '1'}
        response_10_result = response_8_result
        response_9_result = response_8_result
        response_11_result = response_8_result
        response_12_result = response_8_result
        response_13_result = response_8_result
        response_14_result = response_8_result
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
        self.assertEqual(response_12, response_12_result)
        self.assertEqual(response_13, response_13_result)
        self.assertEqual(response_14, response_14_result)
        event_16 = Event.objects.get(id=16)
        event_17 = Event.objects.get(id=17)
        event_18 = Event.objects.get(id=18)
        event_19 = Event.objects.get(id=19)
        event_20 = Event.objects.get(id=20)
        event_21 = Event.objects.get(id=21)
        event_22 = Event.objects.get(id=22)
        creator_16 = UserProfile.objects.get(token="defaultDonator_1")
        creator_17 = UserProfile.objects.get(token="defaultDonator_1")
        creator_18 = UserProfile.objects.get(token="defaultNeedy_1")
        creator_19 = UserProfile.objects.get(token="defaultNeedy_1")
        creator_20 = UserProfile.objects.get(token="defaultNeedy_1")
        creator_21 = UserProfile.objects.get(token="defaultDonator_2")
        creator_22 = UserProfile.objects.get(token="defaultDonator_2")
        self.assertEqual(creator_16.user, event_16.creator)
        self.assertEqual(creator_17.user, event_17.creator)
        self.assertEqual(creator_18.user, event_18.creator)
        self.assertEqual(creator_19.user, event_19.creator)
        self.assertEqual(creator_20.user, event_20.creator)
        self.assertEqual(creator_21.user, event_21.creator)
        self.assertEqual(creator_22.user, event_22.creator)
        self.assertEqual(event_16.title, "earthquake 16")
        self.assertEqual(event_16.description, "an STRONG earthquake 16")
        self.assertEqual(event_16.list_of_needs, "")
        self.assertEqual(event_16.money_target, 5000)
        self.assertEqual(event_16.donated_money, 0)
        self.assertEqual(event_16.enabled, False)
        self.assertEqual(event_16.status, 0)
        self.assertEqual(event_16.image_url, HOST + ":" + PORT + '/images/default.png')
        self.assertEqual(event_16.feedback, "")
        self.assertEqual(event_16.edited, False)
        self.assertEqual(event_16.edited_by, -1)
        self.assertEqual(event_17.title, "earthquake 17")
        self.assertEqual(event_17.description, "an STRONG earthquake 17")
        self.assertEqual(event_17.list_of_needs, "")
        self.assertEqual(event_17.money_target, 8000)
        self.assertEqual(event_17.donated_money, 0)
        self.assertEqual(event_17.enabled, False)
        self.assertEqual(event_17.status, 0)
        self.assertEqual(event_17.image_url, HOST + ":" + PORT + '/images/default.png')
        self.assertEqual(event_17.feedback, "")
        self.assertEqual(event_17.edited, False)
        self.assertEqual(event_17.edited_by, -1)
        self.assertEqual(event_18.title, "earthquake 18")
        self.assertEqual(event_18.description, "a weak earthquake 18")
        self.assertEqual(event_18.list_of_needs, "mobile,rice,car")
        self.assertEqual(event_18.money_target, 0)
        self.assertEqual(event_18.donated_money, 0)
        self.assertEqual(event_18.enabled, False)
        self.assertEqual(event_18.status, 0)
        self.assertEqual(event_18.image_url, "https://i.pinimg.com/originals/14/6d/23/146d2364c3350bed70b3572a165f77cf.jpg")
        self.assertEqual(event_18.feedback, "")
        self.assertEqual(event_18.edited, False)
        self.assertEqual(event_18.edited_by, -1)
        self.assertEqual(event_19.title, "earthquake 19")
        self.assertEqual(event_19.description, "a weak earthquake 19")
        self.assertEqual(event_19.list_of_needs, "")
        self.assertEqual(event_19.money_target, 50000)
        self.assertEqual(event_19.donated_money, 0)
        self.assertEqual(event_19.enabled, False)
        self.assertEqual(event_19.status, 0)
        self.assertEqual(event_19.image_url, "https://images.squarespace-cdn.com/content/v1/580fa3f23e00bed1077047c5/1541363996794-UH93PW4LCUZF17NTJP8A/ke17ZwdGBToddI8pDm48kCKTt8a7LIDpOpilsEC_saVZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpwiQ_SjicWDOsmMxZh_9pyyk2aewuef7oulj76CCF4kB9EEgvOQWMXJy9ISpWkqViM/eq.png")
        self.assertEqual(event_19.feedback, "")
        self.assertEqual(event_19.edited, False)
        self.assertEqual(event_19.edited_by, -1)
        self.assertEqual(event_20.title, "earthquake 20")
        self.assertEqual(event_20.description, "a weak earthquake 20")
        self.assertEqual(event_20.list_of_needs, "mobile,rice")
        self.assertEqual(event_20.money_target, 0)
        self.assertEqual(event_20.donated_money, 0)
        self.assertEqual(event_20.enabled, False)
        self.assertEqual(event_20.status, 0)
        self.assertEqual(event_20.image_url, "https://images.squarespace-cdn.com/content/v1/580fa3f23e00bed1077047c5/1541363996794-UH93PW4LCUZF17NTJP8A/ke17ZwdGBToddI8pDm48kCKTt8a7LIDpOpilsEC_saVZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpwiQ_SjicWDOsmMxZh_9pyyk2aewuef7oulj76CCF4kB9EEgvOQWMXJy9ISpWkqViM/eq.png")
        self.assertEqual(event_20.feedback, "")
        self.assertEqual(event_20.edited, False)
        self.assertEqual(event_20.edited_by, -1)
        self.assertEqual(event_21.title, "earthquake 21")
        self.assertEqual(event_21.description, "a weak earthquake 21")
        self.assertEqual(event_21.list_of_needs, "")
        self.assertEqual(event_21.money_target, 60)
        self.assertEqual(event_21.donated_money, 0)
        self.assertEqual(event_21.enabled, False)
        self.assertEqual(event_21.status, 0)
        self.assertEqual(event_21.image_url, "https://i.pinimg.com/originals/14/6d/23/146d2364c3350bed70b3572a165f77cf.jpg")
        self.assertEqual(event_21.feedback, "")
        self.assertEqual(event_21.edited, False)
        self.assertEqual(event_21.edited_by, -1)
        self.assertEqual(event_22.title, "earthquake 22")
        self.assertEqual(event_22.description, "an STRONG earthquake 22")
        self.assertEqual(event_22.list_of_needs, "mobile,rice,car,oil")
        self.assertEqual(event_22.money_target, 0)
        self.assertEqual(event_22.donated_money, 0)
        self.assertEqual(event_22.enabled, False)
        self.assertEqual(event_22.status, 0)
        self.assertEqual(event_22.image_url, "https://images.squarespace-cdn.com/content/v1/580fa3f23e00bed1077047c5/1541363996794-UH93PW4LCUZF17NTJP8A/ke17ZwdGBToddI8pDm48kCKTt8a7LIDpOpilsEC_saVZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpwiQ_SjicWDOsmMxZh_9pyyk2aewuef7oulj76CCF4kB9EEgvOQWMXJy9ISpWkqViM/eq.png")
        self.assertEqual(event_22.feedback, "")
        self.assertEqual(event_22.edited, False)
        self.assertEqual(event_22.edited_by, -1)

    def test_api_requestedEventList(self):
        pass

    def test_api_searchEvent(self):
        pass

    def test_api_editEventByAdmin(self):
        pass

    def test_api_leaveFeedback(self):
        pass

    def test_api_disableEvent(self):
        pass

    def test_api_userEvent(self):
        pass

    def test_api_deleteEvent(self):
        pass

    def test_api_editEventByUser(self):
        pass

    def test_api_donateMoneyEvent(self):
        pass


class DonateAPIsTestCase(TestCase):
    def setUp(self):
        init_db_user()
        init_db_transaction()
        init_db_storeManagement()
        init_db_donateIn()

    def test_api_generalDonate(self):
        pass

    def test_api_pendingDonates(self):
        superAdminUser = User.objects.get(username="superAdmin")
        adminUser = User.objects.get(username="admin")
        donatorUser_1 = User.objects.get(username="donator_1")
        donatorUser_2 = User.objects.get(username="donator_2")
        needyUser_1 = User.objects.get(username="needy_1")
        superAdminProfile = UserProfile.objects.get(user=superAdminUser)
        adminProfile = UserProfile.objects.get(user=adminUser)
        donatorProfile_1 = UserProfile.objects.get(user=donatorUser_1)
        donatorProfile_2 = UserProfile.objects.get(user=donatorUser_2)
        needyProfile_1 = UserProfile.objects.get(user=needyUser_1)
        superAdminProfile.melli_code = "1232500"
        adminProfile.melli_code = "1234444"
        donatorProfile_1.melli_code = "1235555"
        donatorProfile_2.melli_code = "1236666"
        needyProfile_1.melli_code = "1237777"
        superAdminProfile.save()
        adminProfile.save()
        donatorProfile_1.save()
        donatorProfile_2.save()
        needyProfile_1.save()

        response_1 = client_post('PendingDonate', {})
        response_2 = client_post('PendingDonate', {"melli_code": "800900"})
        response_3 = client_post('PendingDonate', {"melli_code": "1232500"})
        response_4 = client_post('PendingDonate', {"melli_code": "1234444"})
        response_5 = client_post('PendingDonate', {"melli_code": "1235555"})
        response_6 = client_post('PendingDonate', {"melli_code": "1236666"})
        response_7 = client_post('PendingDonate', {"melli_code": "1237777"})
        response_1_result = {'success': '1',
                             'empty': 0,
                             'count': 10,
                             'donate_set': {1: {'donate_id': 1, 'product_name': 'aftab 1.5', 'product_id': 3, 'quantity': 4, 'melli_code': '1235555', 'donator_fname': '', 'donator_lname': ''},
                                            2: {'donate_id': 2, 'product_name': 'bahar 1.5', 'product_id': 5, 'quantity': 50, 'melli_code': '1236666', 'donator_fname': '', 'donator_lname': ''},
                                            3: {'donate_id': 3, 'product_name': 'ladan 0.9', 'product_id': 2, 'quantity': 2, 'melli_code': '1232500', 'donator_fname': '', 'donator_lname': ''},
                                            4: {'donate_id': 4, 'product_name': 'bahar 0.9', 'product_id': 6, 'quantity': 10000, 'melli_code': '1235555', 'donator_fname': '', 'donator_lname': ''},
                                            5: {'donate_id': 5, 'product_name': 'ladan 1.5', 'product_id': 1, 'quantity': 80, 'melli_code': '1236666', 'donator_fname': '', 'donator_lname': ''},
                                            6: {'donate_id': 6, 'product_name': 'aftab 0.9', 'product_id': 4, 'quantity': 29, 'melli_code': '1232500', 'donator_fname': '', 'donator_lname': ''},
                                            7: {'donate_id': 7, 'product_name': 'bahar 1.5', 'product_id': 5, 'quantity': 30, 'melli_code': '1234444', 'donator_fname': '', 'donator_lname': ''},
                                            8: {'donate_id': 8, 'product_name': 'mohsen', 'product_id': 7, 'quantity': 36, 'melli_code': '1234444', 'donator_fname': '', 'donator_lname': ''},
                                            9: {'donate_id': 9, 'product_name': 'ladan 0.9', 'product_id': 2, 'quantity': 1, 'melli_code': '1236666', 'donator_fname': '', 'donator_lname': ''},
                                            10: {'donate_id': 10, 'product_name': 'aftab 0.9', 'product_id': 4, 'quantity': 48, 'melli_code': '1232500', 'donator_fname': '', 'donator_lname': ''}}}
        response_2_result = {'status': 'donatorNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_3_result = {'success': '1',
                             'empty': 0,
                             'count': 3,
                             'donate_set': {3: {'donate_id': 3, 'product_name': 'ladan 0.9', 'product_id': 2, 'quantity': 2, 'melli_code': '1232500', 'donator_fname': '', 'donator_lname': ''},
                                            6: {'donate_id': 6, 'product_name': 'aftab 0.9', 'product_id': 4, 'quantity': 29, 'melli_code': '1232500', 'donator_fname': '', 'donator_lname': ''},
                                            10: {'donate_id': 10, 'product_name': 'aftab 0.9', 'product_id': 4, 'quantity': 48, 'melli_code': '1232500', 'donator_fname': '', 'donator_lname': ''}}}
        response_4_result = {'success': '1', 'empty': 0, 'count': 2,
                             'donate_set': {7: {'donate_id': 7, 'product_name': 'bahar 1.5', 'product_id': 5, 'quantity': 30, 'melli_code': '1234444', 'donator_fname': '', 'donator_lname': ''},
                                            8: {'donate_id': 8, 'product_name': 'mohsen', 'product_id': 7, 'quantity': 36, 'melli_code': '1234444', 'donator_fname': '', 'donator_lname': ''}}}
        response_5_result = {'success': '1', 'empty': 0, 'count': 2,
                             'donate_set': {1: {'donate_id': 1, 'product_name': 'aftab 1.5', 'product_id': 3, 'quantity': 4, 'melli_code': '1235555', 'donator_fname': '', 'donator_lname': ''},
                                            4: {'donate_id': 4, 'product_name': 'bahar 0.9', 'product_id': 6, 'quantity': 10000, 'melli_code': '1235555', 'donator_fname': '', 'donator_lname': ''}}}
        response_6_result = {'success': '1', 'empty': 0, 'count': 3,
                             'donate_set': {2: {'donate_id': 2, 'product_name': 'bahar 1.5', 'product_id': 5, 'quantity': 50, 'melli_code': '1236666', 'donator_fname': '', 'donator_lname': ''},
                                            5: {'donate_id': 5, 'product_name': 'ladan 1.5', 'product_id': 1, 'quantity': 80, 'melli_code': '1236666', 'donator_fname': '', 'donator_lname': ''},
                                            9: {'donate_id': 9, 'product_name': 'ladan 0.9', 'product_id': 2, 'quantity': 1, 'melli_code': '1236666', 'donator_fname': '', 'donator_lname': ''}}}
        response_7_result = {'success': '1',
                             'empty': 1,
                             'count': 0,
                             'donate_set': {}}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        self.assertEqual(response_7, response_7_result)

    def test_api_delivery(self):
        response_1 = client_post('Delivery', {})
        response_2 = client_post('Delivery', {"donate_id": 5})
        response_3 = client_post('Delivery', {"TOKEN_ID": "theToken"})
        response_4 = client_post('Delivery', {"donate_id": 5, "TOKEN_ID": "theToken"})
        response_5 = client_post('Delivery', {"donate_id": 5, "TOKEN_ID": "defaultNeedy_1"})
        response_6 = client_post('Delivery', {"donate_id": 5, "TOKEN_ID": "defaultDonator_2"})
        response_7 = client_post('Delivery', {"donate_id": 5, "TOKEN_ID": "defaultAdmin"})
        response_8 = client_post('Delivery', {"donate_id": 5, "TOKEN_ID": "defaultSuperAdmin"})
        response_9 = client_post('Delivery', {"donate_id": 6, "TOKEN_ID": "defaultSuperAdmin"})
        response_10 = client_post('Delivery', {"donate_id": 500, "TOKEN_ID": "defaultSuperAdmin"})
        donate_5 = DonatesIn.objects.get(id=5)
        donate_6 = DonatesIn.objects.get(id=6)
        adminProfile = UserProfile.objects.get(token="defaultAdmin")
        superAdminProfile = UserProfile.objects.get(token="defaultSuperAdmin")
        self.assertEqual(donate_5.transferee, adminProfile)
        self.assertEqual(donate_6.transferee, superAdminProfile)
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('donate_id',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('TOKEN_ID',)]",
                             'success': '0'}
        response_3_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('donate_id',)]",
                             'success': '0'}
        response_4_result = {'status': 'userNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = {'status': 'userIsNotAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_6_result = {'status': 'userIsNotAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_7_result = {'message': 'delivered successfully',
                             'success': '1'}
        response_8_result = {'status': 'deliveredBefore',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_9_result = {'message': 'delivered successfully',
                             'success': '1'}
        response_10_result = {'status': 'donateNotFound',
                              'error_type': 'CUSTOM',
                              'error_on': 'CUSTOM',
                              'success': '0'}
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


class NeedRequestAPIsTestCase(TestCase):
    def setUp(self):
        pass

    def test_api_createNeedRequest(self):
        pass

    def test_api_requestedNeedRequestList(self):
        pass

    def test_api_myNeedRequestList(self):
        pass

    def test_api_acceptOrRejectNeedRequest(self):
        pass

    def test_api_acceptedNeedRequestList(self):
        pass
