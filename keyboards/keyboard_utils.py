from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CALL_US_BUTTON = ('Позвонить нам', 'call_us')

START_KEYBOARD = [
    ('Записаться', 'Записаться'),
    ('Мои записи', 'Мои записи'),
    ('Оставить отзыв', 'Оставить отзыв'),
    ('О нас', 'О нас')
]


def get_inline_keyboard(query, buttons_in_row=2, CALL_US=True) -> InlineKeyboardMarkup:
    buttons_row = []
    inline_keyboard = []
    for element in query:
        text, data = element
        buttons_row.append(InlineKeyboardButton(text=text, callback_data=data))
        if len(buttons_row) == buttons_in_row:
            inline_keyboard.append(buttons_row)
            buttons_row = []
    if buttons_row:
        inline_keyboard.append(buttons_row)
    if CALL_US:
        text, data = CALL_US_BUTTON
        inline_keyboard.append([InlineKeyboardButton(text=text, callback_data=data)])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)