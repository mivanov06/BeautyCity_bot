from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE)
    phoneNumber = PhoneNumberField(
        unique=True,
        null=False,
        blank=False)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.user.username


class Service(models.Model):
    # Услуга
    name = models.CharField(
        max_length=40,
        verbose_name='Название',
        db_index=True)
    price = models.IntegerField(
        verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class Specialist(models.Model):
    # Специалист
    name = models.CharField(
        max_length=40,
        verbose_name='Имя',
        db_index=True)
    services = models.ManyToManyField(
        Service,
        related_name='services')

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'

    def __str__(self):
        return self.name


class Schedule(models.Model):
    date = models.DateField('Дата посещения')
    time = models.TimeField('Время посещения')
    user = models.ForeignKey(
        Profile,
        verbose_name='Имя клиента',
        on_delete=models.CASCADE,
        related_name='schedules_user',
        blank=False,
    )
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        blank=True,
    )
    services = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        blank=True,
    )

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        return f'{self.time} - {self.specialist.name} - {self.services.name}'
