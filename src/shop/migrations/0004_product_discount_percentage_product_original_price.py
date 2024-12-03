# Generated by Django 5.0.9 on 2024-12-03 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_tag_options_tag_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_percentage',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='product',
            name='original_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
