from App1.models import *


def init_db_user():
    """
    initials the default database for User and UserProfile
    """


def init_db_event():
    """
    initials the default database for Event
    """
    pass


def init_db_donateIn():
    """
    initials the default database for DonatesIn and Transactions
    """
    pass


def init_db_storeManagement():
    """
    initials the default database for Product, Category and SubCategory
    """
    print("ABBAS BUAZAR")
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
