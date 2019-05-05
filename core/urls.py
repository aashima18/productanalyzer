from django.urls import path
from . import views
from .views import ABC, SignUp, spider, graph, index, about, contact, feedback


urlpatterns = [

    path('home',ABC.as_view(),name='abc'),
    path('spider', spider,name='spider'),
    path('graph', graph,name='graph'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('',index,name="index"),
    path('about',about,name="about"),
    path('contact',contact,name="contact"),
    path('contactform',feedback, name='contactform'),
    
]