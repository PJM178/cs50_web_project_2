# Generated by Django 4.0.6 on 2022-07-19 10:02

import auctions.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0035_alter_auctioncomments_comment_closedauctions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='closedauctions',
            name='item',
            field=models.ForeignKey(null=True, on_delete=models.SET(auctions.models.AuctionListing), to='auctions.auctionlisting'),
        ),
        migrations.AlterField(
            model_name='closedauctions',
            name='winner',
            field=models.ForeignKey(on_delete=models.SET(auctions.models.User), related_name='winning_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
