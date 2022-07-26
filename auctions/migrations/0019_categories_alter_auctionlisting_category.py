# Generated by Django 4.0.6 on 2022-07-17 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, choices=[('1', 'Other'), ('2', 'TV'), ('3', 'Laptop'), ('4', 'Smartphone'), ('5', 'Tablet')], max_length=1)),
            ],
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(blank=True, choices=[('1', 'Other'), ('2', 'TV'), ('3', 'Laptop'), ('4', 'Smartphone'), ('5', 'Tablet')], max_length=50),
        ),
    ]
