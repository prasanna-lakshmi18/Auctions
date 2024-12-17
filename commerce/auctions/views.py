from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.db.models import Min
from django.contrib import messages
from .models import User,Listing,bid,Comments,Product_name


def index(request):
    #Lands to an index page with all the active listings/items(if user is authenticated).
    try:
        cate=set(Listing.objects.values_list('Pr_category', flat=True).distinct())
        nam=User.objects.get(id=request.user.id)
        return render(request,"auctions/index.html",{
                "list":Listing.objects.all(),
                "ca":cate,
                "name":nam
            })
    except 	User.DoesNotExist:
        #Redirects to register page if not authenticated or allows you to log-in.
        return HttpResponseRedirect(reverse("register"))
    


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

#Adds a new item.
def Create_Listing(request):
    if request.method=="GET":
        #Directs to the page to add a new item.
        return render(request,"auctions/Create_User.html")
    else:
        #Gets the details about the item to be added
        #name of the listing
        nam=request.POST["name"]

        #Description about the listing.
        description=request.POST["Description"]

        #Category of the listing.
        category=request.POST["Category"]

        #The opening bid price of the listing
        price=request.POST["Price"]

        #The active status of the listing(Default=True).
        status=request.POST["status"]

        #Image url of the listing.
        img=request.POST["img_url"]

        #Name of the owner of the listing.
        User_name=User.objects.get(id=request.user.id)
        def_watchlist=False
        Listing_name=Product_name(
            name=nam,
            User=User_name
        )
        Listing_name.save()

        #updates the bid price
        bidd=bid(
            User=User_name,
            bids=price,
            P_name=Listing_name
        )
        bidd.save()

        #updates listing/items details.
        listings=Listing(
            Pr_name=Listing_name,
            Pr_description=description,
            Pr_category=category.capitalize(),
            Pr_status=status,
            Pr_price=bidd,
            user_List=User_name,
            Pr_image=img,
        )
        listings.save()
        
        #redirects to index page with the just added listing and all other active listings.
        return HttpResponseRedirect(reverse("index"))
    
def All_Listings(request):
    #All the listing that are added so far (Both active and inactive).
    return render(request,"auctions/All_listings.html",{
            "list":Listing.objects.all(),
            "name":User.objects.get(id=request.user.id)
        })
def Product(request,Pr_id):
    #Presents all the details of the product,if the user is authenticated.
    try:
        #Details about the listing of specific id.
        details=Listing.objects.get(id=Pr_id)

        listing_watchist=request.user in details.Pr_watchlist.all()

        #comments made so far on the listings.
        comm=Comments.objects.all()
        names=User.objects.get(id=request.user.id)
        #To get the first bid placed on the listing.
        bidders=bid.objects.filter(P_name=details.Pr_name).annotate(Min('bids'))
        min_bid = bidders.values('bids__min')[0]['bids__min']        
        return render(request,"auctions/Product.html",{
            "list":details,
            "co":comm,
            "names":names,
            "min_bid":min_bid,
            "msg":"The auction is closed",
            "watch_l":listing_watchist
        })
    #Sign-in if not authenticate or login otherwise.
    except 	User.DoesNotExist:
        return HttpResponseRedirect(reverse("register"))


def removewatchlist(request,Pr_id):
    details=Listing.objects.get(id=Pr_id)
    Users=request.user
    #Attempts to update the watchlist status of the listing  to False .
    
    details.Pr_watchlist.remove(Users)
    return redirect('Product', Pr_id=Pr_id)
    
def addwatchlist(request,Pr_id):
    #Attempts to update the watchlist status of the listing  to True from Product page.

    details=Listing.objects.get(id=Pr_id)
    Users=request.user
    details.Pr_watchlist.add(Users)
    return redirect('Product', Pr_id=Pr_id)

def watchlist(request):
    #Renders all the item that are added to the watchlist.
    Users=request.user
    #watchlist_Products=Listing.objects.filter(Pr_watchlist=User)
    watchlist_Products=Users.Product_watchlist.all()
    return render(request,"auctions/watchlist.html",{
        "Products":watchlist_Products,
        "names":User.objects.get(id=request.user.id),
        "msg":"The auction is closed!"
    })


def bidd(request,Pr_id):
    #Attempts to update the bid value.
    details=Listing.objects.get(pk=Pr_id)
    bidddd=request.POST["bid"]
    bi = bid.objects.filter(id=Pr_id)
    L_name=Product_name.objects.get(pk=Pr_id)
    #To get the first bid placed on the listing.
    bidders=bid.objects.filter(P_name=details.Pr_name).annotate(Min('bids'))
    min_bid = bidders.values('bids__min')[0]['bids__min']
    if int(bidddd) > details.Pr_price.bids:
        #updates the bid price if greater.
        New_bid=bid(  
            bids=bidddd,
            P_name=L_name,
            User=User.objects.get(id=request.user.id)
        )
        New_bid.save()
        details.Pr_price=New_bid
        details.save()
        comm=Comments.objects.all()
        return render(request,"auctions/Product.html",{
            "list":details,
            "co":comm,
            "names":User.objects.get(id=request.user.id),
            "msg":"The auction is closed",
            "min_bid":min_bid,
            "mesg":"Bid is updated!!"#Message if the bid is updated.
        })
    else:
        comm=Comments.objects.all()
        bidders=bid.objects.filter(P_name=details.Pr_name).annotate(Min('bids'))
        min_bid = bidders.values('bids__min')[0]['bids__min']
        return render(request,"auctions/Product.html",{
            "list":details,
            "message":"Please enter a greater bid value than the exisings one!",#Message if the attempted bid value is not greater than the existing one.
            "co":comm,
            "min_bid":min_bid,
            "names":User.objects.get(id=request.user.id),
        })
        return redirect('Product', Pr_id=Pr_id)

def comment(request, Pr_id):
    # Get comment from POST request
    comment = request.POST.get("comm", "").strip()
    
    # Check if comment is empty
    if not comment:
        # Use Django messages framework
        messages.error(request, "Comment cannot be empty")
        return redirect('Product', Pr_id=Pr_id)
    
    # Proceed with comment creation
    details = Listing.objects.get(id=Pr_id)
    cm = Comments(
        Pr_comment=comment,
        Comment_User=request.user,
        Commenter=details
    )
    cm.save()
    
    # Success message
    messages.success(request, "Comment added successfully!")
    return redirect('Product', Pr_id=Pr_id)

def catee(request):
    #Attempts to return all the items with the reqd. category.
    cate_name=request.POST["te"]
    name=User.objects.get(id=request.user.id)
    return render(request,"auctions/category.html",{
        "Products":Listing.objects.all(),
        "ac":cate_name,
        "names":User.objects.get(id=request.user.id),
        "msg":"The auction is closed."
    })

def delete(request,Pr_id):
    #Allow the owner of the listing/item to delete.
    ite=request.POST["dele"]
    del_prod=Listing.objects.filter(id=Pr_id).update(Pr_status=ite)
    details=Listing.objects.get(id=Pr_id)
    bidders=bid.objects.filter(P_name=details.Pr_name).annotate(Min('bids'))
    min_bid = bidders.values('bids__min')[0]['bids__min']        

    return redirect('Product', Pr_id=Pr_id)