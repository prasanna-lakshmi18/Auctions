from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Create_Listing",views.Create_Listing,name="Create_Listing"),
    path("All_Listings",views.All_Listings,name="All_Listings"),
    path("<int:Pr_id>/Product",views.Product,name="Product"),
    path("<int:Pr_id>/addwatchlist",views.addwatchlist,name="addwatchlist"),
    path("<int:Pr_id>/removewatchlist",views.removewatchlist,name="removewatchlist"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("<int:Pr_id>/bidd",views.bidd,name="bidd"),
    path("<int:Pr_id>/comment",views.comment,name="comment"),
    path("catee",views.catee,name="catee"),
    path("<int:Pr_id>/delete",views.delete,name="delete")
]
