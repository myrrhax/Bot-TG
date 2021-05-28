# Generated by Django 3.2 on 2021-05-09 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0012_alter_items_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='item_id',
            field=models.CharField(max_length=100, verbose_name='ID товара'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='price',
            field=models.IntegerField(verbose_name='Стоимость товара'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='user_id',
            field=models.IntegerField(max_length=100, verbose_name='ID покупателя в TG'),
        ),
    ]
