# Generated by Django 3.1.7 on 2021-02-28 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Author', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='Type',
            new_name='type',
        ),
    ]
