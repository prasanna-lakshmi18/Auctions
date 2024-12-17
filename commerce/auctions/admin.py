from django.contrib import admin
from .models import User,Listing,bid,Comments,Product_name
# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(bid)
admin.site.register(Comments)
admin.site.register(Product_name)
