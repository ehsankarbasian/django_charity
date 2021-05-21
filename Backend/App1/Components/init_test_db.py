from App1.models import *


def init_db_user():
    """
    initials the default database for User and UserProfile
    """

    superAdminUser = User.objects.create_user(username="superAdmin",
                                              email="superAdmin@gmail.com",
                                              password="12345")
    adminUser = User.objects.create_user(username="admin",
                                         email="admin@gmail.com",
                                         password="12345")
    donatorUser_1 = User.objects.create_user(username="donator_1",
                                             email="donator_1@gmail.com",
                                             password="12345")
    donatorUser_2 = User.objects.create_user(username="donator_2",
                                             email="donator_2@gmail.com",
                                             password="12345")
    needyUser_1 = User.objects.create_user(username="needy_1",
                                           email="needy@gmail.com",
                                           password="12345")

    UserProfile.objects.create(user=superAdminUser,
                               email=superAdminUser.email,
                               token="defaultSuperAdmin",
                               email_tags="",
                               user_type=1,
                               verify_email_code=2500,
                               verify_email_token="verifyEmailToken")
    UserProfile.objects.create(user=adminUser,
                               email=adminUser.email,
                               token="defaultAdmin",
                               email_tags="",
                               user_type=2,
                               verify_email_code=2500,
                               verify_email_token="verifyEmailToken")
    UserProfile.objects.create(user=donatorUser_1,
                               email=donatorUser_1.email,
                               token="defaultDonator_1",
                               email_tags="",
                               user_type=3,
                               verify_email_code=2500,
                               verify_email_token="verifyEmailToken")
    UserProfile.objects.create(user=donatorUser_2,
                               email=donatorUser_2.email,
                               token="defaultDonator_2",
                               email_tags="",
                               user_type=3,
                               verify_email_code=2500,
                               verify_email_token="verifyEmailToken")
    UserProfile.objects.create(user=needyUser_1,
                               email=needyUser_1.email,
                               token="defaultNeedy_1",
                               email_tags="",
                               user_type=4,
                               verify_email_code=2500,
                               verify_email_token="verifyEmailToken")


def init_db_event():
    """
    initials the default database for Event
    """
    pass


def init_db_profile():
    """
    initials the default database for userProfiles
    """
    superAdminUser = User.objects.get(username="superAdmin")
    adminUser = User.objects.get(username="admin")
    superAdminProfile = UserProfile.objects.get(user=superAdminUser)
    adminProfile = UserProfile.objects.get(user=adminUser)

    superAdminProfile.first_name = "super admin first name"
    superAdminProfile.last_name = "super admin last name"
    superAdminProfile.melli_code = "1232500"
    superAdminProfile.job = "the super admin of NTM charity"
    superAdminProfile.address = "ntm charity"
    superAdminProfile.mobile_number = "09132224444"
    superAdminProfile.house_phone = "02152254444"
    superAdminProfile.workplace_phone = "02152253333"
    superAdminProfile.gender = 1
    superAdminProfile.married = 0
    superAdminProfile.birth_date = "2021-01-23"
    superAdminProfile.verified = True
    superAdminProfile.verified_mobile = False
    superAdminProfile.verified_email = True
    superAdminProfile.completed = True
    superAdminProfile.save()

    adminProfile.first_name = "admin first name"
    adminProfile.last_name = "admin last name"
    adminProfile.melli_code = "1234444"
    adminProfile.job = "the admin of NTM charity"
    adminProfile.address = "ntm charity"
    adminProfile.mobile_number = "09132225555"
    adminProfile.house_phone = "02152256666"
    adminProfile.workplace_phone = "02152254444"
    adminProfile.gender = 0
    adminProfile.married = 1
    adminProfile.birth_date = "2020-08-11"
    adminProfile.verified = True
    adminProfile.verified_mobile = True
    adminProfile.verified_email = True
    adminProfile.completed = True
    adminProfile.save()


def init_db_donateIn():
    """
    initials the default database for DonatesIn and Transactions
    """
    pass


