import calendar
import io
import base64
import statistics
import datetime
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.db.models import F, Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import ClientSignUpForm
from .models import Article, OrderService
from .models import CompanyInfo
from .models import News
from .models import FAQ
from .models import Employee
from .models import Vacancy

import logging
logger = logging.getLogger('custom')

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
            logger.info(f"Создан заказ: {order.number}, клиент: {request.user.username}, дата: {order.created_at}")
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

import statistics
def statistic(request):
    # --- (ваш существующий код по возрастам) ---
    today = datetime.date.today()
    ages = []
    for client in Client.objects.select_related('profile').all():
        bd = client.profile.birth_date
        age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
        ages.append(age)
    if ages:
        avg_age = round(statistics.mean(ages), 1)
        med_age = statistics.median(ages)
        try:
            mode_age = statistics.mode(ages)
        except statistics.StatisticsError:
            mode_age = min(statistics.multimode(ages))
    else:
        avg_age = med_age = mode_age = 0

    # Гистограмма возрастов
    fig1, ax1 = plt.subplots()
    bins = range(min(ages, default=18), max(ages, default=18) + 2)
    ax1.hist(ages, bins=bins, edgecolor='black')
    ax1.set_xlabel('Возраст (лет)')
    ax1.set_ylabel('Число клиентов')
    ax1.set_title('Распределение возрастов клиентов')
    buf1 = io.BytesIO()
    fig1.tight_layout()
    fig1.savefig(buf1, format='png')
    plt.close(fig1)
    buf1.seek(0)
    age_chart = base64.b64encode(buf1.getvalue()).decode('ascii')
    buf1.close()

    # --- Новый блок: статистика по типам услуг ---
    # Считаем общее количество всех сервисов в заказах
    total_items = 0
    # словарь {ServiceType: total_quantity}
    counts = {}
    for os in OrderService.objects.select_related('service__type').all():
        st = os.service.type
        counts.setdefault(st, 0)
        counts[st] += os.quantity
        total_items += os.quantity

    # Подготавливаем данные для диаграммы
    labels = []
    values = []
    for st, cnt in counts.items():
        labels.append(st.name)
        # процент
        pct = (cnt / total_items * 100) if total_items else 0
        values.append(pct)

    # Рисуем горизонтальную столбчатую диаграмму
    fig2, ax2 = plt.subplots(figsize=(6, max(4, len(labels)*0.5)))
    y_pos = range(len(labels))
    ax2.barh(y_pos, values, align='center', edgecolor='black')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(labels)
    ax2.invert_yaxis()
    ax2.set_xlabel('Процент заказов (%)')
    ax2.set_title('Распределение заказов по типам услуг')
    buf2 = io.BytesIO()
    fig2.tight_layout()
    fig2.savefig(buf2, format='png')
    plt.close(fig2)
    buf2.seek(0)
    services_chart = base64.b64encode(buf2.getvalue()).decode('ascii')
    buf2.close()

    return render(request, 'comps/statistic.html', {
        'avg_age': avg_age,
        'med_age': med_age,
        'mode_age': mode_age,
        'age_chart': f'data:image/png;base64,{age_chart}',
        'services_chart': f'data:image/png;base64,{services_chart}',
    })


@login_required
@user_passes_test(is_employee)
def company_statistic(request):
    # 1) Считаем выручку по каждому типу услуг
    qs = (
        OrderService.objects
        .values(type_name=F('service__type__name'))
        .annotate(revenue=Sum(F('quantity') * F('service__price')))
        .order_by('-revenue')
    )

    # 2) Метки и данные
    labels = [item['type_name'] for item in qs]
    revenues = [item['revenue'] or 0 for item in qs]

    # 3) Самый прибыльный тип услуги
    top_type = labels[0] if labels else None

    # 4) Строим диаграмму
    fig, ax = plt.subplots(figsize=(6, max(4, len(labels) * 0.5)))
    y_pos = list(range(len(labels)))
    ax.barh(y_pos, revenues, align='center', edgecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel('Выручка (руб.)')
    ax.set_title('Выручка по типам услуг')

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    chart = base64.b64encode(buf.getvalue()).decode('ascii')
    buf.close()

    return render(request, 'comps/company_statistic.html', {
        'top_type': top_type,
        'chart': f'data:image/png;base64,{chart}',
    })


def calendar_view(request):
    # Получаем текущий год и месяц
    today = datetime.date.today()
    year, month = today.year, today.month

    # Генерируем текстовый календарь для месяца
    cal = calendar.TextCalendar(firstweekday=0)  # понедельник первым
    month_calendar = cal.formatmonth(year, month)

    # Передаём текущую дату в формате DD/MM/YYYY (серверное время)
    current_date = today.strftime('%d/%m/%Y')

    return render(request, 'comps/calendar.html', {
        'month_calendar': month_calendar,
        'current_date': current_date,
    })