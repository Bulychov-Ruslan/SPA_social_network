# Generated by Django 4.2.6 on 2023-11-26 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_conversationmessage_file_conversationmessage_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversationmessage',
            name='file',
        ),
        migrations.RemoveField(
            model_name='conversationmessage',
            name='photo',
        ),
    ]
