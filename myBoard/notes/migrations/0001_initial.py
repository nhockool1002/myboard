# Generated by Django 3.2.2 on 2021-12-21 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyBoardNotes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('note_key', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('note_content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'myboard_notes',
            },
        ),
    ]