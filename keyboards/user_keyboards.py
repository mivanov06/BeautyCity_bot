from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import datetime as dt


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


def storage_conditions_keyboard():
    buttons_data = [
        ('Читать 🔍', 'https://telegra.ph/Usloviya-hraneniya-04-20')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, url=url)] for text, url in buttons_data
        ]
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


def send_to_storage_keyboard():
    buttons_data = [
        ('Привезете вещи сами?', 'yourself'),
        ('Курьером (бесплатно)', 'courier')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons_data
        ]
    )


def type_service_keyboard():
    services = [('Мейкап', 'service makeup'), ('Покраска волос', 'service coloring'), ('Маникюр', 'service manicure')]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in services
        ],
    )


def masters_keyboard():
    masters = [('Ольга', 'master Ольга'), ('Татьяна', 'master Татьяна')]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in masters
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
    else:
        first_shift = first_shift_tatiana
        work_shifts_buttons = calculate_work_shifts(first_shift)
    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in work_shifts_buttons
        ],
    )


def output_my_cells_keyboard():
    buttons_data = [
        ('Продлить хранение', 'extend_storage'),
        ('Забрать часть вещей', 'pick_up_some_things'),
        ('Забрать вещи', 'pick_up_all_things')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons_data
        ]
    )


def generate_my_cells_keyboard(user_cells):
    inline_keyboard = []
    for cell in user_cells:
        cell_button = [
                InlineKeyboardButton(
                    text=f'{cell}',
                    callback_data=f'cell_{cell}'
                )
        ]
        inline_keyboard.append(cell_button)
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def extend_rental_period_keyboard():
    periods = [
        ('1 месяц', 'extend_one_month'),
        ('3 месяца', 'extend_tree_month'),
        ('6 месяцев', 'extend_six_month'),
        ('12 месяцев', 'extend_twelve_month')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in periods
        ]
    )


def generate_pick_up_things_keyboard():
    buttons_data = [
        ('Заберу сам(а)', 'pick_up_myself'),
        ('Доставить на дом', 'deliver_home')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons_data
        ]
    )


def generate_pick_up_cells_keyboard(user_cells):
    buttons = []
    for cell in user_cells:
        buttons.append((f'{cell}', f'pick_up_cell_{cell}'))

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons
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
