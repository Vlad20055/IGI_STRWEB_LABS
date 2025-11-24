from django.contrib import admin
from .models import Review, Coupon, Service, ServiceType, Order, Client, Employee, Article, Specialization, SparePart, SparePartType, Device, DeviceType, Profile, Partner

#Register your models here
admin.site.register([ServiceType, Order,
                     Specialization, SparePartType,
                     DeviceType, Device, Profile, Article, Review])


from .models import CompanyInfo
@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    ordering = ('-updated_at',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'logo')
        }),
        ('Медиа контент', {
            'fields': ('video_file', 'audio_file')
        }),
        ('Дополнительная информация', {
            'fields': ('history', 'requisites', 'certificate')
        }),
    )


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


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')
    ordering = ('profile__user__last_name', 'profile__user__first_name')

    def full_name(self, obj):
        user = obj.profile.user
        return f"{user.last_name} {user.first_name}"
    full_name.admin_order_field = 'profile__user__last_name'
    full_name.short_description = 'Фамилия Имя'

    def email(self, obj):
        return obj.profile.user.email
    email.admin_order_field = 'profile__user__email'
    email.short_description = 'E-mail'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')
    ordering = ('profile__user__last_name', 'profile__user__first_name')

    def full_name(self, obj):
        user = obj.profile.user
        return f"{user.last_name} {user.first_name}"
    full_name.admin_order_field = 'profile__user__last_name'
    full_name.short_description = 'Фамилия Имя'

    def email(self, obj):
        return obj.profile.user.email
    email.admin_order_field = 'profile__user__email'
    email.short_description = 'E-mail'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price')
    list_filter  = ('type',)
    ordering     = ('price',)
    search_fields= ('name',)


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price')
    list_filter  = ('type',)
    ordering     = ('price',)
    search_fields= ('name',)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('service', 'discount_percent', 'valid_until', 'is_active')
    list_filter  = ('service',)
    readonly_fields = ()


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'website']
    search_fields = ['name']


from .models import Slide, SliderSettings
@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):  # наследуем от admin.ModelAdmin, а не от Slide
    list_display = ['title', 'order', 'active', 'link']
    list_editable = ['order', 'active']
    list_filter = ['active']
    search_fields = ['title']
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'link', 'order', 'active')
        }),
    )


@admin.register(SliderSettings)
class SliderSettingsAdmin(admin.ModelAdmin):
    list_display = ['delay', 'loop', 'navs', 'pags', 'auto', 'stop_mouse_hover']

    # Автоматическое создание настроек при заходе в админку
    def changelist_view(self, request, extra_context=None):
        if not SliderSettings.objects.exists():
            # Создаем настройки по умолчанию
            SliderSettings.objects.create()
            self.message_user(request, "Созданы настройки слайдера по умолчанию", level='SUCCESS')
        return super().changelist_view(request, extra_context)
    
    # Запрещаем добавление новых записей, если уже есть одна
    def has_add_permission(self, request):
        return not SliderSettings.objects.exists()
    
    # Запрещаем удаление
    def has_delete_permission(self, request, obj=None):
        return False
