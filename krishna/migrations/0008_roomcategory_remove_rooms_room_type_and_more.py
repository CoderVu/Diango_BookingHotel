# Generated by Django 5.0.3 on 2024-04-23 13:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krishna', '0007_rooms_image_alter_hotels_id_alter_hotels_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomtype', models.CharField(max_length=50)),
                ('image_category', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='room_type',
        ),
        migrations.AddField(
            model_name='rooms',
            name='room_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='krishna.roomcategory'),
            preserve_default=False,
        ),
    ]
