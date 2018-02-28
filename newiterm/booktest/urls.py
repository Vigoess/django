
from django.conf.urls import include, url
from django.contrib import admin

from booktest import views

urlpatterns = [
    url(r'^index$',views.index),
    url(r'^test_join$',views.test_join),
    url(r'^test_join1$',views.test_join1),
    url(r'^testself$',views.testself),
    url(r'^test_var$',views.test_var),
    url(r'^show_book$',views.show_book),
    url(r'^extend_show$',views.extend_show),
    url(r'^escape_show$',views.escape_show),
    url(r'^verify_code$',views.verify_code),
    url(r'^verify_show$',views.verify_show),
    url(r'^check_verify$',views.check_verify),
    url(r'^fan1$',views.fan1,name='adc'),
    url(r'^fan2_show$',views.fan2,name='fan2'),
    url(r'^fan3$',views.fan3),
    # url(r'^fan_test/(\d+)_(\w+)_(\w+)$',views.fan_test,name='fan_test'),
    url(r'^fan_test/(?P<age>\d+)_(?P<name>\w+)_(?P<gender>\w+)$',views.fan_test,name='fan_test'),
]
