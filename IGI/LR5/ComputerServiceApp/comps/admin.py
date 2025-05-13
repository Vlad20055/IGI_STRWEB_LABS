from django.contrib import admin
from .models import Service, ServiceType, Order, Client, Employee, Specialization, SparePart, SparePartType, Device, DeviceType

#Register your models here
admin.site.register([ServiceType, Service, Order, Client, Employee,
                     Specialization, SparePartType, SparePart,
                     DeviceType, Device])