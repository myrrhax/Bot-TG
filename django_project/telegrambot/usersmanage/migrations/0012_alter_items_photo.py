# Generated by Django 3.2 on 2021-05-09 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0011_alter_items_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='photo',
            field=models.CharField(max_length=300, verbose_name='Id или ссылка на фото товара'),
        ),
    ]
