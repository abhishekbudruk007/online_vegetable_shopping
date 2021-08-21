from django.conf import settings
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from . import views
app_name = "products"
urlpatterns = [
    # path('product/<int:pk>',views.DetailViewFBV,name='product_detail_view'),
    path('product/<int:pk>',views.ProductDetailCBV.as_view(),name='product_detail_view'),
    path('wishlist/add/<int:pk>',views.AddToWishlistFBV,name='add_to_wishlist'),
    path('wishlist/',views.WishlistCBV.as_view(),name='wishlist'),
    path('wishlist/delete/<int:pk>',views.DeleteWishlistCBV.as_view(),name='remove_from_wishlist'),

    path('add_to_cart/<int:pk>',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:pk>',views.remove_from_cart,name='remove_from_cart'),
    path('reduce_quantity_item/<pk>/', views.reduce_quantity_item, name='reduce_quantity_item'),
    path('order_summary/', views.OrderSummaryView.as_view(), name='order_summary'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/<payment-option>', views.PaymentView.as_view(), name='payment')

]