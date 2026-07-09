from django.urls import path
from . import views as vw

urlpatterns = [
    path('get-cart/', vw.getCartView, name='get-cart'),
    path('add-to-cart/<int:product_id>/', vw.addToCart, name="add-to-cart"),
    path('remove-item/<int:product_id>/', vw.removeItem, name='remove-item')
]
