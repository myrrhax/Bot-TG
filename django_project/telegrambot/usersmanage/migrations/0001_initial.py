# Generated by Django 3.2 on 2021-05-03 17:25

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Название товара')),
                ('photo', models.CharField(max_length=300, verbose_name='Ссылка на фото товара')),
                ('description', models.TextField(max_length=600, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Товары',
                'verbose_name_plural': 'Товар',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.BigIntegerField(default=1, unique=True, verbose_name='ID пользователя TG')),
                ('name', models.CharField(max_length=100, verbose_name='Имя пользователя TG')),
            ],
            options={
                'verbose_name': 'Пользователи',
                'verbose_name_plural': 'Пользователь',
            },
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='usersmanage.user')),
                ('referrer_id', models.BigIntegerField()),
            ],
            options={
                'verbose_name': 'Реферралы',
                'verbose_name_plural': 'Реферрал',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Стоимость товара')),
                ('quantity', models.IntegerField(verbose_name='Количество')),
                ('time_purchase', models.DateTimeField(auto_now_add=True, verbose_name='Время покупки')),
                ('shipping_address', jsonfield.fields.JSONField(null=True, verbose_name='Место доставки')),
                ('phone_number', models.BigIntegerField(max_length=50, null=True, verbose_name='Номер телефона')),
                ('receiver_name', models.CharField(max_length=100, null=True, verbose_name='Имя получателя')),
                ('status', models.BooleanField(default=False, verbose_name='Статус оплаты')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersmanage.items', verbose_name='ID товара')),
                ('user_id', models.ForeignKey(on_delete=models.SET(0), to='usersmanage.user', verbose_name='ID покупателя в TG')),
            ],
            options={
                'verbose_name': 'Покупки',
                'verbose_name_plural': 'Покупка',
            },
        ),
    ]