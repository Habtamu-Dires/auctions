from django.urls import path
from .models import Listing

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing_page/<int:listing_id>/<str:open>", views.listing_page, name="listing_page"),
    path("watchlist",views.watchlist, name="watchlist"),
    path("category", views.category, name="category"),
    path("addTo_watchlist/<int:listing_id>", views.addTo_watchlist, name="addTo_watchlist"),
    path("catagory_list/<str:category_name>", views.category_list,name="category_list"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("delete_listing/<int:listing_id>", views.delete_listing, name="delete_listing")
    
]
