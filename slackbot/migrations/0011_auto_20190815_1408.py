# Generated by Django 2.2.4 on 2019-08-15 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('slackbot', '0010_matchslackmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlackMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel', models.CharField(max_length=255)),
                ('ts', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='MatchSlackMessage',
        ),
        migrations.AddField(
            model_name='coffeerequest',
            name='initial_message',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coffee_request', to='slackbot.SlackMessage'),
        ),
        migrations.AddField(
            model_name='match',
            name='initial_message',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match', to='slackbot.SlackMessage'),
        ),
    ]