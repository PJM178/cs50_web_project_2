# Generated by Django 4.0.6 on 2022-07-17 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_alter_auctionlisting_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(choices=[('1', 'Other'), ('2', 'TV'), ('3', 'Laptop'), ('4', 'Smartphone'), ('5', 'Tablet')], max_length=1),
        ),
    ]
