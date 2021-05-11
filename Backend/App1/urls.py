from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('signup', views.signup),
    path('logout', views.logout),
    path('ForgotPassword', views.forgotPassword),
    path('LoadUserProfile', views.loadUserProfile),
    path('SubmitUserProfile', views.submitUserProfile),
    path('UserBio', views.userBio),
    path('SendEmail', views.email),

    path('CreateEvent', views.createEvent),
    path('GetEventRequested', views.requestedEventList),
    path('EditEventByAdmin', views.editEventByAdmin),
    path('EditEventByUser', views.editEventByUser),
    path('LeaveFeedback', views.leaveFeedback),
    path('DisableEvent', views.disableEvent),
    path('Search', views.search),
    path('UserEvent', views.userEvent),
    path('DeleteEvent', views.deleteEvent),
    path('NotVerifiedUserSet', views.notVerifiedUserSet),
    path('VerifyOrRejectUser', views.verifyOrRejectUser),
    path('DonateMoney', views.donate_money),


    # StoreManagement urls:
    path('CreateCategory', views.create_category),
    path('CreateSubCategory', views.create_subcategory),
    path('CreateProduct', views.create_product),

    path('CategoryList', views.category_list),
    path('SubCategoryList', views.subcategory_list),
    path('ProductList', views.product_list),

    path('EditCategory', views.edit_category),
    path('EditSubCategory', views.edit_subcategory),
    path('EditProduct', views.edit_product),

    path('DeleteCategory', views.delete_category),
    path('DeleteSubCategory', views.delete_subcategory),
    path('DeleteProduct', views.delete_product),

    path('TheCategory', views.the_category),
    path('TheSubCategory', views.the_subcategory),
    path('TheProduct', views.the_product),
]
