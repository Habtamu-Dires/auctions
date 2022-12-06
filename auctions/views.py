import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Listing,Category, Bid, Comment, Watchlist

def index(request):
    active_listing = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "listings": active_listing
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
    if request.method == "POST":
        user = request.user
        title = request.POST['title']
        description = request.POST['description']        
        category =Category.objects.get(name=request.POST['category'])
        image = request.POST['image']
        price = request.POST['starting_bid']
        #create the listing
        listing = Listing(owner=user,title=title, description=description, category=category, 
                            image=image, price=price, date=datetime.datetime.now())
        listing.save()
        bid = Bid(user=user,listing = listing, amount= request.POST['starting_bid'])
        bid.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html",{
            "categories": Category.objects.all()
        })

def listing_page(request, listing_id, open):
    listing = Listing.objects.get(id=listing_id)
    bids = Bid.objects.all()
    bid_counter = 0
    for bid in bids:
        if bid.listing.id == listing_id:
            bid_counter += 1
            if float(bid.amount) == float(listing.price):
                max_bid = bid

    if request.method == "POST":
        if 'comment' in request.POST:
            comment = Comment(user = request.user, listing=listing, 
                                comment = request.POST['comment'])
            comment.save()
            #image 
            listing.image = "../../" + listing.image
            return render(request, "auctions/listing_page.html",{
                "listing": listing,
                "comments": Comment.objects.all(),
                "max_bid": max_bid,
                "bid_counter": bid_counter,
            })
            
        elif 'bid' in request.POST:
            errMessage = ''
            if float(max_bid.amount) > float(request.POST['bid']):
                errMessage = "You cannot bid less than the current bid"
            else:
                bid = Bid(user=request.user, listing=listing,
                            amount=request.POST['bid'])
                bid.save()
                bid_counter += 1
                max_bid = bid
                listing.price = max_bid.amount
                listing.save()
                
            #image 
            listing.image = "../../" + listing.image
            return render(request, "auctions/listing_page.html",{
                "listing": listing,
                "comments": Comment.objects.all(),
                "max_bid": max_bid,
                "bid_counter": bid_counter,
                "error_message": errMessage
            })
    if open == 'False':
        listing.open_forbid = False
        listing.save()

    #image 
    listing.image = "../../" + listing.image
    return render(request, "auctions/listing_page.html",{
        "listing": listing,
        "comments": Comment.objects.all(),
        "max_bid": max_bid,
        "bid_counter": bid_counter,
    })

def watchlist(request):
    watchlists = Watchlist.objects.all()
    return render(request, "auctions/watchlist.html",{
        "watchlists": watchlists
    })

def category(request):
    return render(request, "auctions/category.html",{
        "categories": Category.objects.all()
    })

def addTo_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    watchlist = Watchlist(user = request.user, listing = listing)
    #check for duplication
    errMessage = ''
    old_watchlist = ''
    try:
        old_watchlist = Watchlist.objects.get(user = request.user, listing = listing)
    except:
        pass

    if not old_watchlist:
        watchlist.save()
        return HttpResponseRedirect(reverse("listing_page", 
                                    args=(listing_id, listing.open_forbid,)))
    else:
        errMessage ="Already in your watchlist"

    bids = Bid.objects.all()
    bid_counter = 0
    for bid in bids:
        if bid.listing.id == listing_id:
            bid_counter += 1
            if float(bid.amount) == float(listing.price):
                max_bid = bid
    #image 
    listing.image = "../" + listing.image
    return render(request, "auctions/listing_page.html",{
        "listing": listing,
        "comments": Comment.objects.all(),
        "max_bid": max_bid,
        "bid_counter": bid_counter,
        "watchlist_message": errMessage
    })

def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    watchlist = Watchlist.objects.get(user=request.user, listing = listing)
    watchlist.delete()

    return HttpResponseRedirect(reverse("watchlist"))

def category_list(request, category_name):
    listings = ''
    category = ''
    try:
        category = Category.objects.get(name = category_name)
        listings = Listing.objects.all()
        for listing in listings:
            listing.image = "../" + listing.image
    except:
        pass
    
    return render(request, "auctions/category_list.html",{
        "listings": listings,
        "category": category
    })

def delete_listing(request, listing_id):
    listing = Listing.objects.get(id = listing_id, owner = request.user)
    listing.delete()

    return HttpResponseRedirect(reverse("index"))   