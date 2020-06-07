# Generated by Django 3.0.7 on 2020-06-07 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255, verbose_name='Full name')),
                ('job_title', models.CharField(max_length=255, verbose_name='Job title')),
                ('company', models.CharField(max_length=255, verbose_name='Company Name')),
                ('email', models.EmailField(max_length=254)),
                ('contact_number', models.CharField(max_length=62, verbose_name='Contact Number')),
                ('notes', models.TextField(verbose_name='Notes')),
                ('pid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
                'ordering': ('-modified',),
            },
        ),
    ]
