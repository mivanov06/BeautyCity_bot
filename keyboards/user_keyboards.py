import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BeautyCity_bot.settings")

import django

django.setup()

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import datetime as dt

CALL_US_BUTTON = ('Позвонить нам', 'call_us')

from bot.models import *


def start_keyboard():
    buttons_data = [
        ('Записаться', 'Оставить отзыв'),
        ('О нас',)
    ]

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text) for text in row] for row in buttons_data
        ],
        resize_keyboard=True
    )


def what_can_be_stored_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Читать 🔍',
                    url='https://telegra.ph/Pravila-hraneniya-04-20'
                )
            ]
        ]
    )


def type_service_keyboard():
    services = [
        ('Мейкап', 'service Мейкап'),
        ('Покраска волос', 'service Покраска волос'),
        ('Маникюр', 'service Маникюр'),
        CALL_US_BUTTON
    ]

    serices_m = Service.objects.all()
    services = list()
    for service in serices_m:
        services.append((service.name, f'service {service.id}'))
    services.append(CALL_US_BUTTON)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in services
        ],
    )


def masters_keyboard(service):
    service_m = Service.objects.get(pk=service)
    masters_m = service_m.services.all()
    masters = list()
    for master in masters_m:
        masters.append((master.name, f'master {master.id}'))
    masters.append(CALL_US_BUTTON)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in masters
        ],
    )


def date_work_master_keyboard(master):
    master = Specialist.objects.get(pk=master)
    date_m = master.specialist.filter(date__gte=dt.date.today())
    date_list = list()
    for date_element in date_m:
        date_list.append((str(date_element.date), f'date {date_element.date}'))
    date_list.append(CALL_US_BUTTON)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in date_list
        ],
    )


def time_work_master_keyboard(master_id, service_id, date):
    date_list = Work_time.objects.filter(date=date).filter(specialist_id=master_id).first()  #
    busy_time_query = Schedule.objects.filter(date=date).filter(specialist_id=master_id)
    busy_time_list = list()  # Занятые слоты на день
    for busy_time in busy_time_query:
        busy_time_list.append(busy_time.timeslot)
    time_list = list()
    timeslot_start_id, _ = TIMESLOT_LIST[date_list.timeslot_start]
    timeslot_end_id, _ = TIMESLOT_LIST[date_list.timeslot_end]
    for element_id in range(timeslot_start_id, timeslot_end_id + 1):
        slot_id, time_str = TIMESLOT_LIST[element_id]
        if slot_id not in busy_time_list:
            time_list.append((f'{str(time_str)}', f'time_slot {slot_id}'))
        else:
            time_list.append((f'{str(time_str)} Занято', f't'))
    time_list.append(CALL_US_BUTTON)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in time_list
        ],
    )


def calculate_work_shifts(first_shift):
    now = dt.date.today()
    work_shifts_buttons = []
    work_shifts = [first_shift, first_shift + dt.timedelta(days=1)]
    while now > work_shifts[0] or now > work_shifts[1]:
        first_shift += dt.timedelta(days=4)
        work_shifts = [first_shift, first_shift + dt.timedelta(days=1)]
    while now + dt.timedelta(days=14) > work_shifts[0] or now > work_shifts[1]:
        work_shifts_buttons.append(
            (work_shifts[0].strftime('%d.%m.%Y'), f'date {work_shifts[0].strftime("%d.%m.%Y")}')
        )
        work_shifts_buttons.append(
            (work_shifts[1].strftime('%d.%m.%Y'), f'date {work_shifts[0].strftime("%d.%m.%Y")}')
        )
        first_shift += dt.timedelta(days=4)
        work_shifts = [first_shift, first_shift + dt.timedelta(days=1)]
    return work_shifts_buttons


def master_work_shifts_keyboard(master):
    # Даты выхода на работу впервые для мастеров Ольга и Татьяна
    # Мастера работают по графику 2/2
    date_format = '%d.%m.%Y'
    first_shift_olga = dt.datetime.strptime('10.01.2016', date_format).date()
    first_shift_tatiana = dt.datetime.strptime('13.01.2016', date_format).date()
    if master == 'Ольга':
        first_shift = first_shift_olga
        work_shifts_buttons = calculate_work_shifts(first_shift)
        work_shifts_buttons.append(CALL_US_BUTTON)
    else:
        first_shift = first_shift_tatiana
        work_shifts_buttons = calculate_work_shifts(first_shift)
        work_shifts_buttons.append(CALL_US_BUTTON)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in work_shifts_buttons
        ],
    )


def time_keyboard():
    time = []
    for hour in range(8, 20):
        time.append((str(hour) + ':00', f'time {str(hour) + ":00"}'))
        if hour < 20:
            time.append((str(hour) + ':30', f'time {str(hour) + ":30"}'))
    time.append(CALL_US_BUTTON)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in time
        ],
    )


def pay_keyboard():
    buttons_data = [
        ('Да', 'pay_yes'),
        ('Нет', 'pay_no')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons_data
        ]
    )


def agree_keyboard():
    buttons_data = [
        ('Согласен с правилами', 'agree')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons_data
        ]
    )
