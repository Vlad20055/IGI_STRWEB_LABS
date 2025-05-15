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
            return redirect('order_list')
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
@user_passes_test(lambda u: u.groups.filter(name='Clients').exists())
def order_list(request):
    client = request.user.profile.client
    orders = Order.objects.filter(client=client).order_by('-created_at')
    return render(request, 'comps/order_list.html', {'orders': orders})


@login_required
@user_passes_test(is_client)
def order_detail(request, pk):
    # берём заказ или 404
    order = get_object_or_404(Order, pk=pk)
    # проверяем, что текущий пользователь — владелец заказа
    if order.client.profile.user != request.user:
        return HttpResponseForbidden("Это не ваш заказ.")
    # передаём в шаблон
    return render(request, 'comps/order_detail.html', {'order': order})