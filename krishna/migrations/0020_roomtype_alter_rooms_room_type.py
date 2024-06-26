# Generated by Django 5.0.4 on 2024-05-03 00:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krishna', '0019_userprofile_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50)),
                ('description_room_type', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='rooms',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='krishna.roomtype'),
        ),
    ]
