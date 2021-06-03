from django.db import models
from jsonfield import JSONField


class Items(models.Model):
    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товар'

    item_id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Название товара', max_length=100)
    thumb = models.CharField(verbose_name='Ссылка на фото товара размера thumb', max_length=300)
    photo = models.CharField(verbose_name='Id или ссылка на фото товара', max_length=300)
    description = models.TextField(verbose_name='Описание', max_length=600)
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return f'{self.item_id} - {self.name}({self.price})'


class User(models.Model):
    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователь'

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(verbose_name='ID пользователя TG', unique=True, default=1)
    name = models.CharField(verbose_name='Имя пользователя TG', max_length=100)
    scores = models.IntegerField(verbose_name='Баллы рефферала', default=0)

    def __str__(self):
        return f'{self.user_id}({self.name})'


class Referral(models.Model):
    class Meta:
        verbose_name = 'Реферралы'
        verbose_name_plural = 'Реферрал'

    id = models.AutoField(primary_key=True)
    referrer_id = models.IntegerField(verbose_name='ID Реферера')
    referral_id = models.BigIntegerField()

    def __str__(self):
        return f'{self.referrer_id} привёл {self.referral_id}'


class Purchase(models.Model):
    class Meta:
        verbose_name = 'Покупки'
        verbose_name_plural = 'Покупка'

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, verbose_name='Id Пользователя в ТГ', on_delete=models.SET(0))
    item_id = models.ForeignKey(Items, verbose_name='ID товара', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Стоимость товара')
    quantity = models.IntegerField(verbose_name='Количество')
    time_purchase = models.DateTimeField(verbose_name='Время покупки', auto_now_add=True)
    shipping_address = JSONField(verbose_name='Место доставки', null=True)
    phone_number = models.CharField(verbose_name='Номер телефона', null=True, max_length=25)
    receiver_name = models.CharField(verbose_name='Имя получателя', max_length=100, null=True)
    status = models.BooleanField(verbose_name='Статус оплаты', default=False)

    def __str__(self):
        return f'{self.user_id} --> {self.item_id} ({self.quantity})'
