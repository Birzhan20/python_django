from django.urls import path, include

from rest_framework.routers import DefaultRouter
from django.views.decorators.cache import cache_page

from .views import (
    ShopIndexView,
    GroupListView,
    OrdersListView,
    OrderCreateView,
    ProductDetailView,
    ProductsListView,
    OrdersDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderUpdateView,
    OrderDeleteView,
    ProductsDataExportView,
    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed,
    UserOrdersListView,
    export_user_orders
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)

urlpatterns = [
    # path("", cache_page(60*3)(ShopIndexView.as_view()), name="index"),
    path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    path('api/', include(routers.urls)),
    path("groups/", GroupListView.as_view(), name="groups_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/export/", ProductsDataExportView.as_view(), name="products-export"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrdersDetailView.as_view(), name="order_details"),
    path("orders/create/", OrderCreateView.as_view(), name="orders_create"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path('products/latest/feed/', LatestProductsFeed(), name='products-feed'),

    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user-orders'),
    path('users/<int:user_id>/orders/export/', export_user_orders, name='user-orders-export'),
]
