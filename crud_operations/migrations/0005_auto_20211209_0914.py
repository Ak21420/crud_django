# Generated by Django 3.2.9 on 2021-12-09 09:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud_operations', '0004_auto_20211209_0702'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender_CNN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=128)),
                ('pred', models.BooleanField()),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 12, 9, 9, 14, 37, 820287))),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='GenderCNN',
        ),
    ]
