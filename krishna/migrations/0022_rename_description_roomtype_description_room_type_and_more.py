# Generated by Django 5.0.4 on 2024-05-04 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('krishna', '0021_remove_roomtype_description_room_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomtype',
            old_name='description',
            new_name='description_room_type',
        ),
        migrations.RenameField(
            model_name='roomtype',
            old_name='room_type',
            new_name='type_name',
        ),
    ]
