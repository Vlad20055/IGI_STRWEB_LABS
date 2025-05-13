from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.
# Дополнительная информация о клиенте/сотруднике
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+375\s*\(\d{2}\)\s*\d{3}-\d{2}-\d{2}$',
                message='Формат номера: +375 (XX) XXX-XX-XX'
            )
        ]
    )
    address = models.TextField()
    passport = models.CharField(max_length=20)
    birth_date = models.DateField()
    
    @property
    def age(self):
        return (timezone.now().date() - self.birth_date).days // 365

    def __str__(self):
        return f"{self.user.get_full_name()}"

# Специализация сотрудника
class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

# Сотрудник (мастер)
class Employee(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    specializations = models.ManyToManyField(Specialization, related_name='employees')
    
    def __str__(self):
        return self.profile.user.get_full_name()

# Тип услуги
class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

# Услуга
class Service(models.Model):
    type = models.ForeignKey(ServiceType, on_delete=models.PROTECT, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

# Тип ремонтируемого устройства
class DeviceType(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

# Ремонтируемое устройство
class Device(models.Model):
    type = models.ForeignKey(DeviceType, on_delete=models.PROTECT, related_name='devices')
    model = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.type.name} {self.model}"

# Тип запасной части
class SparePartType(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

# Запасная часть
class SparePart(models.Model):
    type = models.ForeignKey(SparePartType, on_delete=models.PROTECT, related_name='parts')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name

# Клиент
class Client(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.profile.user.get_full_name()

# Договор/Заказ
class Order(models.Model):
    number = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='orders')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='orders')
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    services = models.ManyToManyField(Service, through='OrderService')
    spare_parts = models.ManyToManyField(SparePart, through='OrderPart')
    
    @property
    def total_cost(self):
        svc = sum(item.subtotal for item in self.orderservice_set.all())
        parts = sum(item.subtotal for item in self.orderpart_set.all())
        return svc + parts
    
    def __str__(self):
        return f"Заказ {self.number} — {self.client}"

# Промежуточная модель для услуг в заказе
class OrderService(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    @property
    def subtotal(self):
        return self.service.price * self.quantity

# Промежуточная модель для запчастей в заказе
class OrderPart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    part = models.ForeignKey(SparePart, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    @property
    def subtotal(self):
        return self.part.price * self.quantity

# Промокоды/Купоны
class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    expires_at = models.DateField()
    
    def __str__(self):
        return self.code