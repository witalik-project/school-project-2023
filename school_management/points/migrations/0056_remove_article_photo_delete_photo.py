# Generated by Django 4.1.5 on 2023-08-16 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0055_photo_alter_article_cover_photo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='photo',
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
