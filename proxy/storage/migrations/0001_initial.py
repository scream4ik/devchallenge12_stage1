# Generated by Django 2.0.5 on 2018-05-12 23:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import drf_chunked_upload.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Replica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_domain', models.CharField(max_length=40, unique=True)),
                ('public_port', models.SmallIntegerField()),
                ('free_space', models.BigIntegerField(default=0, editable=False)),
                ('status', models.CharField(choices=[('online', 'online'), ('offline', 'offline')], default='offline', editable=False, max_length=7)),
                ('ssh_host', models.CharField(max_length=20)),
                ('ssh_user', models.CharField(max_length=20)),
                ('ssh_password', models.CharField(max_length=20)),
                ('ssh_port', models.SmallIntegerField(default=22)),
            ],
        ),
        migrations.CreateModel(
            name='TmpChunkedUpload',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(max_length=255, null=True, upload_to=drf_chunked_upload.models.generate_filename)),
                ('filename', models.CharField(max_length=255)),
                ('offset', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Incomplete'), (2, 'Complete')], default=1)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, limit_choices_to={'parent': None}, null=True, on_delete=django.db.models.deletion.CASCADE, to='storage.TmpChunkedUpload', related_name='versions')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='tmpchunkedupload', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='replica',
            name='chunked',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.TmpChunkedUpload'),
        ),
        migrations.AddField(
            model_name='replica',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.Server'),
        ),
        migrations.AlterUniqueTogether(
            name='replica',
            unique_together={('chunked', 'server')},
        ),
    ]
