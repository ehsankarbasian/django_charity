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
            (1, 'married'),
            (0, 'not married')
            ]
    
    # Attributes:
    user = models.OneToOneField(
            User,
            related_name = 'user',
            default = -1,
            on_delete = models.CASCADE
            )
    creator = models.OneToOneField(
            User,
            null = True,
            on_delete = models.DO_NOTHING,
            related_name = 'The one who signed the user up'
                                   + ' for the first time.+'
            )
    user_type = models.IntegerField(
            choices = USER_TYPE_CHOICES
            )
    verified_needy = models.BooleanField(
            null = True
            )
    
    first_name = models.CharField(
            max_length = 127,
            blank = True
            )
    last_name = models.CharField(
            max_length = 127,
            blank = True
            )
    melli_code = models.CharField(
            max_length = 15
            )
    email = models.EmailField()
    verified_email = models.BooleanField(
            default = False
            )
    job = models.CharField(
            max_length = 127,
            blank = True
            )
    address = models.TextField(
            blank = True
            )
    mobile_number = models.CharField(
            max_length = 31
            )
    verified_mobile = models.BooleanField(
            default = False
            )
    house_phone = models.CharField(
            max_length = 31,
            blank = True
            )
    workplace_phone = models.CharField(
            max_length = 31,
            blank = True
            )
    gender = models.BooleanField(
            choices = GENDER_CHOICES
            )
    married = models.BooleanField(
            blank = True,
            choices = MARRIED_CHOICES
            )
    birth_date = models.DateField(
            blank = True
            )
    signup_date = models.DateTimeField(
            auto_now = True
            )
    
    def __str__(self):
        return "TODO"