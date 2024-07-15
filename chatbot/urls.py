from django.urls import path
from chatbot.views import *
urlpatterns = [
    path('', login, name='first_login'),
    path('chatbot/', chatbot, name='chatbot'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
]
