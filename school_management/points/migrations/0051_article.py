# Generated by Django 4.1.5 on 2023-08-15 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0050_remove_pointslog_points_log_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('cover_photo', models.ImageField(upload_to='')),
                ('description', models.TextField()),
            ],
        ),
    ]
