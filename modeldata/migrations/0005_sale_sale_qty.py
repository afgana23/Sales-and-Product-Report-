# Generated by Django 4.2.5 on 2023-12-18 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modeldata', '0004_alter_asset_amount_alter_sale_sale_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='sale_qty',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
