# Generated by Django 2.2.4 on 2019-08-14 22:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('slackbot', '0008_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='coffeerequest',
            name='block_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='block_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
