# Generated by Django 3.2 on 2021-05-19 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0016_delete_basket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='phone_number',
            field=models.CharField(max_length=25, null=True, verbose_name='Номер телефона'),
        ),
    ]