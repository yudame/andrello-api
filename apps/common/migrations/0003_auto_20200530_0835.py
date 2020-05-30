# Generated by Django 3.0.6 on 2020-05-30 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20200512_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.CharField(blank=True, help_text='State, Province, etc', max_length=10, null=True),
        ),
    ]
