# Generated by Django 3.0.7 on 2020-07-20 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('line_app', '0015_auto_20200720_0600'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='linerichmenu',
            options={'ordering': ('index',)},
        ),
        migrations.AddField(
            model_name='linechannelmembership',
            name='current_rich_menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='line_app.LineRichMenu'),
        ),
    ]