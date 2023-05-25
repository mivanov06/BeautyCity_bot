from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    name = models.CharField(max_length=200)
    telegram_id = models.IntegerField(verbose_name='ID пользователя в Telegram', null=True)
    phone = PhoneNumberField(max_length=20, verbose_name='Номер телефона', blank=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name} - {self.phone}'


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


TIMESLOT_LIST = (
    (0, '09:00 – 09:30'),
    (1, '09:30 – 10:00'),
    (2, '10:00 – 10:30'),
    (3, '10:30 – 11:00'),
    (4, '11:00 – 11:30'),
    (5, '11:30 – 12:00'),
    (6, '12:00 – 12:30'),
    (7, '12:30 – 13:00'),
    (8, '13:00 – 13:30'),
    (9, '13:30 – 14:00'),
    (10, '14:00 – 14:30'),
    (11, '14:30 – 15:00'),
    (12, '15:00 – 15:30'),
    (13, '16:00 – 16:30'),
    (14, '17:00 – 17:30'),
    (15, '17:30 – 18:00'),
    (16, '18:00 – 18:30'),
    (17, '18:30 – 19:00'),
    (18, '19:00 – 19:30'),
    (19, '19:30 – 20:00'),
)


class Schedule(models.Model):
    date = models.DateField(help_text="DD-MM-YYYY", verbose_name='Дата посещения')
    timeslot = models.IntegerField(choices=TIMESLOT_LIST, null=True, verbose_name='Время посещения')
    user = models.ForeignKey(
        User,
        verbose_name='Имя клиента',
        on_delete=models.CASCADE,
        related_name='schedules_user',
        blank=True, null=True
    )
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        related_name='schedules_specialist',
        blank=True, null=True
    )
    services = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='schedules_services',
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        return f'{self.timeslot} - {self.specialist.name} - {self.services.name}'
