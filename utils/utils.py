import os

from aiogram.types import FSInputFile

from config_data.config import load_config
import qrcode

import requests

import datetime as dt
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BeautyCity_bot.settings")

import django

django.setup()

from bot.models import *


def set_table():
    today = dt.date.today()
    d = (False, False, True, False, False, True, True, False, False, True)