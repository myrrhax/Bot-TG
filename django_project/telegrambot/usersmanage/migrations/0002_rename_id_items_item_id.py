# Generated by Django 3.2 on 2021-05-03 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='items',
            old_name='id',
            new_name='item_id',
        ),
    ]
