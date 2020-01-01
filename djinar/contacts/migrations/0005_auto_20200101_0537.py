# Generated by Django 3.0.1 on 2020-01-01 05:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_auto_20200101_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='pid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
