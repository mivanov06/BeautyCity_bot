from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery, FSInputFile, pre_checkout_query, successful_payment, LabeledPrice
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types.message import ContentType
from aiogram.methods.send_invoice import SendInvoice

from config_data.config import my_table, load_config, PRICES, PHOTOS
from keyboards import user_keyboards
from lexicon.lexicon_ru import LEXICON_RU
from aiogram3_calendar import DialogCalendar, dialog_cal_callback

from database import database_funcs
from utils.utils import entry_to_database, get_qrcode

router = Router()

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BeautyCity_bot.settings")

import django

django.setup()

from bot.models import *



class MyCellsState(StatesGroup):
    cell_number = State()
    all_things = State()  # True клиент заберет все вещи, если часть - False


class GetUserInfo(StatesGroup):
    new_user = State()
    service = State()  # Тип косметической процедуры
    master = State()  # Специалист, к которому происходит запись
    date = State()  # Дата посещения
    time = State()  # Время посещения
    name = State()  # Имя, которое ввел клиент
    phone = State()  # Телефон клиента
    pay = State()  # Оплатил ли клиент процедуру сразу (True/False)
    pay_yes = State()
    pay_no = State()


class GetCommentInfo(StatesGroup):
    text = State()
    user_name = State()
    save = State()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=user_keyboards.start_keyboard()
    )


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.send.answer(
        text=LEXICON_RU['/help'],
    )


@router.message(Text(contains=['Что можно хранить']))
async def process_what_can_be_stored(message: Message):
    await message.answer(
        text='Ознакомиться с правилами хранения:',
        reply_markup=user_keyboards.what_can_be_stored_keyboard()
    )


# --------------------------------------------------------------------------


@router.message(Text(contains=['Оставить отзыв']))
async def set_text_comment(message: Message, state: FSMContext):
    await message.answer(
        text='Напишите отзыв:'
    )
    await state.set_state(GetCommentInfo.text)


