from django.urls import re_path
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .crud_views import (
    ServiceTypeCreateView, ServiceTypeUpdateView, ServiceTypeDeleteView,
    ServiceCreateView, ServiceUpdateView, ServiceDeleteView,
    DeviceTypeCreateView, DeviceTypeUpdateView, DeviceTypeDeleteView,
    DeviceCreateView, DeviceUpdateView, DeviceDeleteView,
    SparePartTypeCreateView, SparePartTypeUpdateView, SparePartTypeDeleteView,
    SparePartCreateView, SparePartUpdateView, SparePartDeleteView
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
    path('contacts_admin/', views.contacts_admin, name='contacts_admin'),
    path('orders/employee/', views.order_list_employee, name='order_list_employee'),
    path('orders/create/', views.order_create, name='order_create'),
    re_path(r'^orders/(?P<number>ORD-[A-F0-9]{8})/$', views.order_detail_by_number, name='order_detail_by_number'),
    path('orders/client/', views.order_list_client, name='order_list_client'),
    path('special/', views.special, name='special'),
    path('statistic/', views.statistic, name='statistic'),
    path('company-statistic/', views.company_statistic, name='company_statistic'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/add/', views.review_create, name='review_create'),
    path('coupons/', views.coupon_list, name='coupon_list'),
    path('types_services_spareparts_devices/', views.types_services_spareparts_devices, name='types_services_spareparts_devices'),
    path('detail/<str:model_type>/<int:pk>/', views.UniversalDetailView.as_view(), name='detail_services_spareparts'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add_sparepart/<int:sparepart_id>/', views.add_sparepart_to_cart, name='add_sparepart_to_cart'),
    path('cart/update_sparepart/<int:sparepart_id>/', views.update_sparepart_quantity, name='update_sparepart_quantity'),
    path('cart/remove_sparepart/<int:sparepart_id>/', views.remove_sparepart_from_cart, name='remove_sparepart_from_cart'),
    path('cart/add_service/<int:service_id>/', views.add_service_to_cart, name='add_service_to_cart'),
    path('cart/update_service/<int:service_id>/', views.update_service_quantity, name='update_service_quantity'),
    path('cart/remove_service/<int:service_id>/', views.remove_service_from_cart, name='remove_service_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
]


urlpatterns += [
    # ServiceType CUD
    path('types/service/add/', ServiceTypeCreateView.as_view(), name='service_type_add'),
    path('types/service/<int:pk>/edit/', ServiceTypeUpdateView.as_view(), name='service_type_edit'),
    path('types/service/<int:pk>/delete/', ServiceTypeDeleteView.as_view(), name='service_type_delete'),

    # Service CUD
    path('services/add/', ServiceCreateView.as_view(), name='service_add'),
    path('services/<int:pk>/edit/', ServiceUpdateView.as_view(), name='service_edit'),
    path('services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),

    # DeviceType CUD
    path('types/device/add/', DeviceTypeCreateView.as_view(), name='device_type_add'),
    path('types/device/<int:pk>/edit/', DeviceTypeUpdateView.as_view(), name='device_type_edit'),
    path('types/device/<int:pk>/delete/', DeviceTypeDeleteView.as_view(), name='device_type_delete'),

    # Device CUD
    path('devices/add/', DeviceCreateView.as_view(), name='device_add'),
    path('devices/<int:pk>/edit/', DeviceUpdateView.as_view(), name='device_edit'),
    path('devices/<int:pk>/delete/', DeviceDeleteView.as_view(), name='device_delete'),

    # SparePartType CUD
    path('types/part/add/', SparePartTypeCreateView.as_view(), name='spareparttype_add'),
    path('types/part/<int:pk>/edit/', SparePartTypeUpdateView.as_view(), name='spareparttype_edit'),
    path('types/part/<int:pk>/delete/', SparePartTypeDeleteView.as_view(), name='spareparttype_delete'),

    # SparePart CUD
    path('parts/add/', SparePartCreateView.as_view(), name='sparepart_add'),
    path('parts/<int:pk>/edit/', SparePartUpdateView.as_view(), name='sparepart_edit'),
    path('parts/<int:pk>/delete/', SparePartDeleteView.as_view(), name='sparepart_delete'),
]
