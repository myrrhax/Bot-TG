from dataclasses import dataclass
from typing import List

from aiogram import types
from aiogram.types import LabeledPrice

from data import config


@dataclass
class Item:
    title: str
    description: str
    start_parameter: str
    currency: str
    prices: List[LabeledPrice]
    provider_data: dict = None
    photo_url: str = None
    photo_size: int = None
    photo_width: int = None
    photo_height: int = None
    need_name: bool = False
    need_phone_number: bool = False
    need_email: bool = False
    need_shipping_address: bool = False
    send_phone_number_to_provider: bool = False
    send_email_to_provider: bool = False
    is_flexible: bool = False

    provider_token: str = config.PROVIDER_TOKEN

    def generate_invoice(self):
        return self.__dict__


REGULAR_POST_SHIPPING = types.ShippingOption(
    id='post',
    title='Обычная доставка',
    prices=[
        LabeledPrice(
            'Стандартная коробка', 0
        ),
        LabeledPrice(
            'Быстрая доставка', 500
        )
    ]
)

FAST_POST_SHIPPING = types.ShippingOption(
    id='vip_post',
    title='VIP доставка',
    prices=[
        LabeledPrice(
            'Прочная коробка', 500
        ),
        LabeledPrice(
            'Срочной почтой', 500
        )
    ]
)
