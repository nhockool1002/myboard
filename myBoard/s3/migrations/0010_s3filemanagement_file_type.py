# Generated by Django 3.2.2 on 2021-12-27 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3', '0009_auto_20211213_0217'),
    ]

    operations = [
        migrations.AddField(
            model_name='s3filemanagement',
            name='file_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
