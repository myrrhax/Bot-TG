from typing import List

from aiogram import types

from django_project.telegrambot.usersmanage.models import Items, User, Referral, Purchase
from asgiref.sync import sync_to_async


#  Юзеры
@sync_to_async
def add_user(user_id, name):
    try:
        user = User(user_id=int(user_id), name=str(name))
        user.save()
    except Exception:
        return select_user(user_id)


@sync_to_async
def select_user(user_id: int):
    user = User.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def update_score(user_id: int):
    user = User.objects.get(user_id=user_id)
    current_score = user.scores
    total_score = int(current_score) + 10
    user.scores = total_score
    user.save()


@sync_to_async
def check_score(user_id: int):
    current_score = User.objects.filter(user_id=user_id).first().scores
    return current_score


@sync_to_async
def minus_score(user_id: int, score: int):
    user = User.objects.get(user_id=user_id)
    current_score = user.scores
    total_score = int(current_score) - score
    user.scores = total_score
    user.save()


#  Товары
@sync_to_async
def add_item(name, thumb, photo, description, price):
    item = Items(name=name, thumb=thumb, photo=photo, description=description,
                 price=price)
    return item.save()


@sync_to_async
def select_item(item_id: int):
    item = Items.objects.filter(item_id=item_id).first()
    return item


@sync_to_async
def select_all_items():
    items = Items.objects.order_by('name')
    return items


@sync_to_async
def inline_selector(query):
    items = Items.objects.filter(name__icontains=query).order_by('name')
    return items


# Реффералы

@sync_to_async
def add_referral(referrer, referral):
    referral = Referral(referrer_id=referrer, referral_id=referral)
    return referral.save()


# Покупки

@sync_to_async
def add_to_buy(user_id: User, item_id: Items, price: int,
               quantity: int, shipping_address: dict = None,
               phone_number: int = None, receiver_name: str = None,
               status=True):
    purchase = Purchase(user_id=user_id, item_id=item_id, price=price,
                        quantity=quantity, shipping_address=shipping_address,
                        phone_number=phone_number, receiver_name=receiver_name,
                        status=status)
    return purchase.save()