@router.message(GetCommentInfo.text)
async def set_user_name_comment(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await message.answer(
        text='Ваше имя:'
    )
    await state.set_state(GetCommentInfo.save)


@router.message(GetCommentInfo.save)
async def save_comment(message: Message, state: FSMContext):
    user_name = message.text
    user_data = await state.get_data()
    await state.update_data(user_name=user_name)
    comment = Comment.objects.create()
    comment.text = user_data['text']
    comment.user_name = user_name
    comment.save()

    await message.answer(
        text='Спасибо об отзыве о нашем салоне красоты!',
        reply_markup=user_keyboards.start_keyboard()

    )
    await state.clear()


# --------------------------------------------------------------------------


@router.message(Text(contains=['Записаться']))
async def sign_up(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU['rules'],
        reply_markup=user_keyboards.agree_keyboard()
    )
    user_id = int(message.from_user.id)
    await state.update_data(user_id=user_id)
    await state.set_state(GetUserInfo.new_user)


@router.callback_query(Text(text=['call_us']))
async def call_us(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Мы рады звонку в любое время\n8(800) 555 35 35'
    )


@router.callback_query(Text(text=['agree']), GetUserInfo.new_user)
async def get_service_type(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Выберите услугу:',
        reply_markup=user_keyboards.type_service_keyboard()
    )
    await state.update_data(service=callback.data)
    await state.set_state(GetUserInfo.service)
    await callback.answer()


@router.callback_query(Text(startswith=['service']), GetUserInfo.service)
async def get_master(callback: CallbackQuery, state: FSMContext):
    service = callback.data.split()[1]
    await state.update_data(service=service)

    await callback.message.edit_text(
        text='К какому мастеру вы хотите записаться?',
        reply_markup=user_keyboards.masters_keyboard(service)
    )
    await state.set_state(GetUserInfo.master)
    await callback.answer()


@router.callback_query(Text(startswith=['master']), GetUserInfo.master)
async def get_procedure_date(callback: CallbackQuery, state: FSMContext):
    master = callback.data.split()[1]
    await state.update_data(master=master)

    await callback.message.edit_text(
        text='Выберите дату:',
        reply_markup=user_keyboards.date_work_master_keyboard(master)
    )
    await state.set_state(GetUserInfo.date)
    await callback.answer()


@router.callback_query(Text(startswith=['date']), GetUserInfo.date)
async def get_procedure_time(callback: CallbackQuery, state: FSMContext):
    date = callback.data.split()[1]
    user_data = await state.get_data()
    await state.update_data(date=date)

    master_id = user_data['master']
    service_id = user_data['service']
    await callback.message.edit_text(
        text='Выберите время:',
        reply_markup=user_keyboards.time_work_master_keyboard(master_id, service_id, date)
    )
    await state.set_state(GetUserInfo.time)
    await callback.answer()


@router.callback_query(Text(startswith=['time']), GetUserInfo.time)
async def get_user_name(callback: CallbackQuery, state: FSMContext):
    time = callback.data.split()[1]
    await state.update_data(time=time)

    await callback.message.edit_text(
        text='Введите свое имя:'
    )
    await state.set_state(GetUserInfo.name)
    await callback.answer()


@router.message(GetUserInfo.name)
async def get_phone_number(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)

    await message.answer(
        text='Введите ваш номер телефона для связи:'
    )
    await state.set_state(GetUserInfo.phone)


@router.message(GetUserInfo.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)
    user_data = await state.get_data()
    date = user_data['date']
    await message.answer(
        text=f'Спасибо за запись! До встречи {date} по адресу address.\nХотите оплатить сразу?',
        reply_markup=user_keyboards.pay_keyboard()
    )

    await state.set_state(GetUserInfo.pay)


@router.callback_query(Text(contains=['pay_no']))
async def check_pay(callback: CallbackQuery, state: FSMContext):
    print('pay_no')
    user_data = await state.get_data()
    date = user_data['date']
    time = user_data['time']
    await state.update_data(pay=False)
    # write DB
    await callback.message.edit_text(
        text=f"Спасибо за запись! До встречи {date} {time} по адресу address"
    )
    await state.clear()


@router.callback_query(Text(contains=['pay_yes']))
async def process_storage_conditions(message: Message, bot: Bot, state: FSMContext):
    user_data = await state.get_data()
    print(user_data['service'])
    service = Service.objects.get(pk=user_data['service'])
    print(service)
    price = [LabeledPrice(label=str(service.name), amount=int(service.price*100))]
    print(price)
    await bot.send_invoice(
        message.from_user.id,
        title=service.name,
        description='Оплата косметической поцедуры.',
        provider_token=load_config().payment_token.p_token,
        currency='rub',
        photo_url=PHOTOS[f'{service.name}'],
        is_flexible=False,
        prices=price,
        start_parameter='example',
        payload='test-invoice-payload'
    )

    await state.set_state(GetUserInfo.pay_yes)


# @router.message(GetUserInfo.pay_yes)
# async def pay(message: Message, state: FSMContext):
#     user_name = message.text
#     user_data = await state.get_data()
#     await state.update_data(user_name=user_name)
#     await message.answer(
#         text='Оплата произведена',
#         reply_markup=user_keyboards.start_keyboard()
#
#     )
#     await state.clear()


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: pre_checkout_query.PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message()
async def successful_payment(message: successful_payment.SuccessfulPayment, state:FSMContext):
    schedule = Schedule.objects.create()
    user_data = await state.get_data()
    user = User.objects.get_or_create(telegram_id=user_data['user_id'])
    user.name = user_data['name']

    print(f'{user_data["user_id"]=} {user_data["user_name"]}')
    #в процессе



# Ветвь "Мои ячейки"
@router.message(Text(contains=['Мои ячейки']))
async def output_my_cells_menu(message: Message):
    user_id = message.from_user.id
    is_user = database_funcs.check_user(user_id)
    if is_user:
        if not database_funcs.get_user_cells(user_id):
            await message.answer(
                text=f'Ваш заказ в обработке.'
            )
        else:
            cell_number = database_funcs.get_user_cells(user_id)
            await message.answer(
                text=f'{cell_number}',
                reply_markup=user_keyboards.output_my_cells_keyboard()
            )
    else:
        await message.answer(
            text=f'У вас нет вещей на хранении.'
        )


@router.callback_query(Text(text=['extend_storage']))
async def get_cell_number(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_cells = database_funcs.get_user_cells(user_id)
    await callback.message.edit_text(
        text='Выберите ячейку, для которой хотите продлить срок хранения:',
        reply_markup=user_keyboards.generate_my_cells_keyboard(user_cells)
    )


@router.callback_query(Text(startswith=['cell_']))
async def extend_rental_period_cmd(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cell_number=callback.data.split(sep="_")[-1])
    # отправить номер ячейки и время продления в админку, раздел "Запросы на продление"
    await callback.message.edit_text(
        text='Выберите срок продления аренды:',
        reply_markup=user_keyboards.extend_rental_period_keyboard()
    )


@router.callback_query(Text(startswith=['extend_']))
async def send_success_extend_message(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Ваш запрос на продление срока аренды принят. \n'
             'Менеджер свяжется с вами в ближайшее время для '
             'уточнения деталей.'
    )


@router.callback_query(Text(text=['pick_up_some_things', 'pick_up_all_things']))
async def output_pick_up_things_buttons(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Заберете вещи сами?',
        reply_markup=user_keyboards.generate_pick_up_things_keyboard()
    )

    if callback.data == 'pick_up_some_things':
        await state.update_data(all_things=False)  # клиент заберет часть вещей
    else:
        await state.update_data(all_things=True)  # клиент заберет все вещи


@router.callback_query(Text(text=['pick_up_myself', 'deliver_home']))
async def output_pick_up_cells_buttons(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_cells = database_funcs.get_user_cells(user_id)
    await callback.message.edit_text(
        text='Выберите ячейку, из которой хотите забрать вещи:',
        reply_markup=user_keyboards.generate_pick_up_cells_keyboard(user_cells)
    )
    if callback.data == 'deliver_home':
        await state.update_data(deliver=True)  # доставить вещи клиенту на дом
    else:
        await state.update_data(deliver=False)  # клиент заберет вещи сам


@router.callback_query(Text(startswith=['pick_up_cell_']))
async def output_pick_up_cells_buttons(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    deliver = data.get('deliver')
    all_things = data.get('all_things')
    cell_number = data.get('cell_number')
    if deliver:
        await callback.message.edit_text(
            text='Менеджер свяжется с вами в ближайшее время для '
                 'уточнения деталей доставки ваших вещей.'
        )
    else:
        qr_data = f'user_id={user_id}, cell_number={cell_number}'
        photo = get_qrcode(qr_data)
        if all_things:
            await callback.message.answer_photo(photo, caption='Предьявите QR-код на складе, для получения вещей')
        else:
            await callback.message.answer_photo(photo, caption='Предьявите QR-код на складе, для получения вещей')
    await state.clear()
