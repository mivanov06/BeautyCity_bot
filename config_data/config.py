from dataclasses import dataclass
from environs import Env
from sqlite3_api.Table import Table
from sqlite3_api.field_types import List
from pathlib import Path


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


def load_config() -> Config:
    env: Env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        db=DatabaseConfig(database=env('DATABASE_NAME')),
        admin_ids=AdminIds(ids_list=env('ADMIN_IDS')),
        bitly_token=BitlyToken(b_token=env('BITLY_TOKEN'))
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
