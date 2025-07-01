from django.urls import include, path

urlpatterns = [
    path("products/", include('products.api.urls')),
    path("orders/", include('orders.api.urls')),
    path("users/", include('users.api.urls')),

]
