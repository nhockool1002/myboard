# Generated by Django 4.0 on 2021-12-10 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='s3bucketmanagement',
            name='is_deleted',
            field=models.BooleanField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='s3bucketmanagement',
            name='status',
            field=models.BooleanField(blank=True),
        ),
    ]