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

    # ДОБАВЛЕНО НАЧАЛО
    country = models.CharField(
        max_length=100, 
        default="Беларусь",
        verbose_name='Страна'
    )
    newsletter = models.BooleanField(
        default=True,
        verbose_name='Подписка на рассылку'
    )
    computer_experience_years = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(80)],
        verbose_name='Опыт работы с компьютером (в годах)',
        help_text='От 0 до 80 лет',
        default=1
    )
    generation_group = models.CharField(
        max_length=20,
        choices=[
            ('boomer', 'Бумер (1946-1964)'),
            ('gen_x', 'Поколение X (1965-1980)'),
            ('millennial', 'Миллениал (1981-1996)'),
            ('gen_z', 'Поколение Z (1997-2012)'),
            ('gen_alpha', 'Поколение Alpha (2013+)'),
        ],
        default='millennial',  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
        verbose_name='К какому поколению относитесь'
    )
    computer_skill_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Новичок (только основы)'),
            ('middle', 'Продвинутый пользователь'),
            ('advanced', 'Эксперт (программист/админ)'),
        ],
        default='middle',
        verbose_name='Уровень компьютерных навыков'
    )


    
    
    # ДОБАВЛЕНО КОНЕЦ


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def age(self):
        return (timezone.now().date() - self.birth_date).days // 365

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"{self.user.get_full_name()}"

# Специализация сотрудника
class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.name

# Сотрудник (мастер)
class Employee(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    specializations = models.ManyToManyField(Specialization, related_name='employees')
    
    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return self.profile.user.get_full_name()

# Тип услуги
class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'

    def __str__(self):
        return self.name

# Услуга
class Service(models.Model):
    type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name

# Тип ремонтируемого устройства
class DeviceType(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Тип устройства'
        verbose_name_plural = 'Типы устройств'

    def __str__(self):
        return self.name

# Ремонтируемое устройство
class Device(models.Model):
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name='devices')
    model = models.CharField(max_length=200)
    # serial_number = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'

    def __str__(self):
        return f"{self.type.name} {self.model}"

# Тип запчасти
class SparePartType(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Тип запчасти'
        verbose_name_plural = 'Типы запчастей'

    def __str__(self):
        return self.name

# Запчасть
class SparePart(models.Model):
    type = models.ForeignKey(SparePartType, on_delete=models.CASCADE, related_name='parts')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'

    def __str__(self):
        return self.name

# Клиент
class Client(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

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

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

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
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    
    @property
    def subtotal(self):
        return self.service.price * self.quantity

# Промежуточная модель для запчастей в заказе
class OrderPart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    part = models.ForeignKey(SparePart, on_delete=models.CASCADE)
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

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title

# Для страницы "О компании"
# models.py
class CompanyInfo(models.Model):
    """
    Хранит полную информацию о компании
    """
    title = models.CharField(max_length=200, default="О компании", verbose_name="Заголовок")
    content = models.TextField(help_text="Основной текст о компании", verbose_name="Основной текст")
    logo = models.ImageField(upload_to='company/logo/', blank=True, null=True, verbose_name="Логотип компании")
    video_file = models.FileField(upload_to='company/videos/', blank=True, null=True, verbose_name="Видео файл")
    audio_file = models.FileField(upload_to='company/audio/', blank=True, null=True, verbose_name="Аудио файл")
    history = models.TextField(blank=True, null=True, verbose_name="История по годам")
    requisites = models.TextField(blank=True, null=True, verbose_name="Реквизиты")
    certificate = models.TextField(blank=True, null=True, verbose_name="Сертификаты")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

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

# Отзывы
class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв от {self.user.get_full_name()} — {self.rating}"

# Промокоды и купоны
class Coupon(models.Model):
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='coupons'
    )
    discount_percent = models.PositiveSmallIntegerField(
        help_text='Скидка в процентах (1–100)'
    )
    valid_until = models.DateField(
        help_text='Дата окончания действия купона'
    )

    class Meta:
        ordering = ['-valid_until']
        verbose_name = 'Промокод/купон'
        verbose_name_plural = 'Промокоды и купоны'

    @property
    def is_active(self):
        return self.valid_until >= timezone.now().date()

    def __str__(self):
        return f"{self.service.name}: -{self.discount_percent}% до {self.valid_until.strftime('%d/%m/%Y')}"
    
# Компании партнёры
class Partner(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название компании')
    logo = models.ImageField(upload_to='partners/logos/', verbose_name='Логотип')
    website = models.URLField(verbose_name='Сайт компании')
    
    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['name']

    def __str__(self):
        return self.name