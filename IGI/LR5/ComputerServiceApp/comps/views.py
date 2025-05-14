from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import MasterSignUpForm, ClientSignUpForm
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


def signup_master(request):
    if request.method == 'POST':
        form = MasterSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = MasterSignUpForm()
    return render(request, 'comps/signup_master.html', {'form': form})


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