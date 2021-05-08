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
    user = models.OneToOneField(
        User,
        related_name='user',
        null=True,
        on_delete=models.CASCADE
    )
    creator = models.OneToOneField(
        User,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='The one who signed the user up'
                     + ' for the first time.+'
    )
    # TODO:image_url
    user_type = models.IntegerField(
        choices=USER_TYPE_CHOICES,
        default=-1
    )
    verified_needy = models.BooleanField(
        null=True
    )

    first_name = models.CharField(
        max_length=127,
        blank=True
    )
    last_name = models.CharField(
        max_length=127,
        blank=True
    )
    melli_code = models.CharField(
        blank=True,
        max_length=15
    )
    email = models.EmailField()
    email_tags = models.CharField(
        max_length=255,
        blank=True
    )
    verified_email = models.BooleanField(
        default=False
    )
    job = models.CharField(
        max_length=127,
        null=True,
        blank=True
    )
    address = models.TextField(
        null=True,
        blank=True
    )
    mobile_number = models.CharField(
        null=True,
        blank=True,
        max_length=31
    )
    verified_mobile = models.BooleanField(
        default=False
    )
    house_phone = models.CharField(
        max_length=31,
        null=True,
        blank=True
    )
    workplace_phone = models.CharField(
        max_length=31,
        null=True,
        blank=True
    )
    gender = models.BooleanField(
        choices=GENDER_CHOICES,
        null=True,
        default=1
    )
    married = models.BooleanField(
        blank=True,
        null=True,
        choices=MARRIED_CHOICES,
        default=0
    )
    birth_date = models.DateField(
        null=True,
        blank=True
    )
    signup_date = models.DateTimeField(
        auto_now=True
    )
    completed = models.BooleanField(
        default=False
    )
    reset_pass_token = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        default=""
    )
    reset_pass_code = models.IntegerField(
        null=True,
        blank=True
    )
    verify_email_token = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    verify_email_code = models.IntegerField(
        null=True,
        blank=True
    )
    token = models.CharField(
        max_length=128,
        null=True,
        default=""
    )

    def __str__(self):
        return "type:" + str(self.user_type) + " / email:" + self.email + " / username:" + self.user.username


class Event(models.Model):
    STATUS_CHOICES = [
        (0, 'no feedback'),
        (1, 'accepted'),
        (-1, 'failed'),
    ]

    title = models.CharField(
        max_length=128,
        default="",
        null=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    list_of_needs = models.TextField(
        null=True,
        blank=True
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='creator'
    )
    enabled = models.BooleanField(
        default=False,
    )
    create_date = models.DateField(
        auto_now=True
    )
    status = models.IntegerField(
        default=0,
        choices=STATUS_CHOICES
    )
    image_url = models.CharField(
        max_length=512,
        null=True,
        blank=True
    )
    feedback = models.TextField(
        default="",
        null=True
    )
    edited = models.BooleanField(
        default=False
    )
    edited_by = models.IntegerField(
        # The super admin PROFILE id
        default=-1
    )

    def __str__(self):
        return "Title:" + self.title

class StoreCategory(models.Model):
    title = models.CharField(
    null = True,
    blank = True,
    max_length = 127,
    default = ""
    )
     def __str__(self):
        return "Title:" + self.title

class StoreSubCategory(models.Model):
    title = models.CharField(
        null = True,
        blank = True,
        max_length = 127,
        default = ""
    )

    category = models.ForeignKey(
        StoreCategory,
        null = False,

    )


    def __str__(self):
         return "Title:" + self.title

class StoreProduct(models.Model):
    title = models.CharField(
        null = False,
        blank = False,
        max_length = 127
    )

    quantity = models.IntegerField(
        null = True,
        default = 0
    )

    subCategory = models.ForeignKey(
        StoreSubCategory,
        null = False
    )

    def __str__(self):
        return  "Title:" + self.title + " / Quantity:" + self.quantity

class DonatesIn(models.Model):
    quantity = models.IntegerField(
        null=True,
        default = -1
    )

    product = models.ForeignKey(
        StoreProduct,
        null = False
    )

    #transaction

    event = models.ForeignKey(
        Event,
        null = True
    )

    donator = models.ForeignKey(
        User,
        null = False
    )

    create_date = models.DateField(
        auto_now=True
    )

    #DeliveredTo

    #ExpDate?

#class DonatesOut(models.Model):

