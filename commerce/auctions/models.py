from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Table to store the name of the listing items.


class Product_name(models.Model):
    #User who placed the item.
    User=models.ForeignKey(User,on_delete=models.CASCADE,related_name="us_name")

    #Listing_name
    name=models.CharField(max_length=64)
    def __str__(self) -> str:
        return f"{self.name}"

#Table to store the values of the bids.

class bid(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_bid")#User who placed the bid.
    bids=models.IntegerField(default=0)#Bid value
    P_name=models.ForeignKey(Product_name,on_delete=models.CASCADE,related_name="Prod_name",null=True)#Item_name on which bid is placed
    def __str__(self):
        return f'{self.bids} {self.P_name} {self.User}'
        
#Table to store the information about the listing/items.

class Listing(models.Model):
    #Authorized user.
    user_List=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_name")
    #Listing name.
    Pr_name=models.ForeignKey(Product_name,on_delete=models.CASCADE,related_name="Produc_name")
    #Descrpiption of the listing.
    Pr_description=models.CharField(max_length=64)
    #Category of the listing.
    Pr_category=models.CharField(max_length=64)
    #Starting Price of the bid
    Pr_price=models.ForeignKey(bid,on_delete=models.CASCADE,related_name="bidprice",)
    #Item activity status(live/Deleted).
    Pr_status=models.BooleanField()
    #Listing image address
    Pr_image=models.CharField(max_length=1000,null=True)
    #Watchlist status
    Pr_watchlist=models.ManyToManyField(User,blank=True,null=True,related_name="Product_watchlist")

    def __str__(self):
        return f'{self.Pr_name}'

#Table to store the comments made by authorized users with respect to the listing name.

class Comments(models.Model):
    #Comment
    Pr_comment=models.CharField(max_length=400)
    #User_name / Authorized user
    Comment_User=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comm_user")
    #Listing_name
    Commenter=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="commmm",null=True)

    def __str__(self):
        
        return f'{self.Comment_User}  commented on {self.Commenter}'