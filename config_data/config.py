from dataclasses import dataclass
from environs import Env


@dataclass
class PaymentToken:
    p_token: str


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    payment_token: PaymentToken


def load_config() -> Config:
    env: Env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        db=DatabaseConfig(database=env('DATABASE_NAME')),
        payment_token=PaymentToken(p_token=env('PAYMENT_TOKEN'))
    )


PHOTOS = {
    'Мейкап': 'https://images.belcy-storage.com/uploads/1/picture/file/25783/middle_shutterstock_284414423.jpg',
    'Покраска волос': 'https://www.jayneygoddard.org/wp-content/uploads/2020/01/hairdye-1.jpeg',
    'Маникюр': 'https://sun9-58.userapi.com/impf/c837425/v837425672/140dc/LVS_MHlwdmU.jpg?size=424x283&quality=96&sign=16f692a2a6a440bb056b7acf5e4132f0&c_uniq_tag=THMba5azdfNWU7cUQUvd82srg33i0vRijVMgc-Qm7g8&type=album'
}
