# Generated by Django 3.1.7 on 2021-03-24 06:20

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('post_id', models.TextField()),
                ('author_id', models.TextField()),
                ('contentType', models.TextField()),
                ('published', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('comment', models.TextField()),
                ('type', models.TextField(default='comment')),
            ],
        ),
        migrations.CreateModel(
            name='FriendShip',
            fields=[
                ('FriendShipId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author_friend', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('like_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('liker_id', models.TextField()),
                ('comment_id', models.TextField()),
                ('post_id', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('displayName', models.TextField()),
                ('host', models.TextField()),
                ('url', models.TextField()),
                ('type', models.TextField()),
                ('github', models.TextField(null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('type', models.TextField(default='post')),
                ('description', models.TextField()),
                ('source', models.TextField()),
                ('origin', models.TextField()),
                ('contentType', models.TextField(choices=[('text/plain', 'Choice1'), ('text/markdown', 'Choice2'), ('application/base64', 'Choice3'), ('image/png;base64', 'Choice4'), ('image/jpeg;base64', 'Choice5')])),
                ('content', models.TextField()),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, size=None)),
                ('commentLink', models.TextField()),
                ('commentCount', models.IntegerField(default=0)),
                ('pageSize', models.IntegerField()),
                ('published', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('visibility', models.TextField()),
                ('unlisted', models.BooleanField()),
                ('author_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Author.comment')),
                ('like_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Author.like')),
                ('post_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Author.post')),
                ('request_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Author.friendship')),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='author_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendship',
            name='author_primary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary', to=settings.AUTH_USER_MODEL),
        ),
    ]
