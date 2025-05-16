# comps/crud_views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import (
    ServiceType, Service,
    DeviceType, Device,
    SparePartType, SparePart
)

class EmployeeRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Employees').exists()

# === ServiceType CRUD ===
class ServiceTypeListView(ListView):
    model = ServiceType
    template_name = 'comps/crud_views/service_type_list.html'
    context_object_name = 'types'

class ServiceTypeCreateView(EmployeeRequiredMixin, CreateView):
    model = ServiceType
    fields = ['name', 'description']
    template_name = 'comps/crud_views/service_type_form.html'
    success_url = reverse_lazy('service_type_list')

class ServiceTypeUpdateView(EmployeeRequiredMixin, UpdateView):
    model = ServiceType
    fields = ['name', 'description']
    template_name = 'comps/crud_views/service_type_form.html'
    success_url = reverse_lazy('service_type_list')

class ServiceTypeDeleteView(EmployeeRequiredMixin, DeleteView):
    model = ServiceType
    template_name = 'comps/crud_views/service_type_confirm_delete.html'
    success_url = reverse_lazy('service_type_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # все сервисы, которые будут удалены вместе с этим типом
        ctx['related_services'] = self.object.services.all()
        return ctx

# === Service CRUD ===
class ServiceListView(ListView):
    model = Service
    template_name = 'comps/crud_views/service_list.html'
    context_object_name = 'services'

class ServiceCreateView(EmployeeRequiredMixin, CreateView):
    model = Service
    fields = ['type', 'name', 'description', 'price']
    template_name = 'comps/crud_views/service_form.html'
    success_url = reverse_lazy('service_list')

class ServiceUpdateView(EmployeeRequiredMixin, UpdateView):
    model = Service
    fields = ['type', 'name', 'description', 'price']
    template_name = 'comps/crud_views/service_form.html'
    success_url = reverse_lazy('service_list')

class ServiceDeleteView(EmployeeRequiredMixin, DeleteView):
    model = Service
    template_name = 'comps/crud_views/service_confirm_delete.html'
    success_url = reverse_lazy('service_list')

# === DeviceType CRUD ===
class DeviceTypeListView(ListView):
    model = DeviceType
    template_name = 'comps/crud_views/device_type_list.html'
    context_object_name = 'devicetypes'

class DeviceTypeCreateView(EmployeeRequiredMixin, CreateView):
    model = DeviceType
    fields = ['name']
    template_name = 'comps/crud_views/device_type_form.html'
    success_url = reverse_lazy('device_type_list')

class DeviceTypeUpdateView(EmployeeRequiredMixin, UpdateView):
    model = DeviceType
    fields = ['name']
    template_name = 'comps/crud_views/device_type_form.html'
    success_url = reverse_lazy('device_type_list')

class DeviceTypeDeleteView(EmployeeRequiredMixin, DeleteView):
    model = DeviceType
    template_name = 'comps/crud_views/device_type_confirm_delete.html'
    success_url = reverse_lazy('device_type_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['related_devices'] = self.object.devices.all()
        return ctx

# === Device CRUD ===
class DeviceListView(ListView):
    model = Device
    template_name = 'comps/crud_views/device_list.html'
    context_object_name = 'devices'

class DeviceCreateView(EmployeeRequiredMixin, CreateView):
    model = Device
    fields = ['type', 'model', 'serial_number']
    template_name = 'comps/crud_views/device_form.html'
    success_url = reverse_lazy('device_list')

class DeviceUpdateView(EmployeeRequiredMixin, UpdateView):
    model = Device
    fields = ['type', 'model', 'serial_number']
    template_name = 'comps/crud_views/device_form.html'
    success_url = reverse_lazy('device_list')

class DeviceDeleteView(EmployeeRequiredMixin, DeleteView):
    model = Device
    template_name = 'comps/crud_views/device_confirm_delete.html'
    success_url = reverse_lazy('device_list')

# === SparePartType CRUD ===
class SparePartTypeListView(ListView):
    model = SparePartType
    template_name = 'comps/crud_views/spareparttype_list.html'
    context_object_name = 'parttypes'

class SparePartTypeCreateView(EmployeeRequiredMixin, CreateView):
    model = SparePartType
    fields = ['name']
    template_name = 'comps/crud_views/spareparttype_form.html'
    success_url = reverse_lazy('spareparttype_list')

class SparePartTypeUpdateView(EmployeeRequiredMixin, UpdateView):
    model = SparePartType
    fields = ['name']
    template_name = 'comps/crud_views/spareparttype_form.html'
    success_url = reverse_lazy('spareparttype_list')

class SparePartTypeDeleteView(EmployeeRequiredMixin, DeleteView):
    model = SparePartType
    template_name = 'comps/crud_views/spareparttype_confirm_delete.html'
    success_url = reverse_lazy('spareparttype_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['related_parts'] = self.object.parts.all()
        return ctx

# === SparePart CRUD ===
class SparePartListView(ListView):
    model = SparePart
    template_name = 'comps/crud_views/sparepart_list.html'
    context_object_name = 'parts'

class SparePartCreateView(EmployeeRequiredMixin, CreateView):
    model = SparePart
    fields = ['type', 'name', 'price', 'stock']
    template_name = 'comps/crud_views/sparepart_form.html'
    success_url = reverse_lazy('sparepart_list')

class SparePartUpdateView(EmployeeRequiredMixin, UpdateView):
    model = SparePart
    fields = ['type', 'name', 'price', 'stock']
    template_name = 'comps/crud_views/sparepart_form.html'
    success_url = reverse_lazy('sparepart_list')

class SparePartDeleteView(EmployeeRequiredMixin, DeleteView):
    model = SparePart
    template_name = 'comps/crud_views/sparepart_confirm_delete.html'
    success_url = reverse_lazy('sparepart_list')
