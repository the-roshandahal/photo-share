# Generated by Django 5.0 on 2023-12-18 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0002_event_event_credentials_event_secret_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]