from dataclasses import dataclass
from environs import Env
from sqlite3_api.Table import Table
from sqlite3_api.field_types import List
from pathlib import Path


@dataclass
class PaymentToken:
    p_token: str

@dataclass
class BitlyToken:
    b_token: str


@dataclass
class AdminIds:
    ids_list: list  # список телеграм id админов


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
#     db_host: str          # URL-адрес базы данных
#     db_user: str          # Username пользователя базы данных
#     db_password: str      # Пароль к базе данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    # admin_ids: list  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    admin_ids: AdminIds
    bitly_token: BitlyToken
    payment_token: PaymentToken


def load_config() -> Config:
    env: Env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        db=DatabaseConfig(database=env('DATABASE_NAME')),
        admin_ids=AdminIds(ids_list=env('ADMIN_IDS')),
        bitly_token=BitlyToken(b_token=env('BITLY_TOKEN')),
        payment_token=PaymentToken(p_token=env('PAYMENT_TOKEN'))
    )


# Заполнение таблицы полями. Поле id (создается автоматически, поэтому
# здесь не указано), является PRIMARY KEY. Будем считать, что это номер заказа
class Users(Table):
    user_id: int  # Телеграм id клиента.
    weight: str  # Масса вещей.
    storage_time: str  # Время хранения.
    phone: str
    deliver: str  # Самостоятельная доставка либо курьером
    address: str  # Адрес клиента. Если пустое, то клиент
    # привезет свои вещи сам.
    dimension: str  # Значение габаритов ячейки. Если пустое,
    # то клиент не хочет сам мерять.
    cell_number: List  # Список с номерами ячеек хранения
    # для данного клиента.
    expiration_time: str  # Время истечения срока хранения.
    is_processed: str  # Обработанный заказ True. Новый False
    date: str  # Дата самостоятельной доставки клиентом


# Таблица с короткими ссылками для отслеживания статистики
class BitlyUrls(Table):
    name: str  # Название ссылки
    link: str  # Ссылка


my_table = Users(db_path=load_config().db.database)
links_table = BitlyUrls(db_path=load_config().db.database)

PRICES = {
    'Мейкап': 800,
    'Покраска волос': 500,
    'Маникюр': 700
}

PHOTOS = {
    'Мейкап': 'https://images.belcy-storage.com/uploads/1/picture/file/25783/middle_shutterstock_284414423.jpg',
    'Покраска волос': 'https://www.jayneygoddard.org/wp-content/uploads/2020/01/hairdye-1.jpeg',
    'Маникюр': 'https://sun9-58.userapi.com/impf/c837425/v837425672/140dc/LVS_MHlwdmU.jpg?size=424x283&quality=96&sign=16f692a2a6a440bb056b7acf5e4132f0&c_uniq_tag=THMba5azdfNWU7cUQUvd82srg33i0vRijVMgc-Qm7g8&type=album'
}
