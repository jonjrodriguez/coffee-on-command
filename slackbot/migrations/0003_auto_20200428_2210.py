# Generated by Django 2.2.4 on 2020-04-28 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slackbot', '0002_coffeerequest_command'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffeerequest',
            name='command',
            field=models.CharField(choices=[('/coffee', 'Coffee'), ('/mocha', 'Mocha')], default='/coffee', max_length=255),
        ),
    ]