# Generated by Django 4.0 on 2021-12-11 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3', '0004_s3filemanagement_s3foldermanagement'),
    ]

    operations = [
        migrations.AddField(
            model_name='s3foldermanagement',
            name='bucket_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
