# Generated by Django 4.2.6 on 2023-12-10 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_postattachment_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postattachment',
            name='image',
        ),
        migrations.RemoveField(
            model_name='postattachment',
            name='video',
        ),
        migrations.AddField(
            model_name='postattachment',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='post_attachments/test/'),
        ),
    ]
