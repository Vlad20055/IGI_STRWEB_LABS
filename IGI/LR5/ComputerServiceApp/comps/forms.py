from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Profile, Client, Employee, Specialization

class MasterSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    passport = forms.CharField(max_length=20)
    photo = forms.ImageField(required=False)
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
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
            masters_group, _ = Group.objects.get_or_create(name='Masters')
            user.groups.add(masters_group)

            employee = Employee.objects.create(profile=profile)
            employee.specializations.set(self.cleaned_data['specializations'])  # ← добавление специализаций
        return user


class ClientSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    passport = forms.CharField(max_length=20)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Создаём профиль
            profile = Profile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                birth_date=self.cleaned_data['birth_date'],
                passport=self.cleaned_data['passport'],  # добавлено
                photo=self.cleaned_data.get('photo')
            )
            # Привязываем к группе Clients
            clients_group, _ = Group.objects.get_or_create(name='Clients')
            user.groups.add(clients_group)
            # Создаём запись в Client
            Client.objects.create(profile=profile)
        return user
