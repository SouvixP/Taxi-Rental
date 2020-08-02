# Generated by Django 3.0.2 on 2020-07-26 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('taxi', '0003_auto_20200713_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('licence_no', models.CharField(max_length=100)),
            ],
        ),
    ]