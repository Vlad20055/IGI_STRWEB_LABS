from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Profile, Client, Employee, Review

# Для регистрации клиента
class ClientSignUpForm(UserCreationForm):
    email = forms.RegexField(
        regex=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
        error_messages={'invalid': 'Введите корректный e-mail адрес.'},
        label="E-mail",
        max_length=254
    )
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    phone = forms.RegexField(
        regex=r'^\+375\s*\(\d{2}\)\s*\d{3}-\d{2}-\d{2}$',
        error_messages={
            'invalid': 'Номер должен быть в формате +375 (XX) XXX-XX-XX'
        },
        label="Телефон"
    )
    address = forms.CharField(widget=forms.Textarea, label="Адрес", required=False)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата рождения"
    )
    passport = forms.CharField(max_length=20, label="Паспорт")
    photo = forms.ImageField(required=False, label="Фото")

    # ДОБАВЛЕНО: Сохраняем существующие поля
    country = forms.CharField(
        initial="Беларусь",
        disabled=True,  # ЗАБЛОКИРОВАННОЕ поле
        label="Страна"
    )
    
    newsletter = forms.BooleanField(
        initial=True,
        required=False,
        label="Подписаться на рассылку акций и новостей"  # ВКЛЮЧЕННЫЙ флажок
    )
    
    # ДОБАВЛЕНО: Новые поля для сбора статистики
    SKILL_LEVEL_CHOICES = [
        ('beginner', '👶 Новичок (только основы)'),
        ('middle', '💻 Продвинутый пользователь'),
        ('advanced', '👨‍💻 Эксперт (программист/админ)'),
    ]
    computer_skill_level = forms.ChoiceField(
        choices=SKILL_LEVEL_CHOICES,
        widget=forms.RadioSelect,  # ПЕРЕКЛЮЧАТЕЛИ
        initial='middle',
        label="Ваш уровень компьютерных навыков"
    )
    
    GENERATION_CHOICES = [
        ('boomer', '👴 Бумер (1946-1964)'),
        ('gen_x', '🧔 Поколение X (1965-1980)'),
        ('millennial', '🧑 Миллениал (1981-1996)'),
        ('gen_z', '👦 Поколение Z (1997-2012)'),
        ('gen_alpha', '👶 Поколение Alpha (2013+)'),
    ]
    generation_group = forms.ChoiceField(
        choices=GENERATION_CHOICES,
        initial='millennial',
        label="К какому поколению вы относитесь"
    )
    
    computer_experience_years = forms.IntegerField(
        min_value=0,
        max_value=80,
        initial=5,
        label="Опыт работы с компьютером (в годах)",
        help_text="Введите число от 0 до 80 лет",
    )
    # ДОБАВЛЕНО КОНЕЦ



    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        # проверяем уникальность
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким e-mail уже зарегистрирован.")
        return email
    
    def clean_birth_date(self):
        bd = self.cleaned_data['birth_date']
        today = datetime.date.today()
        # вычисляем полные годы:
        years = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
        if years < 18 or years > 100:
            raise ValidationError("Регистрация возможна только с 18 до 100 лет.")
        return bd
    
        # ДОБАВЛЕНО: Валидация для опыта работы (значение ВНЕ ДИАПАЗОНА)
    def clean_computer_experience_years(self):
        experience = self.cleaned_data.get('computer_experience_years')
        if experience is not None and (experience < 0 or experience > 80):
            raise ValidationError("Опыт работы должен быть в диапазоне от 0 до 80 лет")
        return experience

    def save(self, commit=True):
        user = super().save(commit=False)
        # Сохраняем имя и фамилию
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            profile = Profile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                birth_date=self.cleaned_data['birth_date'],
                passport=self.cleaned_data['passport'],
                photo=self.cleaned_data.get('photo'),
                # ДОБАВЛЕНО: Сохраняем поля
                country="Беларусь",
                newsletter=self.cleaned_data['newsletter'],
                computer_skill_level=self.cleaned_data['computer_skill_level'],
                generation_group=self.cleaned_data['generation_group'],
                computer_experience_years=self.cleaned_data['computer_experience_years']
            )

            clients_group, _ = Group.objects.get_or_create(name='Clients')
            user.groups.add(clients_group)

            Client.objects.create(profile=profile)
        return user

# Для создания заказов:
import datetime
from django.forms import inlineformset_factory
from .models import Order, OrderService, OrderPart
from django.core.exceptions import ValidationError


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['employee', 'device', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type':'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только мастеров
        self.fields['employee'].queryset = Employee.objects.select_related('profile__user')
        self.fields['employee'].label_from_instance = lambda obj: obj.profile.user.get_full_name()

    def clean_due_date(self):
        due = self.cleaned_data.get('due_date')
        if due is None:
            return due
        today = datetime.date.today()
        if due < today:
            raise ValidationError("Срок выполнения не может быть раньше сегодняшней даты.")
        return due


OrderServiceFormSet = inlineformset_factory(
    Order, OrderService,
    fields=('service','quantity'),
    extra=3,
    can_delete=False
)


OrderPartFormSet = inlineformset_factory(
    Order, OrderPart,
    fields=('part','quantity'),
    extra=3,
    can_delete=False
)

# Для создания отзывов
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min':1, 'max':10}),
            'text': forms.Textarea(attrs={'rows':4}),
        }

