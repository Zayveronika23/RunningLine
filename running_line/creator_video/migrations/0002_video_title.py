# Generated by Django 3.2.16 on 2024-09-16 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator_video', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='title',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
