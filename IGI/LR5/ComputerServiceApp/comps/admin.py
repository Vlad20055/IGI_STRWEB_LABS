from django.contrib import admin
from .models import Service, ServiceType, Order, Client, Employee, Specialization, SparePart, SparePartType, Device, DeviceType, Profile

#Register your models here
admin.site.register([ServiceType, Service, Order, Client, Employee,
                     Specialization, SparePartType, SparePart,
                     DeviceType, Device, Profile])


from .models import CompanyInfo
@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    ordering = ('-updated_at',)


from .models import News
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')
    list_filter = ('published_at',)
    search_fields = ('title', 'short_description')


from .models import FAQ
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')
    list_filter = ('created_at',)


from .models import Vacancy
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_at', 'is_active')
    list_filter = ('is_active', 'posted_at')
    search_fields = ('title', 'description')