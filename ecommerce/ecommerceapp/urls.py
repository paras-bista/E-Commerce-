from django.urls import path, include
from . import views
# from .views import profile_view


urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path ('checkout/', views.checkout, name='Checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('profile/', views.profile_view, name='profile'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('admin/send-shipment-email/<int:order_id>/', views.send_shipment_email, name='send_shipment_email'),

]
