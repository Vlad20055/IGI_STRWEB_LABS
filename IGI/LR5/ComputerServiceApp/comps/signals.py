import logging
logger = logging.getLogger('custom')

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def log_user_created(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Зарегистрирован новый пользователь: {instance.username} (email: {instance.email})")


from .models import (
    ServiceType, Service,
    SparePartType, SparePart,
    DeviceType, Device,
    Order, Review
)

@receiver(post_save, sender=ServiceType)
def log_service_type_change(sender, instance, created, **kwargs):
    if created:
        logger.info(f"[Создание] Тип услуги: {instance.name}")
    else:
        logger.info(f"[Изменение] Тип услуги: {instance.name}")

@receiver(post_save, sender=Service)
def log_service_change(sender, instance, created, **kwargs):
    if created:
        logger.info(f"[Создание] Услуга: {instance.name} (тип {instance.type.name}, цена {instance.price})")
    else:
        logger.info(f"[Изменение] Услуга: {instance.name} (тип {instance.type.name}, цена {instance.price})")

@receiver(post_save, sender=SparePartType)
def log_sparepart_type_change(sender, instance, created, **kwargs):
    if created:
        logger.info(f"[Создание] Тип запчасти: {instance.name}")
    else:
        logger.info(f"[Изменение] Тип запчасти: {instance.name}")

@receiver(post_save, sender=SparePart)
def log_sparepart_change(sender, instance, created, **kwargs):
    if created:
        logger.info(f"[Создание] Запчасть: {instance.name} (тип {instance.type.name}, цена {instance.price})")
    else:
        logger.info(f"[Изменение] Запчасть: {instance.name} (тип {instance.type.name}, цена {instance.price})")

@receiver(post_save, sender=DeviceType)
def log_devicetype_change(sender, instance, created, **kwargs):
    if created:
        logger.info(f"[Создание] Тип устройства: {instance.name}")
    else:
        logger.info(f"[Изменение] Тип устройства: {instance.name}")

@receiver(post_save, sender=Device)
def log_device_change(sender, instance, created, **kwargs):
    if created:
        logger.info(f"[Создание] Устройство: {instance.type.name} {instance.model}")
    else:
        logger.info(f"[Изменение] Устройство: {instance.type.name} {instance.model}")


# Delete (logging)
@receiver(post_delete, sender=ServiceType)
def log_service_type_delete(sender, instance, **kwargs):
    logger.info(f"[Удаление] Тип услуги: {instance.name}")

@receiver(post_delete, sender=Service)
def log_service_delete(sender, instance, **kwargs):
    logger.info(f"[Удаление] Услуга: {instance.name}")

@receiver(post_delete, sender=SparePartType)
def log_sparepart_type_delete(sender, instance, **kwargs):
    logger.info(f"[Удаление] Тип запчасти: {instance.name}")

@receiver(post_delete, sender=SparePart)
def log_sparepart_delete(sender, instance, **kwargs):
    logger.info(f"[Удаление] Запчасть: {instance.name}")

@receiver(post_delete, sender=DeviceType)
def log_devicetype_delete(sender, instance, **kwargs):
    logger.info(f"[Удаление] Тип устройства: {instance.name}")

@receiver(post_delete, sender=Device)
def log_device_delete(sender, instance, **kwargs):
    logger.info(f"[Удаление] Устройство: {instance.type.name} {instance.model}")

@receiver(post_delete, sender=Order)
def log_order_delete(sender, instance, **kwargs):
    logger.info(f"[Удаление] Заказ: {instance.number}")


@receiver(post_save, sender=Order)
def log_order_created(sender, instance, created, **kwargs):
    if created:
        client = instance.client.profile.user.username
        logger.info(f"Создан заказ: {instance.number}, клиент: {client}, срок: {instance.due_date}")


@receiver(post_save, sender=Review)
def log_review_created(sender, instance, created, **kwargs):
    if created:
        user = instance.user.get_full_name() or instance.user.username
        rating = instance.rating
        logger.info(f"Добавлен новый отзыв от «{user}» — оценка: {rating}/10")
