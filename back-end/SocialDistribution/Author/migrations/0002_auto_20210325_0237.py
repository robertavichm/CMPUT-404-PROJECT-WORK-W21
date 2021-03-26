# Generated by Django 3.1.7 on 2021-03-25 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Author', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='comment_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Author.comment'),
        ),
        migrations.AlterField(
            model_name='like',
            name='post_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Author.post'),
        ),
    ]