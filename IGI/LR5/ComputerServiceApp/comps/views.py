import requests
import re
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import ClientSignUpForm
from .models import Article
from .models import CompanyInfo
from .models import News
from .models import FAQ
from .models import Employee
from .models import Vacancy

def index(request):
    # получаем последнюю по дате опубликования статью
    latest_article = Article.objects.order_by('-published_at').first()
    return render(request, 'comps/index.html', {
        'article': latest_article
    })


def about(request):
    # берём первую запись (или 404, если нет ни одной)
    info = CompanyInfo.objects.order_by('-updated_at').first()
    # если нужно, можно использовать get_object_or_404 для жёсткого 404 при отсутствии
    return render(request, 'comps/about.html', {'info': info})


def news_list(request):
    news_items = News.objects.all()  # уже упорядочены по Meta.ordering
    return render(request, 'comps/news.html', {
        'news_items': news_items
    })


def faq_list(request):
    faqs = FAQ.objects.all()  # уже отсортированы по Meta.ordering
    return render(request, 'comps/faq.html', {'faqs': faqs})


def contacts(request):
    # Подтягиваем всех сотрудников, вместе со связанными профилями и специализациями
    employees = Employee.objects.select_related('profile__user').prefetch_related('specializations')
    return render(request, 'comps/contacts.html', {'employees': employees})


def privacy_policy(request):
    return render(request, 'comps/privacy.html')


def vacancy_list(request):
    vacancies = Vacancy.objects.filter(is_active=True)
    return render(request, 'comps/vacancies.html', {
        'vacancies': vacancies
    })


def signup_client(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = ClientSignUpForm()
    return render(request, 'comps/signup_client.html', {'form': form})


# Для создания заказов
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import OrderForm, OrderServiceFormSet, OrderPartFormSet
from .models import Client

def is_client(user):
    return user.is_authenticated and user.groups.filter(name='Clients').exists()

@login_required
@user_passes_test(is_client)
def order_create(request):
    # Попытка достать клиента через профиль
    try:
        client = request.user.profile.client
    except (AttributeError, Client.DoesNotExist):
        # если что-то не так с профилем/Client, выдаём 403
        return HttpResponseForbidden("У вас нет прав создавать заказы.")
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        svc_fs = OrderServiceFormSet(request.POST)
        part_fs = OrderPartFormSet(request.POST)
        if form.is_valid() and svc_fs.is_valid() and part_fs.is_valid():
            order = form.save(commit=False)
            order.client = client
            order.save()
            svc_fs.instance = order
            svc_fs.save()
            part_fs.instance = order
            part_fs.save()
            return redirect('order_list_client')
    else:
        form = OrderForm()
        svc_fs = OrderServiceFormSet()
        part_fs = OrderPartFormSet()

    return render(request, 'comps/order_form.html', {
        'form': form,
        'svc_fs': svc_fs,
        'part_fs': part_fs
    })


from .models import Order
@login_required
@user_passes_test(is_client)
def order_list_client(request):
    client = request.user.profile.client
    orders = Order.objects.filter(client=client).order_by('-created_at')
    return render(request, 'comps/order_list_client.html', {'orders': orders})


@login_required
def order_detail_by_number(request, number):
    # Ищем заказ по его 'number', а не по 'pk'
    order = get_object_or_404(Order, number=number)

    # Проверка, что заказ принадлежит либо клиенту, либо мастеру
    user = request.user
    if order.client.profile.user != user and order.employee.profile.user != user:
        return HttpResponseForbidden("Это не ваш заказ.")

    return render(request, 'comps/order_detail.html', {'order': order})


# Для Employee
def is_employee(user):
    return user.is_authenticated and user.groups.filter(name='Employees').exists()

@login_required
@user_passes_test(is_employee)
def order_list_employee(request):
    # получаем объект Employee по связанному Profile
    emp = get_object_or_404(Employee, profile=request.user.profile)
    # выбираем все заказы, где этот Employee
    orders = Order.objects.filter(employee=emp).order_by('-created_at')
    return render(request, 'comps/order_list_employee.html', {
        'orders': orders
    })


def special(request):
    action = request.GET.get('action')

    if 'joke' not in request.session or action == 'joke':
        try:
            jr = requests.get('https://official-joke-api.appspot.com/random_joke', timeout=5)
            jr.raise_for_status()
            request.session['joke'] = jr.json()
        except:
            request.session['joke'] = {'setup': 'Ошибка при получении шутки.', 'punchline': ''}

    if 'quote' not in request.session or action == 'quote':
        try:
            qr = requests.get('https://favqs.com/api/qotd', timeout=5)
            qr.raise_for_status()
            quote_data = qr.json().get('quote', {})
            request.session['quote'] = {
                'body': quote_data.get('body', ''),
                'author': quote_data.get('author', '')
            }
        except:
            request.session['quote'] = {'body': 'Ошибка при получении цитаты.', 'author': ''}

    return render(request, 'comps/special.html', {
        'joke': request.session['joke'],
        'quote': request.session['quote'],
    })