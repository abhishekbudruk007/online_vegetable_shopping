from django.contrib import admin
from django.urls import path
from . import views
app_name = "dashboard"
urlpatterns = [
    # path('', views.Home,name="home"),
    path('home/', views.HomePageCBV.as_view(),name="home")
]
