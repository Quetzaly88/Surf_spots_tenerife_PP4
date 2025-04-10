# Generated by Django 5.1.4 on 2025-01-04 21:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_account', '0002_surfspot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surfspot',
            name='location',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='surfspot',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('surf_spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users_account.surfspot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
