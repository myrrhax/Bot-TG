# Generated by Django 3.2.3 on 2021-06-03 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0017_alter_purchase_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='price',
            field=models.IntegerField(verbose_name='Цена'),
        ),
    ]