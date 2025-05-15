from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Profile, Client, Employee


# class ClientSignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(max_length=30, required=True, label="Имя")
#     last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
#     phone = forms.CharField(max_length=20)
#     address = forms.CharField(widget=forms.Textarea)
#     birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     passport = forms.CharField(max_length=20)
#     photo = forms.ImageField(required=False)

#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#             # Создаём профиль
#             profile = Profile.objects.create(
#                 user=user,
#                 phone=self.cleaned_data['phone'],
#                 address=self.cleaned_data['address'],
#                 birth_date=self.cleaned_data['birth_date'],
#                 passport=self.cleaned_data['passport'],  # добавлено
#                 photo=self.cleaned_data.get('photo')
#             )
#             # Привязываем к группе Clients
#             clients_group, _ = Group.objects.get_or_create(name='Clients')
#             user.groups.add(clients_group)
#             # Создаём запись в Client
#             Client.objects.create(profile=profile)
#         return user


class ClientSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    phone = forms.CharField(max_length=20, label="Телефон")
    address = forms.CharField(widget=forms.Textarea, label="Адрес")
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Дата рождения")
    passport = forms.CharField(max_length=20, label="Паспорт")
    photo = forms.ImageField(required=False, label="Фото")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

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
                photo=self.cleaned_data.get('photo')
            )

            clients_group, _ = Group.objects.get_or_create(name='Clients')
            user.groups.add(clients_group)

            Client.objects.create(profile=profile)
        return user


# Для создания заказов:
from django.forms import inlineformset_factory
from .models import Order, OrderService, OrderPart

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['number', 'employee', 'device', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type':'date'})
        }
        exclude = ['number', 'client']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только мастеров
        self.fields['employee'].queryset = Employee.objects.select_related('profile__user')
        self.fields['employee'].label_from_instance = lambda obj: obj.profile.user.get_full_name()


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

