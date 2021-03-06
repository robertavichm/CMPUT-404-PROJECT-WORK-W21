# Generated by Django 3.1.7 on 2021-03-03 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Author', '0006_auto_20210301_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='like_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Author.like'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='post_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Author.post'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='request_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Author.friendship'),
        ),
    ]
