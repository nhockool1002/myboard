# Generated by Django 4.0.2 on 2022-05-27 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyBoardPaymentReminder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('payment_content', models.TextField(blank=True, null=True)),
                ('payment_due_date', models.DateTimeField(null=True)),
                ('payment_price', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('payment_status', models.BooleanField(default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'myboard_payment_reminder',
            },
        ),
    ]