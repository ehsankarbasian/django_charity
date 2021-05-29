import datetime
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from App1.Components.helper_functions import set_email_verified
from App1.Components.helper_functions import client_post
from App1.Components.helper_functions import client_get
from django.contrib.auth import authenticate
from App1.Components.init_test_db import *
from App1.models import *


class AuthAPIsTestCase(TestCase):
    def setUp(self):
        init_db_user()

    def test_api_signup(self):
        response_1 = client_post('signup', {})
        response_2 = client_post('signup', {"username": "ehsan_karbasian",
                                            "email": "ehsan.karbasian@gmail.com"})
        response_3 = client_post('signup', {"username": "ehsan_karbasian",
                                            "email": "ehsan.karbasian@gmail.com",
                                            "password": "54321",
                                            "user_type": "donator"})
        response_4 = client_post('signup', {"username": "donator_1",
                                            "email": "ehsan.karb@asian@gmail.com",
                                            "password": "54321",
                                            "user_type": 3})
        response_5 = client_post('signup', {"username": "ehsan_karbasian",
                                            "email": "donator_2@gmail.com",
                                            "password": "54321",
                                            "user_type": 3})
        response_6 = client_post('signup', {"username": "donator_1",
                                            "email": "donator_1@gmail.com",
                                            "password": "54321",
                                            "user_type": 3})
        response_7 = client_post('signup', {"username": "ehsan_karbasian",
                                            "email": "ehsan.karbasian@gmail.com",
                                            "password": "54321",
                                            "user_type": 1})
        response_8 = client_post('signup', {"username": "ehsan_karbasian",
                                            "email": "ehsan.karbasian@gmail.com",
                                            "password": "54321",
                                            "user_type": 2})
        response_9 = client_post('signup', {"username": "needy_1",
                                            "email": "ehsan.karbasian@gmail.com",
                                            "password": "54321",
                                            "user_type": 3})
        response_10 = client_post('signup', {"username": "donator_3",
                                             "email": "don.ator._3+ntm+charity@gmail.com",
                                             "password": "54321",
                                             "user_type": 3})
        response_11 = client_post('signup', {"username": "needy_2",
                                             "email": "nee..dy._2+ntm_charity@gmail.com",
                                             "password": "54321",
                                             "user_type": 4})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('username',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('password',)]",
                             'success': '0'}
        response_3_result = {'status': 'requiredParams',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'donator\'",)]',
                             'success': '0'}
        response_4_result = {'status': 'invalidEmailError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = {'status': 'emailError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_6_result = {'status': 'emailUsernameError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_7_result = {'status': 'notAllowedUserTypeError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_8_result = {'status': 'notAllowedUserTypeError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_9_result = {'status': 'usernameError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_10_result = {'username': 'donator_3',
                              'email': 'donator_3@gmail.com',
                              'user_type': 3,
                              'success': '1'}
        response_11_result = {'username': 'needy_2',
                              'email': 'needy_2@gmail.com',
                              'user_type': 4,
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
        donatorUser_3 = User.objects.get(username="donator_3")
        donatorUserProfile_3 = UserProfile.objects.get(user=donatorUser_3)
        needyUser_2 = User.objects.get(username="needy_2")
        needyUserProfile_2 = UserProfile.objects.get(user=needyUser_2)
        self.assertEqual(User.objects.get(id=6), donatorUser_3)
        self.assertEqual(UserProfile.objects.get(id=6), donatorUserProfile_3)
        self.assertEqual(User.objects.get(id=7), needyUser_2)
        self.assertEqual(UserProfile.objects.get(id=7), needyUserProfile_2)

    def test_api_login(self):
        response_1 = client_post('login', {})
        response_2 = client_post('login', {"username": "donator_1"})
        response_3 = client_post('login', {"password": "12345"})
        response_4 = client_post('login', {"username": "donator_1", "password": "thePass"})
        response_5 = client_post('login', {"username": "dontor_1", "password": "12345"})
        response_6 = client_post('login', {"username": "superAdmin", "password": "12345"})
        response_7 = client_post('login', {"username": "admin", "password": "12345"})
        response_8 = client_post('login', {"username": "donator_1", "password": "12345"})
        response_9 = client_post('login', {"username": "needy_1", "password": "12345"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('username',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('password',)]",
                             'success': '0'}
        response_3_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('username',)]",
                             'success': '0'}
        response_4_result = {'status': 'wrongUsernameOrPass',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = response_4_result
        response_6_result = {'status': 'emailVerificationError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_7_result = response_6_result
        response_8_result = response_6_result
        response_9_result = response_6_result
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        self.assertEqual(response_7, response_7_result)
        self.assertEqual(response_8, response_8_result)
        self.assertEqual(response_9, response_9_result)
        set_email_verified("superAdmin")
        set_email_verified("admin")
        set_email_verified("donator_1")
        set_email_verified("needy_1")
        response_10 = client_post('login', {"username": "superAdmin", "password": "12345"})
        response_11 = client_post('login', {"username": "admin", "password": "12345"})
        response_12 = client_post('login', {"username": "donator_1", "password": "12345"})
        response_13 = client_post('login', {"username": "needy_1", "password": "12345"})
        response_10_result = {'username': 'superAdmin',
                              'email': 'superAdmin@gmail.com',
                              'token': 'defaultSuperAdmin',
                              'user_type': 1,
                              'success': '1'}
        response_11_result = {'username': 'admin',
                              'email': 'admin@gmail.com',
                              'token': 'defaultAdmin',
                              'user_type': 2,
                              'success': '1'}
        response_12_result = {'username': 'donator_1',
                              'email': 'donator_1@gmail.com',
                              'token': 'defaultDonator_1',
                              'user_type': 3,
                              'success': '1'}
        response_13_result = {'username': 'needy_1',
                              'email': 'needy@gmail.com',
                              'token': 'defaultNeedy_1',
                              'user_type': 4,
                              'success': '1'}
        self.assertEqual(response_10, response_10_result)
        self.assertEqual(response_11, response_11_result)
        self.assertEqual(response_12, response_12_result)
        self.assertEqual(response_13, response_13_result)

    def test_api_logout(self):
        set_email_verified("donator_1")
        client_post('login', {"username": "donator_1", "password": "12345"})
        response_1 = client_post('logout', {})
        response_1_result = {'message': 'successfully logged out', 'success': '1'}
        self.assertEqual(response_1, response_1_result)

    def test_api_verifyEmailTokenBased(self):
        response_1 = client_post('VerifyEmailTokenBased', {})
        response_2 = client_post('VerifyEmailTokenBased', {"email": "superAdmin@gmail.com"})
        response_3 = client_post('VerifyEmailTokenBased', {"email": "superAdmin@gmail.com",
                                                           "token": "theToken"})
        response_4 = client_post('VerifyEmailTokenBased', {"email": "superAdmin@gmail.com",
                                                           "token": "verifyEmailToken"})
        response_5 = client_post('VerifyEmailTokenBased', {"email": "admin@gmail.com",
                                                           "token": "verifyEmailToken"})
        response_6 = client_post('VerifyEmailTokenBased', {"email": "donator_2@gmail.com",
                                                           "token": "verifyEmailToken"})
        response_7 = client_post('VerifyEmailTokenBased', {"email": "needy@gmail.com",
                                                           "token": "verifyEmailToken"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('token',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('token',)]",
                             'success': '0'}
        response_3_result = {'status': 'privateTokenError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'message': 'email verification was successful, you can login now!', 'success': '1'}
        response_5_result = response_4_result
        response_6_result = response_4_result
        response_7_result = response_4_result
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        self.assertEqual(response_7, response_7_result)
        user_1 = UserProfile.objects.get(email="superAdmin@gmail.com")
        user_2 = UserProfile.objects.get(email="admin@gmail.com")
        user_3 = UserProfile.objects.get(email="donator_2@gmail.com")
        user_4 = UserProfile.objects.get(email="needy@gmail.com")
        self.assertEqual(user_1.verified_email, True)
        self.assertEqual(user_2.verified_email, True)
        self.assertEqual(user_3.verified_email, True)
        self.assertEqual(user_4.verified_email, True)

    def test_api_verifyEmailCodeBased(self):
        response_1 = client_post('VerifyEmail', {})
        response_2 = client_post('VerifyEmail', {"email": "superAdmin@gmail.com"})
        response_3 = client_post('VerifyEmail', {"email": "superAdmin@gmail.com", "code": 1355})
        response_4 = client_post('VerifyEmail', {"email": "superAdmin_2@gmail.com", "code": 1355})
        response_5 = client_post('VerifyEmail', {"email": "superAdmin@gmail.com", "code": 2500})
        response_6 = client_post('VerifyEmail', {"email": "admin@gmail.com", "code": 2500})
        response_7 = client_post('VerifyEmail', {"email": "donator_2@gmail.com", "code": 2500})
        response_8 = client_post('VerifyEmail', {"email": "needy@gmail.com", "code": 2500})
        response_9 = client_post('VerifyEmail', {"email": "needy@gmail.com", "code": 2500})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('code',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('code',)]",
                             'success': '0'}
        response_3_result = {'status': 'privateCodeError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'status': 'NoUserForEmail',
                             'error_type': "[<class 'App1.models.UserProfile.DoesNotExist'>]",
                             'error_on': "[DoesNotExist('UserProfile matching query does not exist.',)]",
                             'success': '0'}
        response_5_result = {'message': 'email verification was successful, you can login now!', 'success': '1'}
        response_6_result = response_5_result
        response_7_result = response_5_result
        response_8_result = response_5_result
        response_9_result = {'status': 'VerifiedBefore',
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
        user_1 = UserProfile.objects.get(email="superAdmin@gmail.com")
        user_2 = UserProfile.objects.get(email="admin@gmail.com")
        user_3 = UserProfile.objects.get(email="donator_2@gmail.com")
        user_4 = UserProfile.objects.get(email="needy@gmail.com")
        self.assertEqual(user_1.verified_email, True)
        self.assertEqual(user_2.verified_email, True)
        self.assertEqual(user_3.verified_email, True)
        self.assertEqual(user_4.verified_email, True)

    def test_api_forgotPassword(self):
        response_1 = client_post('ForgotPassword', {})
        response_2 = client_post('ForgotPassword', {"email": "ehsan@k@gmail.com"})
        response_3 = client_post('ForgotPassword', {"email": "ehsan.k@gmail.com"})
        response_4 = client_post('ForgotPassword', {"email": "donator_1@gmail.com"})
        response_5 = client_post('ForgotPassword', {"email": "needy@gmail.com"})
        set_email_verified("donator_1")
        set_email_verified("needy_1")
        response_6 = client_post('ForgotPassword', {"email": "d.on.at...o.r_.1@gmail.com"})
        response_7 = client_post('ForgotPassword', {"email": "nee.dy@gmail.com"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('email',)]",
                             'success': '0'}
        response_2_result = {'status': 'invalidEmailError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_3_result = {'status': 'noSuchUser',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'status': 'notVerifiedEmailError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = {'status': 'notVerifiedEmailError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_6_result = {'message': 'email sent', 'success': '1'}
        response_7_result = {'message': 'email sent', 'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        self.assertEqual(response_7, response_7_result)
        user_1 = User.objects.get(username="donator_1")
        profile_1 = UserProfile.objects.get(user=user_1)
        user_2 = User.objects.get(username="needy_1")
        profile_2 = UserProfile.objects.get(user=user_2)
        self.assertEqual(len(profile_1.reset_pass_token), 256)
        self.assertEqual(len(profile_2.reset_pass_token), 256)
        self.assertGreaterEqual(profile_1.reset_pass_code, 10000000)
        self.assertLessEqual(profile_1.reset_pass_code, 99999999)
        self.assertGreaterEqual(profile_2.reset_pass_code, 10000000)
        self.assertLessEqual(profile_2.reset_pass_code, 99999999)

    def test_api_resetPasswordTokenBased(self):
        set_email_verified("superAdmin")
        set_email_verified("donator_1")
        set_email_verified("needy_1")
        response_1 = client_post('ResetPasswordTokenBased', {})
        response_2 = client_post('ResetPasswordTokenBased', {"email": "superAdmin@gmail.com"})
        response_3 = client_post('ResetPasswordTokenBased', {"email": "superAdmin@gmail.com",
                                                             "pass1": "4444",
                                                             "token": "TheToken"})
        response_4 = client_post('ResetPasswordTokenBased', {"email": "superAdmin@gmail.com",
                                                             "pass1": "4444",
                                                             "pass2": "1234",
                                                             "token": "TheToken"})
        response_5 = client_post('ResetPasswordTokenBased', {"email": "superAdmin@gmail.com",
                                                             "pass1": "4444",
                                                             "pass2": "4444",
                                                             "token": "TheToken"})
        client_post('ForgotPassword', {"email": "superAdmin@gmail.com"})
        profile_1 = UserProfile.objects.get(email="superAdmin@gmail.com")
        response_6 = client_post('ResetPasswordTokenBased', {"email": "superAdmin@gmail.com",
                                                             "pass1": "SuperAdminPass",
                                                             "pass2": "SuperAdminPass",
                                                             "token": profile_1.reset_pass_token})
        client_post('ForgotPassword', {"email": "donator_1@gmail.com"})
        profile_2 = UserProfile.objects.get(email="donator_1@gmail.com")
        response_7 = client_post('ResetPasswordTokenBased', {"email": "donator_1@gmail.com",
                                                             "pass1": "DonatorPass",
                                                             "pass2": "DonatorPass",
                                                             "token": profile_2.reset_pass_token})
        client_post('ForgotPassword', {"email": "needy@gmail.com"})
        profile_3 = UserProfile.objects.get(email="needy@gmail.com")
        response_8 = client_post('ResetPasswordTokenBased', {"email": "needy@gmail.com",
                                                             "pass1": "NeedyPass",
                                                             "pass2": "NeedyPass",
                                                             "token": profile_3.reset_pass_token})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('pass1',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('pass1',)]",
                             'success': '0'}
        response_3_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('pass2',)]",
                             'success': '0'}
        response_4_result = {'status': 'differentPasswords',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = {'status': 'privateTokenError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_6_result = {'message': 'password changed', 'success': '1'}
        response_7_result = {'message': 'password changed', 'success': '1'}
        response_8_result = {'message': 'password changed', 'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        self.assertEqual(response_7, response_7_result)
        self.assertEqual(response_8, response_8_result)
        user_1 = authenticate(username="superAdmin", password="SuperAdminPass")
        user_2 = authenticate(username="donator_1", password="DonatorPass")
        user_3 = authenticate(username="needy_1", password="NeedyPass")
        self.assertEqual(user_1, profile_1.user)
        self.assertEqual(user_2, profile_2.user)
        self.assertEqual(user_3, profile_3.user)

    def test_api_resetPasswordCodeBased(self):
        set_email_verified("superAdmin")
        set_email_verified("donator_1")
        set_email_verified("needy_1")
        response_1 = client_post('ResetPassword', {})
        response_2 = client_post('ResetPassword', {"email": "superAdmin@gmail.com",
                                                   "pass1": "4444",
                                                   "code": "1234"})
        response_3 = client_post('ResetPassword', {"email": "superAdmin@gmail.com",
                                                   "pass1": "4444",
                                                   "pass2": "4444",
                                                   "code": "theCode"})
        response_4 = client_post('ResetPassword', {"email": "superAdmin@gmail.com",
                                                   "pass1": "4444",
                                                   "pass2": "1234",
                                                   "code": "1234"})
        response_5 = client_post('ResetPassword', {"email": "superAdmin@gmail.com",
                                                   "pass1": "4444",
                                                   "pass2": "4444",
                                                   "code": "2021"})
        client_post('ForgotPassword', {"email": "superAdmin@gmail.com"})
        profile_1 = UserProfile.objects.get(email="superAdmin@gmail.com")
        response_6 = client_post('ResetPassword', {"email": "superAdmin@gmail.com",
                                                   "pass1": "SuperAdminPass",
                                                   "pass2": "SuperAdminPass",
                                                   "code": profile_1.reset_pass_code})
        client_post('ForgotPassword', {"email": "donator_1@gmail.com"})
        profile_2 = UserProfile.objects.get(email="donator_1@gmail.com")
        response_7 = client_post('ResetPassword', {"email": "donator_1@gmail.com",
                                                   "pass1": "DonatorPass",
                                                   "pass2": "DonatorPass",
                                                   "code": profile_2.reset_pass_code})
        client_post('ForgotPassword', {"email": "needy@gmail.com"})
        profile_3 = UserProfile.objects.get(email="needy@gmail.com")
        response_8 = client_post('ResetPassword', {"email": "needy@gmail.com",
                                                   "pass1": "NeedyPass",
                                                   "pass2": "NeedyPass",
                                                   "code": profile_3.reset_pass_code})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('pass1',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('pass2',)]",
                             'success': '0'}
        response_3_result = {'status': 'requiredParams',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'theCode\'",)]',
                             'success': '0'}
        response_4_result = {'status': 'differentPasswords',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = {'status': 'privateCodeError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_6_result = {'message': 'password changed', 'success': '1'}
        response_7_result = {'message': 'password changed', 'success': '1'}
        response_8_result = {'message': 'password changed', 'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        self.assertEqual(response_7, response_7_result)
        self.assertEqual(response_8, response_8_result)
        user_1 = authenticate(username="superAdmin", password="SuperAdminPass")
        user_2 = authenticate(username="donator_1", password="DonatorPass")
        user_3 = authenticate(username="needy_1", password="NeedyPass")
        self.assertEqual(user_1, profile_1.user)
        self.assertEqual(user_2, profile_2.user)
        self.assertEqual(user_3, profile_3.user)

    def test_api_notVerifiedUserSet(self):
        response_1 = client_post('NotVerifiedUserSet', {})
        response_2 = client_post('NotVerifiedUserSet', {"TOKEN_API": "jnfavlbinjaedsnc"})
        response_3 = client_post('NotVerifiedUserSet', {"TOKEN_API": "defaultAdmin"})
        response_4 = client_post('NotVerifiedUserSet', {"TOKEN_API": "defaultDonator_1"})
        response_5 = client_post('NotVerifiedUserSet', {"TOKEN_API": "defaultSuperAdmin"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('TOKEN_API',)]",
                             'success': '0'}
        response_2_result = {'status': 'adminNotFound',
                             'error_type': "[<class 'App1.models.UserProfile.DoesNotExist'>]",
                             'error_on': "[DoesNotExist('UserProfile matching query does not exist.',)]",
                             'success': '0'}
        response_3_result = {'status': 'notSuperAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'status': 'notSuperAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = {'success': '1',
                             'empty_needy': 0,
                             'empty_donator': 0,
                             'pagination_params': None,
                             'needy_set': {5: {'id': 5,
                                               'username': 'needy_1',
                                               'user_type': 4,
                                               'first_name': '',
                                               'last_name': '',
                                               'melli_code': '',
                                               'email': 'needy@gmail.com',
                                               'job': None,
                                               'address': None,
                                               'mobile_number': None,
                                               'house_phone': None,
                                               'workplace_phone': None,
                                               'gender': 'male',
                                               'married': False,
                                               'birth_date': None, }},
                             'donator_set': {3: {'id': 3,
                                                 'username': 'donator_1',
                                                 'user_type': 3,
                                                 'first_name': '',
                                                 'last_name': '',
                                                 'melli_code': '',
                                                 'email': 'donator_1@gmail.com',
                                                 'job': None,
                                                 'address': None,
                                                 'mobile_number': None,
                                                 'house_phone': None,
                                                 'workplace_phone': None,
                                                 'gender': 'male',
                                                 'married': False,
                                                 'birth_date': None, },
                                             4: {'id': 4,
                                                 'username': 'donator_2',
                                                 'user_type': 3,
                                                 'first_name': '',
                                                 'last_name': '',
                                                 'melli_code': '',
                                                 'email': 'donator_2@gmail.com',
                                                 'job': None,
                                                 'address': None,
                                                 'mobile_number': None,
                                                 'house_phone': None,
                                                 'workplace_phone': None,
                                                 'gender': 'male',
                                                 'married': False,
                                                 'birth_date': None}}}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)

    def test_api_verifyOrRejectUser(self):
        response_1 = client_post('VerifyOrRejectUser', {})
        response_2 = client_post('VerifyOrRejectUser',
                                 {"TOKEN_API": "jnfavlbinjaedsnc", "user_id": 3, "action": "verify"})
        response_3 = client_post('VerifyOrRejectUser',
                                 {"TOKEN_API": "jnfavlbinjaedsnc", "user_id": "one", "action": "verify"})
        response_4 = client_post('VerifyOrRejectUser', {"TOKEN_API": "jnfavlbinjaedsnc", "user_id": 4, "action": 1})
        response_5 = client_post('VerifyOrRejectUser', {"TOKEN_API": "defaultDonator_2", "user_id": 4, "action": 1})
        response_6 = client_post('VerifyOrRejectUser', {"TOKEN_API": "defaultNeedy_1", "user_id": 4, "action": 1})
        response_7 = client_post('VerifyOrRejectUser', {"TOKEN_API": "defaultAdmin", "user_id": 4, "action": 1})
        response_8 = client_post('VerifyOrRejectUser', {"TOKEN_API": "defaultSuperAdmin", "user_id": 12, "action": 1})
        response_9 = client_post('VerifyOrRejectUser', {"TOKEN_API": "defaultSuperAdmin", "user_id": 1, "action": 1})
        response_10 = client_post('VerifyOrRejectUser', {"TOKEN_API": "defaultSuperAdmin", "user_id": 2, "action": 1})
        response_11 = client_post('VerifyOrRejectUser', {"TOKEN_API": "defaultSuperAdmin", "user_id": 3, "action": 0})
        response_12 = client_post('VerifyOrRejectUser', {"TOKEN_API": "defaultSuperAdmin", "user_id": 3, "action": 1})
        response_13 = client_post('VerifyOrRejectUser', {"TOKEN_API": "defaultSuperAdmin", "user_id": 4, "action": 1})
        response_14 = client_post('VerifyOrRejectUser', {"TOKEN_API": "defaultSuperAdmin", "user_id": 4, "action": 1})
        response_15 = client_post('VerifyOrRejectUser', {"TOKEN_API": "defaultSuperAdmin", "user_id": 5, "action": 1})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('TOKEN_API',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'verify\'",)]',
                             'success': '0'}
        response_3_result = {'status': 'requiredParams',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'one\'",)]',
                             'success': '0'}
        response_4_result = {'status': 'adminNotFound',
                             'error_type': "[<class 'App1.models.UserProfile.DoesNotExist'>]",
                             'error_on': "[DoesNotExist('UserProfile matching query does not exist.',)]",
                             'success': '0'}
        response_5_result = {'status': 'notSuperAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_6_result = {'status': 'notSuperAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_7_result = {'status': 'notSuperAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_8_result = {'status': 'userNotFound',
                             'error_type': "[<class 'App1.models.UserProfile.DoesNotExist'>]",
                             'error_on': "[DoesNotExist('UserProfile matching query does not exist.',)]",
                             'success': '0'}
        response_9_result = {'status': 'userTypeError',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0',
                             'explanation': 'user_type is superAdmin'}
        response_10_result = {'status': 'userTypeError',
                              'error_type': 'CUSTOM',
                              'error_on': 'CUSTOM',
                              'success': '0',
                              'explanation': 'user_type is admin'}
        response_11_result = {'message': 'user rejected (deleted) successfully', 'success': '1'}
        response_12_result = {'status': 'userNotFound',
                              'error_type': "[<class 'App1.models.UserProfile.DoesNotExist'>]",
                              'error_on': "[DoesNotExist('UserProfile matching query does not exist.',)]",
                              'success': '0'}
        response_13_result = {'message': 'user verified successfully', 'success': '1'}
        response_14_result = {'status': 'verifiedBefore',
                              'error_type': 'CUSTOM',
                              'error_on': 'CUSTOM',
                              'success': '0'}
        response_15_result = {'message': 'user verified successfully', 'success': '1'}
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
        self.assertEqual(response_15, response_15_result)
        user_1 = UserProfile.objects.get(id=1)
        user_2 = UserProfile.objects.get(id=2)
        user_3 = UserProfile.objects.filter(id=3)
        user_4 = UserProfile.objects.get(id=4)
        user_5 = UserProfile.objects.get(id=5)
        self.assertEqual(user_1.verified, False)
        self.assertEqual(user_2.verified, False)
        self.assertEqual(len(user_3), 0)
        self.assertEqual(user_4.verified, True)
        self.assertEqual(user_5.verified, True)


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
        self.assertEqual(event_16.image_url, None)
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
        self.assertEqual(event_17.image_url, None)
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


class ProfileAPIsTestCase(TestCase):
    def setUp(self):
        init_db_user()
        init_db_profile()

    def test_api_loadUserProfile(self):
        response_1 = client_post('LoadUserProfile', {})
        response_2 = client_post('LoadUserProfile', {"username": "Nobody"})
        response_3 = client_post('LoadUserProfile', {"username": "superAdmin"})
        response_4 = client_post('LoadUserProfile', {"username": "admin"})
        response_5 = client_post('LoadUserProfile', {"username": "donator_2"})
        response_6 = client_post('LoadUserProfile', {"username": "needy_1"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('username',)]",
                             'success': '0'}
        response_2_result = {'status': 'DoesNotExist',
                             'error_type': "[<class 'django.contrib.auth.models.User.DoesNotExist'>]",
                             'error_on': "[DoesNotExist('User matching query does not exist.',)]",
                             'success': '0'}
        response_3_result = {'username': 'superAdmin',
                             'user_type': 1,
                             'first_name': 'super admin first name',
                             'last_name': 'super admin last name',
                             'melli_code': '1232500',
                             'email': 'superAdmin@gmail.com',
                             'job': 'the super admin of NTM charity',
                             'address': 'ntm charity',
                             'mobile_number': '09132224444',
                             'house_phone': '02152254444',
                             'workplace_phone': '02152253333',
                             'gender': True,
                             'married': False,
                             'birth_date': datetime.date(2021, 1, 23),
                             'verified_needy': True,
                             'verified': True,
                             'verified_mobile': False,
                             'verified_email': True,
                             'is_profile_completed': True,
                             'success': '1'}
        response_4_result = {'username': 'admin',
                             'user_type': 2,
                             'first_name': 'admin first name',
                             'last_name': 'admin last name',
                             'melli_code': '1234444',
                             'email': 'admin@gmail.com',
                             'job': 'the admin of NTM charity',
                             'address': 'ntm charity',
                             'mobile_number': '09132225555',
                             'house_phone': '02152256666',
                             'workplace_phone': '02152254444',
                             'gender': False,
                             'married': True,
                             'birth_date': datetime.date(2020, 8, 11),
                             'verified_needy': True,
                             'verified': True,
                             'verified_mobile': True,
                             'verified_email': True,
                             'is_profile_completed': True,
                             'success': '1'}
        response_5_result = {'username': 'donator_2',
                             'user_type': 3,
                             'first_name': '',
                             'last_name': '',
                             'melli_code': '',
                             'email': 'donator_2@gmail.com',
                             'job': None,
                             'address': None,
                             'mobile_number': None,
                             'house_phone': None,
                             'workplace_phone': None,
                             'gender': True,
                             'married': False,
                             'birth_date': None,
                             'verified_needy': False,
                             'verified': False,
                             'verified_mobile': False,
                             'verified_email': False,
                             'is_profile_completed': False,
                             'success': '1'}
        response_6_result = {'username': 'needy_1',
                             'user_type': 4,
                             'first_name': '',
                             'last_name': '',
                             'melli_code': '',
                             'email': 'needy@gmail.com',
                             'job': None,
                             'address': None,
                             'mobile_number': None,
                             'house_phone': None,
                             'workplace_phone': None,
                             'gender': True,
                             'married': False,
                             'birth_date': None,
                             'verified_needy': False,
                             'verified': False,
                             'verified_mobile': False,
                             'verified_email': False,
                             'is_profile_completed': False,
                             'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        superAdminUser = User.objects.get(username="superAdmin")
        adminUser = User.objects.get(username="admin")
        donatorUser_2 = User.objects.get(username="donator_2")
        needyUser_1 = User.objects.get(username="needy_1")
        superAdminProfile = UserProfile.objects.get(user=superAdminUser)
        adminProfile = UserProfile.objects.get(user=adminUser)
        donatorProfile_2 = UserProfile.objects.get(user=donatorUser_2)
        needyProfile_1 = UserProfile.objects.get(user=needyUser_1)
        donatorProfile_2.first_name = "donator 2 first name"
        donatorProfile_2.last_name = "donator 2 last name"
        donatorProfile_2.melli_code = "12344425"
        donatorProfile_2.job = "a donator of NTM charity"
        donatorProfile_2.address = "ntm charity donator 2 home"
        donatorProfile_2.mobile_number = "09132225665"
        donatorProfile_2.house_phone = "02152256556"
        donatorProfile_2.workplace_phone = "02152254334"
        donatorProfile_2.gender = 0
        donatorProfile_2.married = 0
        donatorProfile_2.birth_date = "2018-08-11"
        donatorProfile_2.verified = True
        donatorProfile_2.verified_mobile = True
        donatorProfile_2.verified_email = False
        donatorProfile_2.completed = True
        donatorProfile_2.save()
        needyProfile_1.first_name = "needy 1 first name"
        needyProfile_1.last_name = "needy 1 last name"
        needyProfile_1.melli_code = "1234455"
        needyProfile_1.job = "a needy of NTM charity"
        needyProfile_1.address = "ntm charity needy 1 home"
        needyProfile_1.mobile_number = "09132225775"
        needyProfile_1.house_phone = "02152256766"
        needyProfile_1.workplace_phone = "02152254474"
        needyProfile_1.gender = 1
        needyProfile_1.married = 0
        needyProfile_1.birth_date = "2007-08-11"
        needyProfile_1.verified = True
        needyProfile_1.verified_mobile = True
        needyProfile_1.verified_email = True
        needyProfile_1.completed = True
        needyProfile_1.save()
        superAdminProfile.first_name = "THE super admin first name"
        superAdminProfile.last_name = "THE super admin last name"
        superAdminProfile.address = "ntm charity address 2"
        superAdminProfile.mobile_number = "09132229999"
        superAdminProfile.married = 1
        superAdminProfile.save()
        adminProfile.first_name = "THE admin first name"
        adminProfile.last_name = "THE admin last name"
        adminProfile.house_phone = "02152256896"
        adminProfile.save()
        response_7 = client_post('LoadUserProfile', {"username": "superAdmin"})
        response_8 = client_post('LoadUserProfile', {"username": "admin"})
        response_9 = client_post('LoadUserProfile', {"username": "donator_2"})
        response_10 = client_post('LoadUserProfile', {"username": "needy_1"})
        response_7_result = {'username': 'superAdmin',
                             'user_type': 1,
                             'first_name': 'THE super admin first name',
                             'last_name': 'THE super admin last name',
                             'melli_code': '1232500',
                             'email': 'superAdmin@gmail.com',
                             'job': 'the super admin of NTM charity',
                             'address': 'ntm charity address 2',
                             'mobile_number': '09132229999',
                             'house_phone': '02152254444',
                             'workplace_phone': '02152253333',
                             'gender': True,
                             'married': True,
                             'birth_date': datetime.date(2021, 1, 23),
                             'verified_needy': True,
                             'verified': True,
                             'verified_mobile': False,
                             'verified_email': True,
                             'is_profile_completed': True,
                             'success': '1'}
        response_8_result = {'username': 'admin',
                             'user_type': 2,
                             'first_name': 'THE admin first name',
                             'last_name': 'THE admin last name',
                             'melli_code': '1234444',
                             'email': 'admin@gmail.com',
                             'job': 'the admin of NTM charity',
                             'address': 'ntm charity',
                             'mobile_number': '09132225555',
                             'house_phone': '02152256896',
                             'workplace_phone': '02152254444',
                             'gender': False,
                             'married': True,
                             'birth_date': datetime.date(2020, 8, 11),
                             'verified_needy': True,
                             'verified': True, 'verified_mobile': True,
                             'verified_email': True,
                             'is_profile_completed': True,
                             'success': '1'}
        response_9_result = {'username': 'donator_2',
                             'user_type': 3,
                             'first_name': 'donator 2 first name',
                             'last_name': 'donator 2 last name',
                             'melli_code': '12344425',
                             'email': 'donator_2@gmail.com',
                             'job': 'a donator of NTM charity',
                             'address': 'ntm charity donator 2 home',
                             'mobile_number': '09132225665',
                             'house_phone': '02152256556',
                             'workplace_phone': '02152254334',
                             'gender': False,
                             'married': False,
                             'birth_date': datetime.date(2018, 8, 11),
                             'verified_needy': True,
                             'verified': True,
                             'verified_mobile': True,
                             'verified_email': False,
                             'is_profile_completed': True,
                             'success': '1'}
        response_10_result = {'username': 'needy_1',
                              'user_type': 4,
                              'first_name': 'needy 1 first name',
                              'last_name': 'needy 1 last name',
                              'melli_code': '1234455',
                              'email': 'needy@gmail.com',
                              'job': 'a needy of NTM charity',
                              'address': 'ntm charity needy 1 home',
                              'mobile_number': '09132225775',
                              'house_phone': '02152256766',
                              'workplace_phone': '02152254474',
                              'gender': True,
                              'married': False,
                              'birth_date': datetime.date(2007, 8, 11),
                              'verified_needy': True,
                              'verified': True,
                              'verified_mobile': True,
                              'verified_email': True,
                              'is_profile_completed': True,
                              'success': '1'}
        self.assertEqual(response_7, response_7_result)
        self.assertEqual(response_8, response_8_result)
        self.assertEqual(response_9, response_9_result)
        self.assertEqual(response_10, response_10_result)

    def test_api_submitUserProfile(self):
        response_1 = client_post('SubmitUserProfile', {})
        response_2 = client_post('SubmitUserProfile', {"username": "donator_1",
                                                       "first_name": "donator_1 f_name"})
        response_3 = client_post('SubmitUserProfile', {"username": "donator_8",
                                                       "first_name": "donator_8 f_name",
                                                       "last_name": "donator_8 l_name",
                                                       "melli_code": "11111111",
                                                       "mobile_number": "09138888888"})
        response_4 = client_post('SubmitUserProfile', {"username": "donator_1",
                                                       "first_name": "donator_1 f_name",
                                                       "last_name": "donator_1 l_name",
                                                       "melli_code": "1170228271",
                                                       "mobile_number": "09139889999"})
        response_5 = client_post('SubmitUserProfile', {"username": "admin",
                                                       "first_name": "admin f_name",
                                                       "last_name": "admin l_name",
                                                       "melli_code": "1170228280",
                                                       "mobile_number": "09139889989"})
        response_6 = client_post('SubmitUserProfile', {"username": "needy_1",
                                                       "first_name": "needy f_name",
                                                       "last_name": "needy l_name",
                                                       "melli_code": "1170226666",
                                                       "mobile_number": "09139886655",
                                                       "job": "NTM needy 1",
                                                       "address": "needy_1 address",
                                                       "house_phone": "03152251111",
                                                       "gender": "1",
                                                       "married": "0"})
        response_7 = client_post('SubmitUserProfile', {"username": "donator_2",
                                                       "first_name": "donator_2 f_name",
                                                       "last_name": "donator_2 l_name",
                                                       "melli_code": "1170234567",
                                                       "mobile_number": "09139881346",
                                                       "job": "NTM donator 2",
                                                       "address": "donator_2 address",
                                                       "house_phone": "03152254545",
                                                       "workplace_phone": "03152255454",
                                                       "gender": "0",
                                                       "married": "1",
                                                       "birth_date": "2000-10-23"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('username',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('last_name',)]",
                             'success': '0'}
        response_3_result = {'status': 'noSuchUser',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'username': 'donator_1',
                             'email': 'donator_1@gmail.com',
                             'user_type': 3,
                             'success': '1'}
        response_5_result = {'username': 'admin',
                             'email': 'admin@gmail.com',
                             'user_type': 2,
                             'success': '1'}
        response_6_result = {'username': 'needy_1',
                             'email': 'needy@gmail.com',
                             'user_type': 4,
                             'success': '1'}
        response_7_result = {'username': 'donator_2',
                             'email': 'donator_2@gmail.com',
                             'user_type': 3,
                             'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        self.assertEqual(response_7, response_7_result)
        donatorUser_1 = User.objects.get(username="donator_1")
        donatorProfile_1 = UserProfile.objects.get(user=donatorUser_1)
        self.assertEqual(donatorUser_1.first_name, "donator_1 f_name")
        self.assertEqual(donatorUser_1.last_name, "donator_1 l_name")
        self.assertEqual(donatorProfile_1.first_name, "donator_1 f_name")
        self.assertEqual(donatorProfile_1.last_name, "donator_1 l_name")
        self.assertEqual(donatorProfile_1.melli_code, "1170228271")
        self.assertEqual(donatorProfile_1.mobile_number, "09139889999")
        adminUser_1 = User.objects.get(username="admin")
        adminProfile_1 = UserProfile.objects.get(user=adminUser_1)
        self.assertEqual(adminUser_1.first_name, "admin f_name")
        self.assertEqual(adminUser_1.last_name, "admin l_name")
        self.assertEqual(adminProfile_1.first_name, "admin f_name")
        self.assertEqual(adminProfile_1.last_name, "admin l_name")
        self.assertEqual(adminProfile_1.melli_code, "1170228280")
        self.assertEqual(adminProfile_1.mobile_number, "09139889989")
        needyUser = User.objects.get(username="needy_1")
        needyProfile = UserProfile.objects.get(user=needyUser)
        self.assertEqual(needyUser.first_name, "needy f_name")
        self.assertEqual(needyUser.last_name, "needy l_name")
        self.assertEqual(needyProfile.first_name, "needy f_name")
        self.assertEqual(needyProfile.last_name, "needy l_name")
        self.assertEqual(needyProfile.melli_code, "1170226666")
        self.assertEqual(needyProfile.mobile_number, "09139886655")
        self.assertEqual(needyProfile.job, "NTM needy 1")
        self.assertEqual(needyProfile.address, "needy_1 address")
        self.assertEqual(needyProfile.house_phone, "03152251111")
        self.assertEqual(needyProfile.gender, True)
        self.assertEqual(needyProfile.married, False)
        donatorUser_2 = User.objects.get(username="donator_2")
        donatorProfile_2 = UserProfile.objects.get(user=donatorUser_2)
        self.assertEqual(donatorUser_2.first_name, "donator_2 f_name")
        self.assertEqual(donatorUser_2.last_name, "donator_2 l_name")
        self.assertEqual(donatorProfile_2.first_name, "donator_2 f_name")
        self.assertEqual(donatorProfile_2.last_name, "donator_2 l_name")
        self.assertEqual(donatorProfile_2.melli_code, "1170234567")
        self.assertEqual(donatorProfile_2.mobile_number, "09139881346")
        self.assertEqual(donatorProfile_2.job, "NTM donator 2")
        self.assertEqual(donatorProfile_2.address, "donator_2 address")
        self.assertEqual(donatorProfile_2.house_phone, "03152254545")
        self.assertEqual(donatorProfile_2.workplace_phone, "03152255454")
        self.assertEqual(donatorProfile_2.gender, False)
        self.assertEqual(donatorProfile_2.married, True)
        self.assertEqual(donatorProfile_2.birth_date, datetime.date(2000, 10, 23))

    def test_api_userBio(self):
        response_1 = client_post('UserBio', {})
        response_2 = client_post('UserBio', {"username": "Nobody"})
        response_3 = client_post('UserBio', {"username": "superAdmin"})
        response_4 = client_post('UserBio', {"username": "admin"})
        donatorUser_2 = User.objects.get(username="donator_2")
        donatorProfile_2 = UserProfile.objects.get(user=donatorUser_2)
        donatorProfile_2.first_name = "donator 2 first name"
        donatorProfile_2.last_name = "donator 2 last name"
        donatorProfile_2.save()
        needyUser_1 = User.objects.get(username="needy_1")
        needyProfile_1 = UserProfile.objects.get(user=needyUser_1)
        needyProfile_1.first_name = "needy 1 first name"
        needyProfile_1.last_name = "needy 1 last name"
        needyProfile_1.verified = 1
        needyProfile_1.save()
        response_5 = client_post('UserBio', {"username": "donator_2"})
        response_6 = client_post('UserBio', {"username": "needy_1"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('username',)]",
                             'success': '0'}
        response_2_result = {'status': 'DoesNotExist',
                             'error_type': "[<class 'django.contrib.auth.models.User.DoesNotExist'>]",
                             'error_on': "[DoesNotExist('User matching query does not exist.',)]",
                             'success': '0'}
        response_3_result = {'username': 'superAdmin',
                             'user_type': 1,
                             'first_name': 'super admin first name',
                             'last_name': 'super admin last name',
                             'email': 'superAdmin@gmail.com',
                             'verified_needy': True,
                             'success': '1'}
        response_4_result = {'username': 'admin',
                             'user_type': 2,
                             'first_name': 'admin first name',
                             'last_name': 'admin last name',
                             'email': 'admin@gmail.com',
                             'verified_needy': True,
                             'success': '1'}
        response_5_result = {'username': 'donator_2',
                             'user_type': 3,
                             'first_name': 'donator 2 first name',
                             'last_name': 'donator 2 last name',
                             'email': 'donator_2@gmail.com',
                             'verified_needy': False,
                             'success': '1'}
        response_6_result = {'username': 'needy_1',
                             'user_type': 4,
                             'first_name': 'needy 1 first name',
                             'last_name': 'needy 1 last name',
                             'email': 'needy@gmail.com',
                             'verified_needy': True,
                             'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)


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
                             'subcategory_set': {
                                 1: {'id': 1, 'title': 'oil', 'category_title': 'food', 'category_id': 1},
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
                             'subcategory_set': {
                                 12: {'id': 12, 'title': 'GTA', 'category_title': 'video game', 'category_id': 4}}}
        response_5_result = {'success': '1', 'empty': 0, 'count': 2,
                             'subcategory_set': {
                                 4: {'id': 4, 'title': 'pants', 'category_title': 'clothes', 'category_id': 2},
                                 5: {'id': 5, 'title': 'shirts', 'category_title': 'clothes', 'category_id': 2}}}
        response_6_result = {'success': '1', 'empty': 0, 'count': 2,
                             'subcategory_set': {
                                 9: {'id': 9, 'title': 'printer', 'category_title': 'digital', 'category_id': 3},
                                 10: {'id': 10, 'title': 'laptop', 'category_title': 'digital', 'category_id': 3}}}
        response_7_result = {'success': '1', 'empty': 0, 'count': 2,
                             'subcategory_set': {
                                 11: {'id': 11, 'title': 'tmnt', 'category_title': 'video game', 'category_id': 4},
                                 12: {'id': 12, 'title': 'GTA', 'category_title': 'video game', 'category_id': 4}}}
        response_8_result = {'success': '1', 'empty': 0, 'count': 3,
                             'subcategory_set': {
                                 1: {'id': 1, 'title': 'oil', 'category_title': 'food', 'category_id': 1},
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
                             'product_set': {
                                 1: {'id': 1, 'title': 'ladan 1.5', 'quantity': 16, 'subcategory_title': 'oil',
                                     'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                 2: {'id': 2, 'title': 'ladan 0.9', 'quantity': 12, 'subcategory_title': 'oil',
                                     'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                 3: {'id': 3, 'title': 'aftab 1.5', 'quantity': 8, 'subcategory_title': 'oil',
                                     'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                 4: {'id': 4, 'title': 'aftab 0.9', 'quantity': 24, 'subcategory_title': 'oil',
                                     'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                 5: {'id': 5, 'title': 'bahar 1.5', 'quantity': 6, 'subcategory_title': 'oil',
                                     'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                 6: {'id': 6, 'title': 'bahar 0.9', 'quantity': 36, 'subcategory_title': 'oil',
                                     'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                 7: {'id': 7, 'title': 'mohsen', 'quantity': 20, 'subcategory_title': 'rice',
                                     'subcategory_id': 2, 'category_title': 'food', 'category_id': 1},
                                 8: {'id': 8, 'title': 'khatere', 'quantity': 32, 'subcategory_title': 'rice',
                                     'subcategory_id': 2, 'category_title': 'food', 'category_id': 1},
                                 9: {'id': 9, 'title': 'gtc', 'quantity': 28, 'subcategory_title': 'rice',
                                     'subcategory_id': 2, 'category_title': 'food', 'category_id': 1},
                                 10: {'id': 10, 'title': 'benis', 'quantity': 40, 'subcategory_title': 'rice',
                                      'subcategory_id': 2, 'category_title': 'food', 'category_id': 1},
                                 11: {'id': 11, 'title': 'orange', 'quantity': 400, 'subcategory_title': 'fruit',
                                      'subcategory_id': 3, 'category_title': 'food', 'category_id': 1},
                                 12: {'id': 12, 'title': 'apple', 'quantity': 200, 'subcategory_title': 'fruit',
                                      'subcategory_id': 3, 'category_title': 'food', 'category_id': 1},
                                 13: {'id': 13, 'title': 'banana', 'quantity': 100, 'subcategory_title': 'fruit',
                                      'subcategory_id': 3, 'category_title': 'food', 'category_id': 1},
                                 14: {'id': 14, 'title': 'watermelon', 'quantity': 800, 'subcategory_title': 'fruit',
                                      'subcategory_id': 3, 'category_title': 'food', 'category_id': 1},
                                 15: {'id': 15, 'title': 'carrot', 'quantity': 400, 'subcategory_title': 'fruit',
                                      'subcategory_id': 3, 'category_title': 'food', 'category_id': 1},
                                 16: {'id': 16, 'title': 'tomato', 'quantity': 1200, 'subcategory_title': 'fruit',
                                      'subcategory_id': 3, 'category_title': 'food', 'category_id': 1},
                                 17: {'id': 17, 'title': 'jeans', 'quantity': 50, 'subcategory_title': 'pants',
                                      'subcategory_id': 4, 'category_title': 'clothes', 'category_id': 2},
                                 18: {'id': 18, 'title': 'slash', 'quantity': 80, 'subcategory_title': 'pants',
                                      'subcategory_id': 4, 'category_title': 'clothes', 'category_id': 2},
                                 19: {'id': 19, 'title': 'sport', 'quantity': 300, 'subcategory_title': 'pants',
                                      'subcategory_id': 4, 'category_title': 'clothes', 'category_id': 2},
                                 20: {'id': 20, 'title': 'blue t-shirt', 'quantity': 250, 'subcategory_title': 'shirts',
                                      'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                 21: {'id': 21, 'title': 'white t-shirt', 'quantity': 200,
                                      'subcategory_title': 'shirts', 'subcategory_id': 5, 'category_title': 'clothes',
                                      'category_id': 2},
                                 22: {'id': 22, 'title': 'black t-shirt', 'quantity': 50, 'subcategory_title': 'shirts',
                                      'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                 23: {'id': 23, 'title': 'white shirt', 'quantity': 300, 'subcategory_title': 'shirts',
                                      'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                 24: {'id': 24, 'title': 'blue shirt', 'quantity': 400, 'subcategory_title': 'shirts',
                                      'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                 25: {'id': 25, 'title': 'black', 'quantity': 350, 'subcategory_title': 'socks',
                                      'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                 26: {'id': 26, 'title': 'white', 'quantity': 200, 'subcategory_title': 'socks',
                                      'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                 27: {'id': 27, 'title': 'blue', 'quantity': 250, 'subcategory_title': 'socks',
                                      'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                 28: {'id': 28, 'title': 'blue sport', 'quantity': 150, 'subcategory_title': 'socks',
                                      'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                 29: {'id': 29, 'title': 'red sport', 'quantity': 100, 'subcategory_title': 'socks',
                                      'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                 30: {'id': 30, 'title': 'red cap', 'quantity': 20, 'subcategory_title': 'hat',
                                      'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2},
                                 31: {'id': 31, 'title': 'black cap', 'quantity': 25, 'subcategory_title': 'hat',
                                      'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2},
                                 32: {'id': 32, 'title': 'green cap', 'quantity': 400, 'subcategory_title': 'hat',
                                      'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2},
                                 33: {'id': 33, 'title': 'blue cap', 'quantity': 60, 'subcategory_title': 'hat',
                                      'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2},
                                 34: {'id': 34, 'title': 'cowboy', 'quantity': 750, 'subcategory_title': 'hat',
                                      'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2},
                                 35: {'id': 35, 'title': 'NOKIA 1200', 'quantity': 500, 'subcategory_title': 'mobile',
                                      'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                 36: {'id': 36, 'title': 'NOKIA 1100', 'quantity': 500, 'subcategory_title': 'mobile',
                                      'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                 37: {'id': 37, 'title': 'NOKIA 6600', 'quantity': 200, 'subcategory_title': 'mobile',
                                      'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                 38: {'id': 38, 'title': 'galaxy star', 'quantity': 80, 'subcategory_title': 'mobile',
                                      'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                 39: {'id': 39, 'title': 'NOKIA X2-00', 'quantity': 2000, 'subcategory_title': 'mobile',
                                      'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                 40: {'id': 40, 'title': 'hp', 'quantity': 5, 'subcategory_title': 'printer',
                                      'subcategory_id': 9, 'category_title': 'digital', 'category_id': 3},
                                 41: {'id': 41, 'title': 'hp big', 'quantity': 3, 'subcategory_title': 'printer',
                                      'subcategory_id': 9, 'category_title': 'digital', 'category_id': 3},
                                 42: {'id': 42, 'title': 'acer', 'quantity': 20, 'subcategory_title': 'laptop',
                                      'subcategory_id': 10, 'category_title': 'digital', 'category_id': 3},
                                 43: {'id': 43, 'title': 'asus', 'quantity': 15, 'subcategory_title': 'laptop',
                                      'subcategory_id': 10, 'category_title': 'digital', 'category_id': 3},
                                 44: {'id': 44, 'title': 'hp', 'quantity': 25, 'subcategory_title': 'laptop',
                                      'subcategory_id': 10, 'category_title': 'digital', 'category_id': 3},
                                 45: {'id': 45, 'title': 'tmnt 1', 'quantity': 20, 'subcategory_title': 'tmnt',
                                      'subcategory_id': 11, 'category_title': 'video game', 'category_id': 4},
                                 46: {'id': 46, 'title': 'tmnt 2', 'quantity': 60, 'subcategory_title': 'tmnt',
                                      'subcategory_id': 11, 'category_title': 'video game', 'category_id': 4},
                                 47: {'id': 47, 'title': 'tmnt 3', 'quantity': 10, 'subcategory_title': 'tmnt',
                                      'subcategory_id': 11, 'category_title': 'video game', 'category_id': 4},
                                 48: {'id': 48, 'title': 'tmnt 4', 'quantity': 15, 'subcategory_title': 'tmnt',
                                      'subcategory_id': 11, 'category_title': 'video game', 'category_id': 4},
                                 49: {'id': 49, 'title': 'gta sa', 'quantity': 2000, 'subcategory_title': 'GTA',
                                      'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4},
                                 50: {'id': 50, 'title': 'gta vice city', 'quantity': 1500, 'subcategory_title': 'GTA',
                                      'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4},
                                 51: {'id': 51, 'title': 'gta V', 'quantity': 500, 'subcategory_title': 'GTA',
                                      'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4},
                                 52: {'id': 52, 'title': 'gta III', 'quantity': 1000, 'subcategory_title': 'GTA',
                                      'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4}}}
        response_2_result = response_1_result
        response_3_result = {'success': '1', 'empty': 0, 'count': 7,
                             'product_set': {
                                 1: {'id': 1, 'title': 'ladan 1.5', 'quantity': 16, 'subcategory_title': 'oil',
                                     'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                 2: {'id': 2, 'title': 'ladan 0.9', 'quantity': 12, 'subcategory_title': 'oil',
                                     'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                 18: {'id': 18, 'title': 'slash', 'quantity': 80, 'subcategory_title': 'pants',
                                      'subcategory_id': 4, 'category_title': 'clothes', 'category_id': 2},
                                 22: {'id': 22, 'title': 'black t-shirt', 'quantity': 50, 'subcategory_title': 'shirts',
                                      'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                 25: {'id': 25, 'title': 'black', 'quantity': 350, 'subcategory_title': 'socks',
                                      'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                 31: {'id': 31, 'title': 'black cap', 'quantity': 25, 'subcategory_title': 'hat',
                                      'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2},
                                 38: {'id': 38, 'title': 'galaxy star', 'quantity': 80, 'subcategory_title': 'mobile',
                                      'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3}}}
        response_4_result = {'success': '1', 'empty': 0, 'count': 2,
                             'product_set': {
                                 1: {'id': 1, 'title': 'ladan 1.5', 'quantity': 16, 'subcategory_title': 'oil',
                                     'subcategory_id': 1, 'category_title': 'food', 'category_id': 1},
                                 2: {'id': 2, 'title': 'ladan 0.9', 'quantity': 12, 'subcategory_title': 'oil',
                                     'subcategory_id': 1, 'category_title': 'food', 'category_id': 1}}}
        response_5_result = {'success': '1', 'empty': 0, 'count': 4,
                             'product_set': {
                                 18: {'id': 18, 'title': 'slash', 'quantity': 80, 'subcategory_title': 'pants',
                                      'subcategory_id': 4, 'category_title': 'clothes', 'category_id': 2},
                                 22: {'id': 22, 'title': 'black t-shirt', 'quantity': 50, 'subcategory_title': 'shirts',
                                      'subcategory_id': 5, 'category_title': 'clothes', 'category_id': 2},
                                 25: {'id': 25, 'title': 'black', 'quantity': 350, 'subcategory_title': 'socks',
                                      'subcategory_id': 6, 'category_title': 'clothes', 'category_id': 2},
                                 31: {'id': 31, 'title': 'black cap', 'quantity': 25, 'subcategory_title': 'hat',
                                      'subcategory_id': 7, 'category_title': 'clothes', 'category_id': 2}}}
        response_6_result = {'success': '1', 'empty': 0, 'count': 1,
                             'product_set': {
                                 18: {'id': 18, 'title': 'slash', 'quantity': 80, 'subcategory_title': 'pants',
                                      'subcategory_id': 4, 'category_title': 'clothes', 'category_id': 2}}}
        response_7_result = {'success': '1', 'empty': 1, 'count': 0,
                             'product_set': {}}
        response_8_result = {'success': '1', 'empty': 0, 'count': 4,
                             'product_set': {
                                 49: {'id': 49, 'title': 'gta sa', 'quantity': 2000, 'subcategory_title': 'GTA',
                                      'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4},
                                 50: {'id': 50, 'title': 'gta vice city', 'quantity': 1500, 'subcategory_title': 'GTA',
                                      'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4},
                                 51: {'id': 51, 'title': 'gta V', 'quantity': 500, 'subcategory_title': 'GTA',
                                      'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4},
                                 52: {'id': 52, 'title': 'gta III', 'quantity': 1000, 'subcategory_title': 'GTA',
                                      'subcategory_id': 12, 'category_title': 'video game', 'category_id': 4}}}
        response_9_result = {'success': '1', 'empty': 1, 'count': 0,
                             'product_set': {}}
        response_10_result = {'success': '1', 'empty': 0, 'count': 5,
                              'product_set': {
                                  35: {'id': 35, 'title': 'NOKIA 1200', 'quantity': 500, 'subcategory_title': 'mobile',
                                       'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                  36: {'id': 36, 'title': 'NOKIA 1100', 'quantity': 500, 'subcategory_title': 'mobile',
                                       'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                  37: {'id': 37, 'title': 'NOKIA 6600', 'quantity': 200, 'subcategory_title': 'mobile',
                                       'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                  38: {'id': 38, 'title': 'galaxy star', 'quantity': 80, 'subcategory_title': 'mobile',
                                       'subcategory_id': 8, 'category_title': 'digital', 'category_id': 3},
                                  39: {'id': 39, 'title': 'NOKIA X2-00', 'quantity': 2000,
                                       'subcategory_title': 'mobile', 'subcategory_id': 8, 'category_title': 'digital',
                                       'category_id': 3}}}
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

    def test_api_edit_category(self):
        response_1 = client_post('EditCategory', {})
        response_2 = client_post('EditCategory', {"category_id": 2})
        response_3 = client_post('EditCategory', {"title": "digital"})
        response_4 = client_post('EditCategory', {"category_id": 2, "title": "digital"})
        response_5 = client_post('EditCategory', {"category_id": 8, "title": "digital"})
        response_6 = client_post('EditCategory', {"category_id": 8, "title": "pooshaak"})
        response_7 = client_post('EditCategory', {"category_id": 2, "title": "pooshaak"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('category_id',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('title',)]",
                             'success': '0'}
        response_3_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('category_id',)]",
                             'success': '0'}
        response_4_result = {'status': 'notUniqueTitle',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = {'status': 'notUniqueTitle',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_6_result = {'status': 'categoryNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_7_result = {'message': 'category edited successfully', 'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        self.assertEqual(response_7, response_7_result)
        category = Category.objects.get(id=2)
        self.assertEqual(category.title, "pooshaak")

    def test_api_edit_subcategory(self):
        response_1 = client_post('EditSubCategory', {})
        response_2 = client_post('EditSubCategory', {"subcategory_id": 27})
        response_3 = client_post('EditSubCategory', {"subcategory_id": 8})
        response_4 = client_post('EditSubCategory', {"subcategory_id": 27, "category_id": 1})
        response_5 = client_post('EditSubCategory', {"subcategory_id": 8, "category_id": 1})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('subcategory_id',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0',
                             'message': "at least one of 'title' or 'category_id' must be passed"}
        response_3_result = {'status': 'requiredParams',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0',
                             'message': "at least one of 'title' or 'category_id' must be passed"}
        response_4_result = {'status': 'subcategoryNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = {'message': 'subcategory edited successfully',
                             'success': '1'}
        response_6_result = {'status': 'subcategoryNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_7_result = {'status': 'notUniqueTitle',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_8_result = {'message': 'subcategory edited successfully', 'success': '1'}
        response_9_result = {'message': 'subcategory edited successfully', 'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        subcategory = SubCategory.objects.get(id=8)
        category = Category.objects.get(id=1)
        self.assertEqual(subcategory.category, category)
        response_6 = client_post('EditSubCategory', {"subcategory_id": 27, "title": "phone"})
        response_7 = client_post('EditSubCategory', {"subcategory_id": 8, "title": "laptop"})
        response_8 = client_post('EditSubCategory', {"subcategory_id": 8, "title": "phone"})
        self.assertEqual(response_6, response_6_result)
        self.assertEqual(response_7, response_7_result)
        self.assertEqual(response_8, response_8_result)
        subcategory = SubCategory.objects.get(id=8)
        self.assertEqual(subcategory.title, "phone")
        response_9 = client_post('EditSubCategory', {"subcategory_id": 8, "title": "telephone", "category_id": 3})
        self.assertEqual(response_9, response_9_result)
        subcategory = SubCategory.objects.get(id=8)
        self.assertEqual(subcategory.title, "telephone")
        category = Category.objects.get(id=3)
        self.assertEqual(subcategory.category, category)

    def test_api_edit_product(self):
        response_1 = client_post('EditProduct', {})
        response_2 = client_post('EditProduct', {"product_id": 8})
        response_3 = client_post('EditProduct', {"title": "ladan 1.8"})
        response_4 = client_post('EditProduct', {"product_id": 82, "title": "ladan 1.8"})
        response_5 = client_post('EditProduct', {"product_id": 2, "title": "bahar 1.5"})
        response_6 = client_post('EditProduct', {"product_id": 8, "subcategory_id": 17})
        response_7 = client_post('EditProduct', {"product_id": 8, "title": "mashhood"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('product_id',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0',
                             'message': "at least one of 'title', 'subcategory_id' or 'quantity 'must be passed"}
        response_3_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('product_id',)]",
                             'success': '0'}
        response_4_result = {'status': 'productNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = {'status': 'notUniqueTitle',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_6_result = {'status': 'subcategoryNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_7_result = {'message': 'product edited successfully', 'success': '1'}
        response_8_result = response_7_result
        response_9_result = response_7_result
        response_10_result = response_7_result
        response_11_result = response_7_result
        response_12_result = response_7_result
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(response_5, response_5_result)
        self.assertEqual(response_6, response_6_result)
        self.assertEqual(response_7, response_7_result)
        product = Product.objects.get(id=8)
        self.assertEqual(product.title, "mashhood")
        response_8 = client_post('EditProduct', {"product_id": 8, "quantity": 400})
        self.assertEqual(response_8, response_8_result)
        product = Product.objects.get(id=8)
        self.assertEqual(product.quantity, 400)
        response_9 = client_post('EditProduct', {"product_id": 8, "subcategory_id": 8})
        self.assertEqual(response_9, response_9_result)
        product = Product.objects.get(id=8)
        subCategory = SubCategory.objects.get(id=8)
        self.assertEqual(product.subCategory, subCategory)
        response_10 = client_post('EditProduct', {"product_id": 8, "title": "NOKIA N95", "quantity": 5000})
        self.assertEqual(response_10, response_10_result)
        product = Product.objects.get(id=8)
        self.assertEqual(product.quantity, 5000)
        self.assertEqual(product.title, "NOKIA N95")
        response_11 = client_post('EditProduct',
                                  {"product_id": 8, "title": "GTA VI", "quantity": 999999, "subcategory_id": 12})
        self.assertEqual(response_11, response_11_result)
        product = Product.objects.get(id=8)
        subCategory = SubCategory.objects.get(id=12)
        self.assertEqual(product.quantity, 999999)
        self.assertEqual(product.title, "GTA VI")
        self.assertEqual(product.subCategory, subCategory)
        response_12 = client_post('EditProduct', {"product_id": 8, "title": "tmnt 2020", "subcategory_id": 11})
        self.assertEqual(response_12, response_12_result)
        product = Product.objects.get(id=8)
        subCategory = SubCategory.objects.get(id=11)
        self.assertEqual(product.title, "tmnt 2020")
        self.assertEqual(product.subCategory, subCategory)

    def test_api_delete_category(self):
        response_1 = client_post('DeleteCategory', {})
        response_2 = client_post('DeleteCategory', {"id": "four"})
        response_3 = client_post('DeleteCategory', {"id": 8})
        response_4 = client_post('DeleteCategory', {"id": 2})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('id',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'four\'",)]',
                             'success': '0'}
        response_3_result = {'status': 'categoryNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'message': 'category deleted successfully', 'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(len(Category.objects.filter(id=2)), 0)

    def test_api_delete_subcategory(self):
        response_1 = client_post('DeleteSubCategory', {})
        response_2 = client_post('DeleteSubCategory', {"id": "four"})
        response_3 = client_post('DeleteSubCategory', {"id": 26})
        response_4 = client_post('DeleteSubCategory', {"id": 2})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('id',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'four\'",)]',
                             'success': '0'}
        response_3_result = {'status': 'subcategoryNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'message': 'subcategory deleted successfully', 'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(len(SubCategory.objects.filter(id=2)), 0)

    def test_api_delete_product(self):
        response_1 = client_post('DeleteProduct', {})
        response_2 = client_post('DeleteProduct', {"id": "four"})
        response_3 = client_post('DeleteProduct', {"id": 74})
        response_4 = client_post('DeleteProduct', {"id": 2})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('id',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'four\'",)]',
                             'success': '0'}
        response_3_result = {'status': 'productNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'message': 'product deleted successfully', 'success': '1'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)
        self.assertEqual(len(Product.objects.filter(id=2)), 0)

    def test_api_the_category(self):
        response_1 = client_post('TheCategory', {})
        response_2 = client_post('TheCategory', {"id": "four"})
        response_3 = client_post('TheCategory', {"id": 8})
        response_4 = client_post('TheCategory', {"id": 2})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('id',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'four\'",)]',
                             'success': '0'}
        response_3_result = {'status': 'categoryNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'id': 2, 'title': 'clothes'}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)

    def test_api_the_subcategory(self):
        response_1 = client_post('TheSubCategory', {})
        response_2 = client_post('TheSubCategory', {"id": "four"})
        response_3 = client_post('TheSubCategory', {"id": 26})
        response_4 = client_post('TheSubCategory', {"id": 2})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('id',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'four\'",)]',
                             'success': '0'}
        response_3_result = {'status': 'subcategoryNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'id': 2, 'title': 'rice', 'category_title': 'food', 'category_id': 1}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)

    def test_api_the_product(self):
        response_1 = client_post('TheProduct', {})
        response_2 = client_post('TheProduct', {"id": "four"})
        response_3 = client_post('TheProduct', {"id": 74})
        response_4 = client_post('TheProduct', {"id": 2})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('id',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'four\'",)]',
                             'success': '0'}
        response_3_result = {'status': 'productNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'id': 2,
                             'title': 'ladan 0.9',
                             'quantity': 12,
                             'subcategory_title': 'oil',
                             'subcategory_id': 1,
                             'category_title': 'food',
                             'category_id': 1}
        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
        self.assertEqual(response_3, response_3_result)
        self.assertEqual(response_4, response_4_result)


class AdminManagementAPIsTestCase(TestCase):
    def setUp(self):
        init_db_user()

    def test_api_promoteToSuperAdmin(self):
        response_1 = client_post('PromoteToSuperAdmin', {})
        response_2 = client_post('PromoteToSuperAdmin', {"TOKEN_ID": "defaultSuperAdmin"})
        response_3 = client_post('PromoteToSuperAdmin', {"TOKEN_ID": "defaultSuperAdminLie", "username": "donator_1"})
        response_4 = client_post('PromoteToSuperAdmin', {"TOKEN_ID": "defaultAdmin", "username": "donator_1"})
        response_5 = client_post('PromoteToSuperAdmin', {"TOKEN_ID": "defaultDonator_2", "username": "donator_1"})
        response_6 = client_post('PromoteToSuperAdmin', {"TOKEN_ID": "defaultNeedy_1", "username": "donator_1"})
        response_7 = client_post('PromoteToSuperAdmin', {"TOKEN_ID": "defaultSuperAdmin", "username": "donator_3"})
        response_8 = client_post('PromoteToSuperAdmin', {"TOKEN_ID": "defaultSuperAdmin", "username": "superAdmin"})
        response_9 = client_post('PromoteToSuperAdmin', {"TOKEN_ID": "defaultSuperAdmin", "username": "admin"})
        response_10 = client_post('PromoteToSuperAdmin', {"TOKEN_ID": "defaultSuperAdmin", "username": "donator_2"})
        response_11 = client_post('PromoteToSuperAdmin', {"TOKEN_ID": "defaultSuperAdmin", "username": "needy_1"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('TOKEN_ID',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('username',)]",
                             'success': '0'}
        response_3_result = {'status': 'superAdminNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'status': 'youAreNotSuperAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = response_4_result
        response_6_result = response_4_result
        response_7_result = {'status': 'userNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_8_result = {'status': 'userIsSuperAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_9_result = {'message': 'User promoted to SuperAdmin',
                             'success': '1'}
        response_10_result = response_9_result
        response_11_result = response_9_result
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
        superAdmin = UserProfile.objects.get(token="defaultSuperAdmin")
        self.assertEqual(superAdmin.user_type, 1)
        formerly_admin = UserProfile.objects.get(token="defaultAdmin")
        self.assertEqual(formerly_admin.user_type, 1)
        formerly_donator_2 = UserProfile.objects.get(token="defaultDonator_2")
        self.assertEqual(formerly_donator_2.user_type, 1)
        formerly_needy_1 = UserProfile.objects.get(token="defaultNeedy_1")
        self.assertEqual(formerly_needy_1.user_type, 1)

    def test_api_promoteToAdmin(self):
        response_1 = client_post('PromoteToAdmin', {})
        response_2 = client_post('PromoteToAdmin', {"TOKEN_ID": "defaultSuperAdmin"})
        response_3 = client_post('PromoteToAdmin', {"TOKEN_ID": "defaultSuperAdminLie", "username": "donator_1"})
        response_4 = client_post('PromoteToAdmin', {"TOKEN_ID": "defaultAdmin", "username": "donator_1"})
        response_5 = client_post('PromoteToAdmin', {"TOKEN_ID": "defaultDonator_2", "username": "donator_1"})
        response_6 = client_post('PromoteToAdmin', {"TOKEN_ID": "defaultNeedy_1", "username": "donator_1"})
        response_7 = client_post('PromoteToAdmin', {"TOKEN_ID": "defaultSuperAdmin", "username": "donator_3"})
        response_8 = client_post('PromoteToAdmin', {"TOKEN_ID": "defaultSuperAdmin", "username": "superAdmin"})
        response_9 = client_post('PromoteToAdmin', {"TOKEN_ID": "defaultSuperAdmin", "username": "admin"})
        response_10 = client_post('PromoteToAdmin', {"TOKEN_ID": "defaultSuperAdmin", "username": "donator_2"})
        response_11 = client_post('PromoteToAdmin', {"TOKEN_ID": "defaultSuperAdmin", "username": "needy_1"})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('TOKEN_ID',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('username',)]",
                             'success': '0'}
        response_3_result = {'status': 'superAdminNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'status': 'youAreNotSuperAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = response_4_result
        response_6_result = response_4_result
        response_7_result = {'status': 'userNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_8_result = {'status': 'userIsSuperAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_9_result = {'status': 'userIsAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_10_result = {'message': 'User promoted to Admin',
                              'success': '1'}
        response_11_result = response_10_result
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
        superAdmin = UserProfile.objects.get(token="defaultSuperAdmin")
        self.assertEqual(superAdmin.user_type, 1)
        admin = UserProfile.objects.get(token="defaultAdmin")
        self.assertEqual(admin.user_type, 2)
        formerly_donator_2 = UserProfile.objects.get(token="defaultDonator_2")
        self.assertEqual(formerly_donator_2.user_type, 2)
        formerly_needy_1 = UserProfile.objects.get(token="defaultNeedy_1")
        self.assertEqual(formerly_needy_1.user_type, 2)

    def test_api_demoteAdmin(self):
        response_1 = client_post('DemoteAdmin', {})
        response_2 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultSuperAdmin"})
        response_3 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultSuperAdminLie",
                                                 "username": "donator_1",
                                                 "user_type": 3})
        response_4 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultAdmin",
                                                 "username": "donator_1",
                                                 "user_type": 3})
        response_5 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultDonator_2",
                                                 "username": "donator_1",
                                                 "user_type": 4})
        response_6 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultNeedy_1",
                                                 "username": "donator_1",
                                                 "user_type": 3})
        response_7 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultSuperAdmin",
                                                 "username": "donator_3",
                                                 "user_type": 4})
        response_8 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultSuperAdmin",
                                                 "username": "superAdmin",
                                                 "user_type": 3})
        response_9 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultSuperAdmin",
                                                 "username": "admin",
                                                 "user_type": "one"})
        response_10 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultSuperAdmin",
                                                  "username": "admin",
                                                  "user_type": "1"})
        response_11 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultSuperAdmin",
                                                  "username": "admin",
                                                  "user_type": 1})
        response_12 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultSuperAdmin",
                                                  "username": "admin",
                                                  "user_type": 3})
        response_13 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultSuperAdmin",
                                                  "username": "donator_2",
                                                  "user_type": 3})
        response_14 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultSuperAdmin",
                                                  "username": "needy_1",
                                                  "user_type": 3})
        response_1_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('TOKEN_ID',)]",
                             'success': '0'}
        response_2_result = {'status': 'requiredParams',
                             'error_type': "[<class 'django.utils.datastructures.MultiValueDictKeyError'>]",
                             'error_on': "[MultiValueDictKeyError('username',)]",
                             'success': '0'}
        response_3_result = {'status': 'superAdminNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_4_result = {'status': 'youAreNotSuperAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_5_result = response_4_result
        response_6_result = response_4_result
        response_7_result = {'status': 'userNotFound',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_8_result = {'status': 'userIsSuperAdmin',
                             'error_type': 'CUSTOM',
                             'error_on': 'CUSTOM',
                             'success': '0'}
        response_9_result = {'status': 'requiredParams',
                             'error_type': "[<class 'ValueError'>]",
                             'error_on': '[ValueError("invalid literal for int() with base 10: \'one\'",)]',
                             'success': '0'}
        response_10_result = {'status': 'dontDemoteToSuperAdmin',
                              'error_type': 'CUSTOM',
                              'error_on': 'CUSTOM',
                              'success': '0'}
        response_11_result = response_10_result
        response_12_result = {'message': 'User Demoted',
                              'success': '1'}
        response_13_result = {'status': 'userIsDonator',
                              'error_type': 'CUSTOM',
                              'error_on': 'CUSTOM',
                              'success': '0'}
        response_14_result = {'status': 'userIsNeedy',
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
        self.assertEqual(response_11, response_11_result)
        self.assertEqual(response_12, response_12_result)
        self.assertEqual(response_13, response_13_result)
        self.assertEqual(response_14, response_14_result)
        superAdmin = UserProfile.objects.get(token="defaultSuperAdmin")
        self.assertEqual(superAdmin.user_type, 1)
        formerly_admin = UserProfile.objects.get(token="defaultAdmin")
        self.assertEqual(formerly_admin.user_type, 3)
        donator_2 = UserProfile.objects.get(token="defaultDonator_2")
        self.assertEqual(donator_2.user_type, 3)
        needy_1 = UserProfile.objects.get(token="defaultNeedy_1")
        self.assertEqual(needy_1.user_type, 4)
        formerly_admin.user_type = 2
        formerly_admin.save()
        response_15 = client_post('DemoteAdmin', {"TOKEN_ID": "defaultSuperAdmin",
                                                  "username": "admin",
                                                  "user_type": 4})
        response_15_result = {'message': 'User Demoted',
                              'success': '1'}
        self.assertEqual(response_15, response_15_result)
        formerly_admin = UserProfile.objects.get(token="defaultAdmin")
        self.assertEqual(formerly_admin.user_type, 4)


class DonateAPIsTestCase(TestCase):
    def setUp(self):
        pass

    def test_api_generalDonate(self):
        pass

    def test_api_pendingDonates(self):
        pass

    def test_api_delivery(self):
        pass


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


class TransactionAPIsTestCase(TestCase):
    def setUp(self):
        pass

    def test_api_transactionList(self):
        pass

    def test_api_resentTransactionList(self):
        pass

    def test_api_biggestTransactionList(self):
        pass
