
from django.urls import path
from order import views
app_name = 'order'
urlpatterns = [
    path('add/<pk>/', views.add_cart, name='add_cart'),
    path('remove/<pk>', views.removefromcart, name='remove'),
    path('increase/<pk>',views.increase_cart,name='increase'),
    path('decrease/<pk>',views.decrease_cart,name='decrease'),
    path('cart/',views.Cart_view,name='cart'),

   ]
