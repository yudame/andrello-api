# Generated by Django 2.1.7 on 2019-05-27 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_footer_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='_description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='blog',
            name='footer_text',
            field=models.TextField(blank=True, default=''),
        ),
    ]