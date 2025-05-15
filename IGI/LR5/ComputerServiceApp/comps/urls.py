from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('news/', views.news_list, name='news_list'),
    path('faq/', views.faq_list, name='faq_list'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('vacancies/', views.vacancy_list, name='vacancy_list'),
    path('signup/client/', views.signup_client, name='signup_client'),
    path('login/', auth_views.LoginView.as_view(template_name='comps/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_list, name='order_list'),
]