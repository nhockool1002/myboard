# Generated by Django 3.2.2 on 2022-01-03 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExCategories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.TextField(blank=True, null=True)),
                ('category_slug', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('order', models.IntegerField(blank=True, default=0, null=True)),
                ('sticky', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'ex_categories',
            },
        ),
    ]
