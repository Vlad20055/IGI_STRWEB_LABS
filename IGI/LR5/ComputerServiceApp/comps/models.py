from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

# Create your models here.
# Дополнительная информация о клиенте/сотруднике
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        verbose_name='Фото'
    )
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
        return self.profile.user.username

# Договор/Заказ
class Order(models.Model):
    number = models.CharField(max_length=50, unique=True, editable=False)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='orders')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='orders')
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    services = models.ManyToManyField(Service, through='OrderService')
    spare_parts = models.ManyToManyField(SparePart, through='OrderPart')

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

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
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    
    @property
    def subtotal(self):
        return self.service.price * self.quantity

# Промежуточная модель для запчастей в заказе
class OrderPart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    part = models.ForeignKey(SparePart, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    
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
    
# Статья
class Article(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Для страницы "О компании"
class CompanyInfo(models.Model):
    """
    Хранит текстовую информацию «О компании».
    Можно создавать несколько записей (например, для разных разделов или историй по годам),
    но сейчас будем брать первую.
    """
    title = models.CharField(max_length=200, default="О компании")
    content = models.TextField(help_text="Основной текст «О компании»")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"

    def __str__(self):
        return self.title

# Для страницы "Новости"
class News(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    short_description = models.CharField(
        "Краткое содержание", 
        max_length=255,
        help_text="Одно предложение"
    )
    content = models.TextField("Полный текст новости")
    image = models.ImageField(
        "Изображение",
        upload_to='news/',
        blank=True,
        null=True
    )
    published_at = models.DateTimeField(
        "Дата и время публикации",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-published_at']

    def __str__(self):
        return self.title

# Для страницы "FAQ"
class FAQ(models.Model):
    question = models.CharField("Вопрос", max_length=255)
    answer = models.TextField("Ответ")
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Термин / Вопрос"
        verbose_name_plural = "Словарь терминов и понятий"
        ordering = ['-created_at']

    def __str__(self):
        # чтобы в админке было понятно
        return self.question

# Для страницы "Вакансии"
class Vacancy(models.Model):
    title = models.CharField("Должность", max_length=200)
    description = models.TextField("Описание вакансии")
    posted_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-posted_at']

    def __str__(self):
        return self.title