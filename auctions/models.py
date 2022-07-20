from logging import PlaceHolder
from sre_parse import CATEGORIES
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import FloatField


class User(AbstractUser):
    pass

class Categories(models.Model):
    CATEGORIES = (
        ('1','Other'),
        ('2', 'TV'),
        ('3', 'Laptop'),
        ('4', 'Smartphone'),
        ('5', 'Tablet')
    )
    category = models.CharField(max_length=1, blank=False, choices=CATEGORIES, default="1")
    

class AuctionListing(models.Model):
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister", null=True)
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, blank=True)
    price = models.FloatField()
    image_url = models.URLField(blank=True)
    CATEGORIES = (
        ('1','Other'),
        ('2', 'TV'),
        ('3', 'Laptop'),
        ('4', 'Smartphone'),
        ('5', 'Tablet')
    )
    category = models.CharField(max_length=1, blank=False, choices=CATEGORIES)
    # category = models.CharField(max_length=50, blank=True)
    # category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="categories")
    time = models.DateTimeField()

class AuctionBids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", null=True)
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bid_item", null=True)
    amount = models.FloatField()

class AuctionComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="commenter", null=True)
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comment_item", null=True)
    comment = models.CharField(max_length=1000, verbose_name="")
    time = models.DateTimeField()

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user", null=True)
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlist_item", null=True)

class ClosedAuctions(models.Model):
    winner = models.ForeignKey(User, on_delete=models.SET(User), related_name="winning_user", null=True)
    item = models.ForeignKey(AuctionListing, on_delete=models.SET(AuctionListing), null=True)
