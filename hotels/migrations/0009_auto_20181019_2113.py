# Generated by Django 2.1 on 2018-10-19 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotels', '0008_auto_20181019_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('num_rooms', models.PositiveIntegerField()),
                ('amount', models.PositiveIntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='room',
            name='type_name',
            field=models.CharField(default='Deluxe', max_length=100),
        ),
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.Room'),
        ),
    ]