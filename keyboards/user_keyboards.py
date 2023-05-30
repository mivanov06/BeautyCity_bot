import os

from keyboards.keyboard_utils import get_inline_keyboard

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
    query_services = Service.objects.all()
    masters = list()
    for service in query_services:
        masters.append((service.name, f'service {service.id}'))
    return get_inline_keyboard(masters, buttons_in_row=3)


def masters_keyboard(service):
    service_m = Service.objects.get(pk=service)
    query_masters = service_m.services.all()
    masters = list()
    for master in query_masters:
        masters.append((master.name, f'master {master.id}'))
    return get_inline_keyboard(masters, buttons_in_row=3)


def date_work_master_keyboard(master):
    master = Specialist.objects.get(pk=master)
    query_date = master.specialist.filter(date__gte=dt.date.today())
    print(query_date)
    dates = list()
    for date_element in query_date:
        dates.append((str(date_element.date), f'date {date_element.date}'))
    return get_inline_keyboard(dates, buttons_in_row=4)


def time_work_master_keyboard(master_id, date):
    date_list = Work_time.objects.filter(date=date).filter(specialist_id=master_id).first()
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
    return get_inline_keyboard(time_list, buttons_in_row=2)


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
