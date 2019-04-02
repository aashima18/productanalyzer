from django.urls import path
from . import views
from .views import ABC, SignUp

urlpatterns = [

    path('',ABC.as_view(),name='abc'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]