# Generated by Django 3.1.7 on 2021-03-01 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Author', '0002_auto_20210228_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Type',
            field=models.TextField(default='post'),
        ),
    ]