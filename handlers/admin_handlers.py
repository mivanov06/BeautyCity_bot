from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon_ru import LEXICON_RU
from keyboards import admin_keyboards
from database import database_funcs
from config_data.config import load_config
from utils import utils

from sqlite3_api.Table import Table

router = Router()


class GetCellNumber(StatesGroup):
    cell_number = State()
    order_id = State()
    link = State()
    link_name = State()


@router.message(Command(commands=['admin']))
async def process_admin_command(message: Message):
    # database_funcs.filling_users_table_test_data()  # Заполнение таблицы Users тестовыми данными
    # database_funcs.filling_links_table_test_data()  # Заполнение таблицы links_table тестовыми данными
    # database_funcs.print_table()
    ids = load_config().admin_ids.ids_list
    if str(message.from_user.id) in ids:
        await message.answer(
            text=LEXICON_RU['/admin'],
            reply_markup=admin_keyboards.start_admin_keyboard()
        )
    else:
        await message.answer(text='У вас не достаточно прав')


@router.message(Text(contains=['Новые заказы']))
async def show_new_orders(message: Message):
    new_orders = database_funcs.get_new_orders()
    await message.answer(
        text=f'{len(new_orders)} новых заказов.\nНажмите на кнопку, чтобы посмотреть детали:',
        reply_markup=admin_keyboards.new_orders_keyboard(new_orders)
    )


@router.callback_query(Text(startswith=['new_order_button_']))
async def show_new_order_details(callback: CallbackQuery):
    order_id = int(callback.data.split(sep="_")[-1])
    order_details = database_funcs.get_new_order_details(order_id)
    await callback.message.edit_text(
        text=f'Заказ № {order_id}\nТелефон: {order_details["phone"]}\nАдрес: {order_details["address"]}',
        reply_markup=admin_keyboards.assign_cell_number(order_id)
    )


@router.callback_query(Text(startswith=['assign_cell_number_']))
async def assign_cell_number(callback: CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split(sep="_")[-1])
    await state.update_data(order_id=order_id)
    await state.set_state(GetCellNumber.cell_number)
    await callback.message.edit_text(
        text='Введите номер ячейки:'
    )
    await callback.answer()


@router.message(GetCellNumber.cell_number)
async def process_assign_cell_number(message: Message, state: FSMContext):
    await state.update_data(cell_number=message.text)
    data = await state.get_data()
    order_id = int(data['order_id'])
    database_funcs.assign_cell_number(order_id, message.text)
    await message.answer(
        text=f'Заказу №{order_id} присвоена ячейка {message.text}'
    )
    await state.clear()


@router.message(Text(contains=['Статистика заказов']))
async def show_links(message: Message):
    current_links = database_funcs.get_current_links()
    if current_links:
        await message.answer(
            text='Выберите интересующую вас ссылку, чтобы посмотреть статистику',
            reply_markup=admin_keyboards.show_current_links(current_links)
        )
    else:
        await message.answer(
            text='Нет ссылок для сбора статистики.',
            reply_markup=admin_keyboards.add_link_keyboard()
        )


@router.callback_query(Text(startswith=['current_link_']))
async def show_link_details(callback: CallbackQuery):
    link_name = callback.data.split(sep="_")[-1]
    link = database_funcs.get_link(link_name)
    count_clicks = utils.get_link_clicks(link)
    await callback.message.edit_text(text=f'Количество кликов по ссылке {count_clicks} раз.')


@router.callback_query(Text(text=['add_link']))
async def add_link(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GetCellNumber.link)
    await callback.message.edit_text(text='Вставьте bitly ссылку:')


@router.message(GetCellNumber.link)
async def add_link_name(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await state.set_state(GetCellNumber.link_name)
    await message.answer(text='Введите название для ссылки:')


@router.message(GetCellNumber.link_name)
async def write_link_details(message: Message, state: FSMContext):
    await state.update_data(link_name=message.text)
    data = await state.get_data()
    link = data.get('link')
    name = data.get('link_name')
    database_funcs.add_new_link(link, name)
    database_funcs.print_table()
    await message.answer(text='Ссылка добавлена')
    await state.clear()


@router.message(Text(contains=['Просроченные заказы']))
async def show_overdue_orders(message: Message):
    overdue_orders = database_funcs.get_overdue_orders()
    if len(overdue_orders):
        await message.answer(
            text=f'Сегодня {len(overdue_orders)} просроченных заказов.\nНажмите на заказ, чтобы посмотреть детали',
            reply_markup=admin_keyboards.show_overdue_keyboard(overdue_orders)
        )
    else:
        await message.answer(
            text=f'Сегодня нет просроченных заказов.'
        )


@router.callback_query(Text(startswith=['overdue_order_']))
async def show_overdue_order_details(callback: CallbackQuery):
    order_id = int(callback.data.split(sep="_")[-1])
    order_phone = database_funcs.get_overdue_order_details(order_id)
    await callback.message.edit_text(
        text=f'Заказ №{order_id}\nТелефон: {order_phone}'
    )
