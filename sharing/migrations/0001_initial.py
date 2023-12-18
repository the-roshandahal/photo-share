# Generated by Django 5.0 on 2023-12-18 13:37

import django.db.models.deletion
import sharing.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gallery_name', models.CharField(max_length=255)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sharing.event')),
            ],
        ),
        migrations.CreateModel(
            name='Photographer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=sharing.models.generate_filename)),
                ('guest_name', models.CharField(max_length=255, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sharing.gallery')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sharing.photographer')),
            ],
        ),
    ]
