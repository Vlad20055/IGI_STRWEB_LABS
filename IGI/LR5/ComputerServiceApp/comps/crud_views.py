# comps/crud_views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import (
    ServiceType, Service,
    DeviceType, Device,
    SparePartType, SparePart
)

import logging
logger = logging.getLogger('custom')

class EmployeeRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Employees').exists()

# === ServiceType CUD ===
class ServiceTypeCreateView(EmployeeRequiredMixin, CreateView):
    model = ServiceType
    fields = ['name']
    template_name = 'comps/crud_views/service_type_form.html'
    success_url = reverse_lazy('types_services_spareparts')


class ServiceTypeUpdateView(EmployeeRequiredMixin, UpdateView):
    model = ServiceType
    fields = ['name']
    template_name = 'comps/crud_views/service_type_form.html'
    success_url = reverse_lazy('types_services_spareparts')


class ServiceTypeDeleteView(EmployeeRequiredMixin, DeleteView):
    model = ServiceType
    template_name = 'comps/crud_views/service_type_confirm_delete.html'
    success_url = reverse_lazy('types_services_spareparts')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # все сервисы, которые будут удалены вместе с этим типом
        ctx['related_services'] = self.object.services.all()
        return ctx

# === Service CUD ===
class ServiceCreateView(EmployeeRequiredMixin, CreateView):
    model = Service
    fields = ['type', 'name', 'description', 'price']
    template_name = 'comps/crud_views/service_form.html'
    success_url = reverse_lazy('home')


class ServiceUpdateView(EmployeeRequiredMixin, UpdateView):
    model = Service
    fields = ['type', 'name', 'description', 'price']
    template_name = 'comps/crud_views/service_form.html'
    success_url = reverse_lazy('home')


class ServiceDeleteView(EmployeeRequiredMixin, DeleteView):
    model = Service
    template_name = 'comps/crud_views/service_confirm_delete.html'
    success_url = reverse_lazy('home')

# === DeviceType CUD ===
class DeviceTypeCreateView(EmployeeRequiredMixin, CreateView):
    model = DeviceType
    fields = ['name']
    template_name = 'comps/crud_views/device_type_form.html'
    success_url = reverse_lazy('home')


class DeviceTypeUpdateView(EmployeeRequiredMixin, UpdateView):
    model = DeviceType
    fields = ['name']
    template_name = 'comps/crud_views/device_type_form.html'
    success_url = reverse_lazy('home')


class DeviceTypeDeleteView(EmployeeRequiredMixin, DeleteView):
    model = DeviceType
    template_name = 'comps/crud_views/device_type_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['related_devices'] = self.object.devices.all()
        return ctx

# === Device CUD ===
class DeviceCreateView(EmployeeRequiredMixin, CreateView):
    model = Device
    fields = ['type', 'model']
    template_name = 'comps/crud_views/device_form.html'
    success_url = reverse_lazy('home')


class DeviceUpdateView(EmployeeRequiredMixin, UpdateView):
    model = Device
    fields = ['type', 'model']
    template_name = 'comps/crud_views/device_form.html'
    success_url = reverse_lazy('home')


class DeviceDeleteView(EmployeeRequiredMixin, DeleteView):
    model = Device
    template_name = 'comps/crud_views/device_confirm_delete.html'
    success_url = reverse_lazy('home')

# === SparePartType CUD ===
class SparePartTypeCreateView(EmployeeRequiredMixin, CreateView):
    model = SparePartType
    fields = ['name']
    template_name = 'comps/crud_views/spareparttype_form.html'
    success_url = reverse_lazy('types_services_spareparts')


class SparePartTypeUpdateView(EmployeeRequiredMixin, UpdateView):
    model = SparePartType
    fields = ['name']
    template_name = 'comps/crud_views/spareparttype_form.html'
    success_url = reverse_lazy('types_services_spareparts')


class SparePartTypeDeleteView(EmployeeRequiredMixin, DeleteView):
    model = SparePartType
    template_name = 'comps/crud_views/spareparttype_confirm_delete.html'
    success_url = reverse_lazy('types_services_spareparts')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['related_parts'] = self.object.parts.all()
        return ctx

# === SparePart CUD ===
class SparePartCreateView(EmployeeRequiredMixin, CreateView):
    model = SparePart
    fields = ['type', 'name', 'price', 'description']
    template_name = 'comps/crud_views/sparepart_form.html'
    success_url = reverse_lazy('home')


class SparePartUpdateView(EmployeeRequiredMixin, UpdateView):
    model = SparePart
    fields = ['type', 'name', 'price', 'description']
    template_name = 'comps/crud_views/sparepart_form.html'
    success_url = reverse_lazy('home')


class SparePartDeleteView(EmployeeRequiredMixin, DeleteView):
    model = SparePart
    template_name = 'comps/crud_views/sparepart_confirm_delete.html'
    success_url = reverse_lazy('home')


