# Generated by Django 3.2 on 2021-05-03 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0002_rename_id_items_item_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='phone_number',
            field=models.IntegerField(max_length=50, null=True, verbose_name='Номер телефона'),
        ),
    ]
