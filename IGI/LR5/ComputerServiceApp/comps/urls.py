from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .crud_views import (
    ServiceTypeListView, ServiceTypeCreateView, ServiceTypeUpdateView, ServiceTypeDeleteView,
    ServiceListView, ServiceCreateView, ServiceUpdateView, ServiceDeleteView,
    DeviceTypeListView, DeviceTypeCreateView, DeviceTypeUpdateView, DeviceTypeDeleteView,
    DeviceListView, DeviceCreateView, DeviceUpdateView, DeviceDeleteView,
    SparePartTypeListView, SparePartTypeCreateView, SparePartTypeUpdateView, SparePartTypeDeleteView,
    SparePartListView, SparePartCreateView, SparePartUpdateView, SparePartDeleteView
)

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
    path('orders/employee/', views.order_list_employee, name='order_list_employee'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/client/', views.order_list_client, name='order_list_client'),
]


urlpatterns += [
    # ServiceType CRUD
    path('types/service/', ServiceTypeListView.as_view(), name='service_type_list'),
    path('types/service/add/', ServiceTypeCreateView.as_view(), name='service_type_add'),
    path('types/service/<int:pk>/edit/', ServiceTypeUpdateView.as_view(), name='service_type_edit'),
    path('types/service/<int:pk>/delete/', ServiceTypeDeleteView.as_view(), name='service_type_delete'),

    # Service CRUD
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/add/', ServiceCreateView.as_view(), name='service_add'),
    path('services/<int:pk>/edit/', ServiceUpdateView.as_view(), name='service_edit'),
    path('services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),

    # DeviceType CRUD
    path('types/device/', DeviceTypeListView.as_view(), name='device_type_list'),
    path('types/device/add/', DeviceTypeCreateView.as_view(), name='device_type_add'),
    path('types/device/<int:pk>/edit/', DeviceTypeUpdateView.as_view(), name='device_type_edit'),
    path('types/device/<int:pk>/delete/', DeviceTypeDeleteView.as_view(), name='device_type_delete'),

    # Device CRUD
    path('devices/', DeviceListView.as_view(), name='device_list'),
    path('devices/add/', DeviceCreateView.as_view(), name='device_add'),
    path('devices/<int:pk>/edit/', DeviceUpdateView.as_view(), name='device_edit'),
    path('devices/<int:pk>/delete/', DeviceDeleteView.as_view(), name='device_delete'),

    # SparePartType CRUD
    path('types/part/', SparePartTypeListView.as_view(), name='spareparttype_list'),
    path('types/part/add/', SparePartTypeCreateView.as_view(), name='spareparttype_add'),
    path('types/part/<int:pk>/edit/', SparePartTypeUpdateView.as_view(), name='spareparttype_edit'),
    path('types/part/<int:pk>/delete/', SparePartTypeDeleteView.as_view(), name='spareparttype_delete'),

    # SparePart CRUD
    path('parts/', SparePartListView.as_view(), name='sparepart_list'),
    path('parts/add/', SparePartCreateView.as_view(), name='sparepart_add'),
    path('parts/<int:pk>/edit/', SparePartUpdateView.as_view(), name='sparepart_edit'),
    path('parts/<int:pk>/delete/', SparePartDeleteView.as_view(), name='sparepart_delete'),
]