def init_db_storeManagement():
    """
    initials the default database for Product, Category and SubCategory
    """

    food = Category.objects.create(title="food")
    clothes = Category.objects.create(title="clothes")
    digital = Category.objects.create(title="digital")
    video_game = Category.objects.create(title="video game")

    oil = SubCategory.objects.create(title="oil", category=food)
    rice = SubCategory.objects.create(title="rice", category=food)
    fruit = SubCategory.objects.create(title="fruit", category=food)
    pants = SubCategory.objects.create(title="pants", category=clothes)
    shirts = SubCategory.objects.create(title="shirts", category=clothes)
    socks = SubCategory.objects.create(title="socks", category=clothes)
    hat = SubCategory.objects.create(title="hat", category=clothes)
    mobile = SubCategory.objects.create(title="mobile", category=digital)
    printer = SubCategory.objects.create(title="printer", category=digital)
    laptop = SubCategory.objects.create(title="laptop", category=digital)
    tmnt = SubCategory.objects.create(title="tmnt", category=video_game)
    gta = SubCategory.objects.create(title="GTA", category=video_game)

    Product.objects.create(title="ladan 1.5", subCategory=oil, quantity=16)
    Product.objects.create(title="ladan 0.9", subCategory=oil, quantity=12)
    Product.objects.create(title="aftab 1.5", subCategory=oil, quantity=8)
    Product.objects.create(title="aftab 0.9", subCategory=oil, quantity=24)
    Product.objects.create(title="bahar 1.5", subCategory=oil, quantity=6)
    Product.objects.create(title="bahar 0.9", subCategory=oil, quantity=36)

    Product.objects.create(title="mohsen", subCategory=rice, quantity=20)
    Product.objects.create(title="khatere", subCategory=rice, quantity=32)
    Product.objects.create(title="gtc", subCategory=rice, quantity=28)
    Product.objects.create(title="benis", subCategory=rice, quantity=40)

    Product.objects.create(title="orange", subCategory=fruit, quantity=400)
    Product.objects.create(title="apple", subCategory=fruit, quantity=200)
    Product.objects.create(title="banana", subCategory=fruit, quantity=100)
    Product.objects.create(title="watermelon", subCategory=fruit, quantity=800)
    Product.objects.create(title="carrot", subCategory=fruit, quantity=400)
    Product.objects.create(title="tomato", subCategory=fruit, quantity=1200)

    Product.objects.create(title="jeans", subCategory=pants, quantity=50)
    Product.objects.create(title="slash", subCategory=pants, quantity=80)
    Product.objects.create(title="sport", subCategory=pants, quantity=300)

    Product.objects.create(title="blue t-shirt", subCategory=shirts, quantity=250)
    Product.objects.create(title="white t-shirt", subCategory=shirts, quantity=200)
    Product.objects.create(title="black t-shirt", subCategory=shirts, quantity=50)
    Product.objects.create(title="white shirt", subCategory=shirts, quantity=300)
    Product.objects.create(title="blue shirt", subCategory=shirts, quantity=400)

    Product.objects.create(title="black", subCategory=socks, quantity=350)
    Product.objects.create(title="white", subCategory=socks, quantity=200)
    Product.objects.create(title="blue", subCategory=socks, quantity=250)
    Product.objects.create(title="blue sport", subCategory=socks, quantity=150)
    Product.objects.create(title="red sport", subCategory=socks, quantity=100)

    Product.objects.create(title="red cap", subCategory=hat, quantity=20)
    Product.objects.create(title="black cap", subCategory=hat, quantity=25)
    Product.objects.create(title="green cap", subCategory=hat, quantity=400)
    Product.objects.create(title="blue cap", subCategory=hat, quantity=60)
    Product.objects.create(title="cowboy", subCategory=hat, quantity=750)

    Product.objects.create(title="NOKIA 1200", subCategory=mobile, quantity=500)
    Product.objects.create(title="NOKIA 1100", subCategory=mobile, quantity=500)
    Product.objects.create(title="NOKIA 6600", subCategory=mobile, quantity=200)
    Product.objects.create(title="galaxy star", subCategory=mobile, quantity=80)
    Product.objects.create(title="NOKIA X2-00", subCategory=mobile, quantity=2000)

    Product.objects.create(title="hp", subCategory=printer, quantity=5)
    Product.objects.create(title="hp big", subCategory=printer, quantity=3)

    Product.objects.create(title="acer", subCategory=laptop, quantity=20)
    Product.objects.create(title="asus", subCategory=laptop, quantity=15)
    Product.objects.create(title="hp", subCategory=laptop, quantity=25)

    Product.objects.create(title="tmnt 1", subCategory=tmnt, quantity=20)
    Product.objects.create(title="tmnt 2", subCategory=tmnt, quantity=60)
    Product.objects.create(title="tmnt 3", subCategory=tmnt, quantity=10)
    Product.objects.create(title="tmnt 4", subCategory=tmnt, quantity=15)

    Product.objects.create(title="gta sa", subCategory=gta, quantity=2000)
    Product.objects.create(title="gta vice city", subCategory=gta, quantity=1500)
    Product.objects.create(title="gta V", subCategory=gta, quantity=500)
    Product.objects.create(title="gta III", subCategory=gta, quantity=1000)
