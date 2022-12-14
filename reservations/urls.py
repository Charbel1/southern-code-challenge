"""reservations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

import core.views.booking_view
import core.views.pricing_rule_view
import core.views.property_view
from core.views.user_view import UserCrud

property = [
        path('get_modify_delete_one_property/<int:id>',
             core.views.property_view.GetModifyDeleteOnePropertyDataView.as_view()),
        path('get_all_property/', core.views.property_view.GetAllPropertyDataView.as_view()),
        path('create_property/', core.views.property_view.PropertyCreateView.as_view()),

        ]

pricing_rule = [
        path('get_pricing_rule/<int:property_id>', core.views.pricing_rule_view.GetPrincingRulePropertyView.as_view()),

        path('create_pricing_rule/', core.views.pricing_rule_view.CreatePrincingRulePropertyView.as_view()),

        path('get_one_pricing_rule/<int:pricing_id>',
             core.views.pricing_rule_view.GetOnePrincingRulePropertyView.as_view()),

        path('delete_one_pricing_rule/<int:pricing_id>', core.views.pricing_rule_view
             .DeleteOnePricingRuleProperty.as_view()),

        path('update_one_pricing_rule/', core.views.pricing_rule_view
             .UpdateOnePricingRuleProperty.as_view()),

        ]

booking = [
    path('create_booking/', core.views.booking_view.SetBookingView.as_view()),
    path('get_booking_by_property/<int:property_id>', core.views.booking_view.GetBookingPropertyView.as_view()),
    path('get_all_booking/', core.views.booking_view.GetAllBookingView.as_view()),
    path('get_booking/<int:booking_id>', core.views.booking_view.GetBookingByIdView.as_view())
        ]

user = [
        path('login/', obtain_auth_token),
        path('create_user',UserCrud.as_view())

        ]
urlpatterns = [
    path('admin/', admin.site.urls),



]
urlpatterns = urlpatterns+booking+pricing_rule+property+user
