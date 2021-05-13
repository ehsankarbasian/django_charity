from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    # Statics:
    USER_TYPE_CHOICES = [
        (1, 'Super admin'),
        (2, 'Admin'),
        (3, 'Donator'),
        (4, 'Needy')
    ]
    GENDER_CHOICES = [
        (1, 'male'),
        (0, 'female')
    ]
    MARRIED_CHOICES = [
        (0, 'not married'),
        (1, 'married')
    ]

    # Attributes:
    # TODO:image_url
    user = models.OneToOneField(User, related_name='user', null=True, on_delete=models.CASCADE)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=-1)
    verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=127, blank=True)
    last_name = models.CharField(max_length=127, blank=True)
    melli_code = models.CharField(blank=True, max_length=15)
    email = models.EmailField()
    email_tags = models.CharField(max_length=255, blank=True)
    verified_email = models.BooleanField(default=False)
    job = models.CharField(max_length=127, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    mobile_number = models.CharField(null=True, blank=True, max_length=31)
    verified_mobile = models.BooleanField(default=False)
    house_phone = models.CharField(max_length=31, null=True, blank=True)
    workplace_phone = models.CharField(max_length=31, null=True, blank=True)
    gender = models.BooleanField(choices=GENDER_CHOICES, null=True, default=1)
    married = models.BooleanField(blank=True, null=True, choices=MARRIED_CHOICES, default=0)
    birth_date = models.DateField(null=True, blank=True)
    signup_date = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    reset_pass_token = models.CharField(max_length=128, null=True, blank=True, default="")
    reset_pass_code = models.IntegerField(null=True, blank=True)
    verify_email_token = models.CharField(max_length=128, null=True, blank=True)
    verify_email_code = models.IntegerField(null=True, blank=True)
    token = models.CharField(max_length=128, null=True, default="")

    def __str__(self):
        return "type:" + str(self.user_type) + " / email:" + self.email + " / username:" + self.user.username


class Event(models.Model):
    STATUS_CHOICES = [
        (0, 'no feedback'),
        (1, 'accepted'),
        (-1, 'failed'),
    ]

    title = models.CharField(max_length=128, default="", null=True)
    description = models.TextField(null=True, blank=True)
    list_of_needs = models.TextField(null=True, blank=True)
    money_target = models.IntegerField(default=0)
    donated_money = models.IntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='creator')
    enabled = models.BooleanField(default=False, )
    create_date = models.DateField(auto_now=True)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    feedback = models.TextField(default="", null=True)
    edited = models.BooleanField(default=False)
    edited_by = models.IntegerField(default=-1)  # The super admin PROFILE id

    def to_money_target(self):
        if self.donated_money - self.money_target >= 0:
            return 0
        else:
            return self.money_target - self.donated_money

    def __str__(self):
        return "Title:" + self.title


class Category(models.Model):
    title = models.CharField(null=True, blank=True, max_length=127, default="")

    def __str__(self):
        return "Title: " + self.title


class SubCategory(models.Model):
    title = models.CharField(null=True, blank=True, max_length=127, default="")
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return "(" + self.category.title + ") Title: " + self.title


class Product(models.Model):
    title = models.CharField(null=False, blank=False, max_length=127)
    quantity = models.IntegerField(null=True, default=0)
    subCategory = models.ForeignKey(SubCategory, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.subCategory.category.title + " > " + self.subCategory.title + \
               " > Title: " + self.title + " / Quantity: " + str(self.quantity)


class Transactions(models.Model):
    # If is In, boolean will be true and if it is out,boolean will be false

    is_in = models.BooleanField(default=True)
    amount = models.IntegerField(null=False, default=0)
    create_date = models.DateTimeField(auto_now=True)
    donatorOrNeedy = models.ForeignKey(UserProfile, null=False, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Amount: " + str(self.amount) + \
               " / Is in? :" + str(self.is_in) + \
               " / From: " + str(self.donatorOrNeedy.user.username)


class DonatesIn(models.Model):
    quantity = models.IntegerField(null=True, default=-1)
    product = models.ForeignKey(Product, null=True, on_delete=models.DO_NOTHING)
    transaction = models.ForeignKey(Transactions, null=True, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, null=True, on_delete=models.DO_NOTHING)
    donator = models.ForeignKey(UserProfile, null=False, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    # DeliveredTo (optional)
    # ExpDate (optional)

    def __str__(self):
        return "Quantity: " + str(self.quantity) + " / Amount: " + str(self.transaction.amount)


class DonatesOut(models.Model):
    quantity = models.IntegerField(
        null=True,
        default=-1
    )
    create_date = models.DateTimeField(
        auto_now=True
    )
    delivered_to = models.ForeignKey(
        UserProfile,
        null=False,
        blank=False,
        related_name='needy',
        on_delete=models.DO_NOTHING
    )
    delivered_by = models.ForeignKey(
        UserProfile,
        null=False,
        blank=False,
        related_name='admin',
        on_delete=models.DO_NOTHING
    )
