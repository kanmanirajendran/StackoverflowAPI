from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [

url("stack_overflow",views.stack_overflow,name="stack_overflow"),


]
