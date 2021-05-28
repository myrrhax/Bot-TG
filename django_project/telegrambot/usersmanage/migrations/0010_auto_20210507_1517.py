# Generated by Django 3.2 on 2021-05-07 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0009_auto_20210505_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='thumb',
            field=models.CharField(default=1, max_length=300, verbose_name='Ссылка на фото товара размера thumb'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='items',
            name='photo',
            field=models.CharField(max_length=300, verbose_name='Фото товара'),
        ),
    ]
