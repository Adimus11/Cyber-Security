# Generated by Django 2.1.3 on 2018-11-22 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20181121_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='date',
            field=models.DateTimeField(blank=True, default=None),
        ),
    ]