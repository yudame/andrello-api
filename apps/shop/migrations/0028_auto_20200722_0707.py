# Generated by Django 3.0.7 on 2020-07-22 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('line_app', '0019_auto_20200720_1421'),
        ('shop', '0027_order_draft_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='line_channel_membership',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='line_app.LineChannelMembership'),
        ),
    ]
