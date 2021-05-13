from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Transactions)
admin.site.register(DonatesIn)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
