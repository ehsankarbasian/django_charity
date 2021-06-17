from django.contrib import admin
from .models import *


admin.site.register(Image)

admin.site.register(UserProfile)
admin.site.register(ExpiredTokens)

admin.site.register(Event)
admin.site.register(Transactions)
admin.site.register(DonatesIn)
admin.site.register(NeedRequest)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
