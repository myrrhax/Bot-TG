# Generated by Django 3.2 on 2021-05-04 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0004_alter_purchase_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='scores',
            field=models.IntegerField(default=0, verbose_name='Баллы рефферала'),
        ),
    ]