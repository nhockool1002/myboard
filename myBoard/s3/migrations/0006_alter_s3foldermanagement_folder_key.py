# Generated by Django 4.0 on 2021-12-11 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3', '0005_s3foldermanagement_bucket_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='s3foldermanagement',
            name='folder_key',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
