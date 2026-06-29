from django.urls import path
from . import views as pv


urlpatterns = [
    path("all-product/", pv.allProductView, name="all-product"),
    path("single-product/<int:id>/", pv.singleProduct, name="single-product"),
    path("add-product/", pv.addProduct, name="add-product"),
    path('delete-product/<int:id>/', pv.deleteProduct, name='delete-product'),
    path('edit-product/<int:id>/', pv.editProduct, name='edit-product')
]
