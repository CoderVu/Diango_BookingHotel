# Generated by Django 5.0.3 on 2024-04-23 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krishna', '0006_auto_20200808_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hotels',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='hotels',
            name='name',
            field=models.CharField(default='VietNam', max_length=30),
        ),
        migrations.AlterField(
            model_name='hotels',
            name='state',
            field=models.CharField(default='Hotel', max_length=50),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='room_type',
            field=models.CharField(choices=[('1', 'Premium'), ('2', 'Deluxe'), ('3', 'Basic')], max_length=50),
        ),
    ]