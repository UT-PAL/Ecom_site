
from django.urls import path
from payment import views

app_name = 'payment'
urlpatterns = [
  path('checkout/', views.checkout,name="checkout"),
  path('pay/', views.payment,name="pay"),
  path('status/', views.complete, name="complete"),
  path('purchase/<val_id>/<tran_id>/<bank_id>/', views.purchase, name="purchase"),
  path('order/',views.order_details,name='order'),



]