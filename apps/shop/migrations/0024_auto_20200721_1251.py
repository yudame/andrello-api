# Generated by Django 3.0.7 on 2020-07-21 12:51

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('line_app', '0019_auto_20200720_1421'),
        ('common', '0006_auto_20200721_1251'),
        ('shop', '0023_auto_20200720_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('status_log', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=1, max_digits=8)),
                ('is_ad_hoc_item', models.BooleanField(default=False)),
                ('ad_hoc_name', models.CharField(blank=True, default='', max_length=100)),
                ('ad_hoc_price_currency', djmoney.models.fields.CurrencyField(choices=[('THB', 'Baht')], default='THB', editable=False, max_length=3)),
                ('ad_hoc_price', djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='THB', max_digits=8, null=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='shop.Item')),
                ('notes', models.ManyToManyField(blank=True, to='common.Note')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='shop.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='orders', through='shop.OrderItem', to='shop.Item'),
        ),
        migrations.AddField(
            model_name='order',
            name='line_channel_membership',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='line_app.LineChannelMembership'),
        ),
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.ManyToManyField(blank=True, to='common.Note'),
        ),
    ]
