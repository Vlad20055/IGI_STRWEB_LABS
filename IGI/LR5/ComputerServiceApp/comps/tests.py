# файл: comps/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import ServiceType, Service, Review, Coupon, Profile, Client as ClientModel
from datetime import date, timedelta

class ServiceTypeModelTest(TestCase):
    def test_str(self):
        st = ServiceType.objects.create(name="Ремонт", description="Описание")
        self.assertEqual(str(st), "Ремонт")

class ServiceListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        st = ServiceType.objects.create(name="ТестТип")
        # создаём несколько услуг
        for i in range(5):
            Service.objects.create(type=st, name=f"Услуга{i}", description="", price=100+i)

    def test_view_url_exists(self):
        response = self.client.get(reverse('service_list'))
        self.assertEqual(response.status_code, 200)

    def test_pagination_and_context(self):
        response = self.client.get(reverse('service_list'))
        self.assertTrue('services' in response.context)
        self.assertEqual(len(response.context['services']), 5)

class CouponListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # создаём тип и услугу
        st = ServiceType.objects.create(name="T")
        cls.service = Service.objects.create(
            type=st, name="U", description="", price=50
        )
        today = date.today()
        # активный купон
        Coupon.objects.create(
            service=cls.service,
            discount_percent=10,
            valid_until=today + timedelta(days=1)
        )
        # просроченный купон
        Coupon.objects.create(
            service=cls.service,
            discount_percent=5,
            valid_until=today - timedelta(days=1)
        )

    def test_coupons_list(self):
        response = self.client.get(reverse('coupon_list'))
        self.assertEqual(response.status_code, 200)

        # проверяем, что на странице есть заголовок "Активные"
        self.assertContains(response, "Активные")

        # проверяем, что в секции активных купонов есть услуга с именем "U"
        self.assertContains(response, self.service.name)

        # дополнительно явно убеждаемся, что именно "U" встречается в HTML
        self.assertContains(response, ">U<")

        # проверяем, что есть заголовок "Архив"
        self.assertContains(response, "Архив")

class ReviewFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 't@example.com', 'pass')

    def test_review_requires_login(self):
        url = reverse('review_create')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_review_creation(self):
        self.client.login(username='tester', password='pass')
        data = {'rating': 8, 'text': 'Отлично'}
        response = self.client.post(reverse('review_create'), data)
        self.assertRedirects(response, reverse('review_list'))
        self.assertEqual(Review.objects.count(), 1)
        r = Review.objects.first()
        self.assertEqual(r.rating, 8)
        self.assertEqual(r.text, 'Отлично')
