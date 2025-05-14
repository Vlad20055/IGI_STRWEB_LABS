from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('news/', views.news_list, name='news_list'),
    path('faq/', views.faq_list, name='faq_list'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('vacancies/', views.vacancy_list, name='vacancy_list'),
    path('signup/master/', views.signup_master, name='signup_master'),
    path('signup/client/', views.signup_client, name='signup_client'),
]