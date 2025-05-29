from django.urls import path
from .views import wishlist_view, wishlist_add_view_json, wishlist_del_view_json, wishlist_view_json, wishlist_remove_view

app_name = 'app_wishlist'

urlpatterns = [
    path('', wishlist_view, name="wishlist_view"),
    path('api/', wishlist_view_json),
    path('api/add/<str:id_product>', wishlist_add_view_json, name="add_now"),
    path('api/del/<str:id_product>', wishlist_del_view_json,),
    path('/del/<str:id_product>', wishlist_remove_view, name="del_now"),
]