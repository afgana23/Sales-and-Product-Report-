# Generated by Django 4.2.5 on 2023-12-19 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modeldata', '0006_alter_sale_qty_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sale_qty',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
