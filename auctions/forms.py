from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import AuctionBids, AuctionComments, AuctionListing
from .models import WatchList
from .models import Categories
from .models import ClosedAuctions
import datetime


class ListingForm(forms.Form):
    name = forms.CharField(label="Name")
    description = forms.CharField(label="Description")
    price = forms.FloatField(label="Starting bid")
    image_url = forms.CharField(label="Url to image")
    category = forms.CharField(label="Category")

class testi(forms.ModelForm):
    #category = forms.ChoiceField(choices=AuctionListing.CATEGORIES, required=False)
    class Meta:
        model = AuctionListing
        exclude = ['lister', 'time', 'category']

class CategoriesForm(forms.ModelForm):
    #category = forms.ChoiceField(choices=AuctionListing.CATEGORIES, required=False)
    class Meta:
        model = Categories
        exclude = ['user', 'item']

class Watchlist(forms.Form):
    class Meta:
        model = WatchList

class BidForm(forms.ModelForm):
    class Meta:
        model = AuctionBids
        exclude = ['user', 'item']

class CommentForm(forms.ModelForm):
    class Meta:
        model = AuctionComments
        exclude = ['user', 'item', 'time']

class AuctionWinner(forms.ModelForm):
    class Meta:
        model = ClosedAuctions
        exclude = ['winner', 'item']