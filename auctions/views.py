from time import time
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages

from .forms import ListingForm
from .forms import testi
from .forms import Watchlist
from .forms import CategoriesForm 
from .forms import BidForm
from .forms import CommentForm
from .forms import AuctionWinner
from .models import AuctionComments, AuctionListing, User, WatchList, Categories, AuctionBids, ClosedAuctions

#@login_required(login_url="/login")

def index(request):
    auctions = AuctionListing.objects.all()
    closed_auctions = ClosedAuctions.objects.values_list("item", flat = True)
    auctions = AuctionListing.objects.exclude(id__in=closed_auctions)
    return render(request, "auctions/index.html",{
        "auctions": auctions,
        "closed_auctions": closed_auctions
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == 'POST':
        form = testi(request.POST)
        category_form = CategoriesForm(request.POST)
        if form.is_valid() and category_form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image_url = form.cleaned_data["image_url"]
            category = category_form.cleaned_data["category"]
            categories = Categories(category = category)
            categories.save()
            auction = AuctionListing(lister = request.user, name = name, description = description, price = price,
                                    image_url = image_url, category = category, time = datetime.now())
            auction.save()
            #request.session["task"]
            return HttpResponseRedirect(reverse("create_listing"))
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form,
                "category": category_form
            })

    return render(request, "auctions/create_listing.html", {
        "form": testi(),
        "category": CategoriesForm()
        })

@login_required(login_url="/login")

def listings(request, listing_id):
    watchlist_check = WatchList.objects.all()
    auctions = AuctionListing.objects.get(pk = listing_id)
    watchlist_check_user = WatchList.objects.filter(user = request.user, item = auctions)
    check_winner = ClosedAuctions.objects.filter(item = auctions)
    if check_winner:
        comments = AuctionComments.objects.filter(item = auctions)
        if request.method == "POST":
            if 'watchlist' in request.POST:
                form = Watchlist(request.POST)
                if not watchlist_check_user:
                    if form.is_valid():
                        lister = request.user
                        item = AuctionListing.objects.get(pk = listing_id)
                        watchlist = WatchList(user = lister, item = item)
                        if not watchlist_check:
                            watchlist.save()
                        if not watchlist_check_user:
                            watchlist.save()
                        return HttpResponseRedirect(request.path_info)
                else:
                    if form.is_valid():
                        watchlist_check_user.delete()
                        return HttpResponseRedirect(request.path_info)
        return render(request, "auctions/listings.html",{
            "winner": check_winner,
            "auction": auctions,
            "watchlist": watchlist_check,
            "listing_id": listing_id,
            "watchlist_user":  watchlist_check_user,
            "bid_form": BidForm(),
            "comment_form": CommentForm(),
            "comments": comments,
            "auction_winner": AuctionWinner()
        })
    if request.method == "POST":
        if 'watchlist' in request.POST:
            form = Watchlist(request.POST)
            if not watchlist_check_user:
                if form.is_valid():
                    lister = request.user
                    item = AuctionListing.objects.get(pk = listing_id)
                    watchlist = WatchList(user = lister, item = item)
                    if not watchlist_check:
                        watchlist.save()
                    if not watchlist_check_user:
                        watchlist.save()
                    return HttpResponseRedirect(request.path_info)
            else:
                if form.is_valid():
                    watchlist_check_user.delete()
                    return HttpResponseRedirect(request.path_info)
        if 'bidlist' in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                lister = request.user
                item = AuctionListing.objects.get(pk = listing_id)
                bid = bid_form.cleaned_data["amount"]
                bids = AuctionBids(user = lister, item = item, amount = bid)
                if bid >= item.price and not AuctionBids.objects.filter(item = auctions):
                    bids.save()
                elif bid > item.price:
                    item.price = bid
                    item.save()
                    bids.save()
                else:
                    return redirect("error", listing_id = listing_id)
                return HttpResponseRedirect(request.path_info)
            else:
                return HttpResponseRedirect(request.path_info)
        if 'comments' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                lister = request.user
                item = AuctionListing.objects.get(pk = listing_id)
                comment = comment_form.cleaned_data["comment"]
                time = datetime.now()
                comments = AuctionComments(user = lister, item = item, comment = comment, time = time)
                comments.save()
                return HttpResponseRedirect(request.path_info)
            else:
                return HttpResponseRedirect(request.path_info)
        if 'closeauction' in request.POST:
            try:
                bid_winner = AuctionBids.objects.filter(item = auctions).latest("user")
                winner = bid_winner.user
            except:
                winner = request.user
            # user_list = []
            # for user in bid_winner:
            #     user_list.append(user.user)
            # winner = user_list[-1]
            item = auctions
            closed_auction = ClosedAuctions(winner = winner, item = item)
            closed_auction.save()
            return HttpResponseRedirect(request.path_info)
    else:
        auctions = AuctionListing.objects.get(pk = listing_id)
        comments = AuctionComments.objects.filter(item = auctions)
        return render(request, "auctions/listings.html",{
            "auction": auctions,
            "watchlist": watchlist_check,
            "listing_id": listing_id,
            "watchlist_user":  watchlist_check_user,
            "bid_form": BidForm(),
            "comment_form": CommentForm(),
            "comments": comments,
            "auction_winner": AuctionWinner()
    })

    auctions = AuctionListing.objects.get(pk = listing_id)
    return render(request, "auctions/listings.html",{
        "auction": auctions,
        "form": Watchlist(),
        "bid_form": BidForm()
    })

def watchlist(request):
    auctions = AuctionListing.objects.all()
    watchlist_check_user = WatchList.objects.filter(user = request.user)
    return render(request, "auctions/watchlist.html",{
        "auctions": auctions,
        "watchlist": watchlist_check_user
        })

def categories(request):
    categories = Categories.category.field.choices
    return render(request, "auctions/categories.html",{
        "categories": categories
    })

def category_id(request, category_id):
    closed_auctions = ClosedAuctions.objects.values_list("item", flat = True)
    auctions = AuctionListing.objects.exclude(id__in=closed_auctions).filter(category = category_id)
    categories = Categories.category.field.choices
    kategoriat = []
    for category in categories:
        kategoriat.append(category[1])
    category = kategoriat[int(category_id)-1]
    return render(request, "auctions/category_id.html",{
        "auctions": auctions,
        "category": category
    })

def error(request, listing_id):
        auctions = AuctionListing.objects.get(pk = listing_id)
        return render(request, "auctions/error.html",{
            "auction": auctions,
            "listing_id": listing_id
    })
