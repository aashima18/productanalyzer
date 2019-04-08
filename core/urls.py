from django.urls import path
from . import views
from .views import ABC, SignUp, spider

urlpatterns = [

    path('',ABC.as_view(),name='abc'),
    path('spider', spider,name='spider'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]