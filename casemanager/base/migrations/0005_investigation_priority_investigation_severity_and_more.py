# Generated by Django 4.0.5 on 2022-07-25 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_case_options_alter_message_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigation',
            name='priority',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='investigation',
            name='severity',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='investigation',
            name='state',
            field=models.CharField(default='New', max_length=200),
        ),
    ]
