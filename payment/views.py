from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from sslcommerz_python.payment import SSLCSession

from login_app.models import Profile
from order.models import Order, Product, Cart
from payment.forms import Billing_form
from payment.forms import billing_address
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib import messages
# Create your views here.
import requests
from shop_app import models
from decimal import Decimal
import socket


@login_required
def checkout(request):
    saved_address = billing_address.objects.get_or_create(user=request.user)[0]
    form = Billing_form(instance= saved_address)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()

    order_total = order_qs[0].get_totals()
    if request.method == 'POST':
        form = Billing_form(request.POST,instance=saved_address)
        if form.is_valid():
            form.save()
            form = Billing_form(instance=saved_address)
            messages.success(request,f"Shipping Address saved")


    return render(request,'payment/checkout.html',context={'form':form,'order_items':order_items,'order_total':order_total,'saved_address':saved_address})


@login_required

def payment(request):
    saved_address = billing_address.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]

    if not saved_address.is_fully_filled():
        messages.info(request, f"Please complete shipping address")
        return redirect('payment:checkout')


    profile_details = Profile.objects.get_or_create(user= request.user)
    profile_details = profile_details[0]
    print(profile_details.address_1)
    if not profile_details.address_1 :
        messages.info(request,f"Please complete Profile details!")
        return redirect('login_app:profile')
    if not profile_details.phone:
        messages.info(request, f"Please complete Profile details!")
        return redirect('login_app:profile')

    store_id ='nezzo5f00ae215aa04'
    API_key = 'nezzo5f00ae215aa04@ssl'

    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
                           sslc_store_pass=API_key)
    status_url = request.build_absolute_uri(reverse('payment:complete'))

    mypayment.set_urls(success_url=status_url, fail_url=status_url,
                       cancel_url=status_url, ipn_url=status_url)

    order_qs = Order.objects.filter(user=request.user,ordered= False)
    order_item = order_qs[0].orderitems.all()
    order_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_totals()
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='mixed',
                                      product_name=order_item, num_of_item=order_count, shipping_method='Courier',
                                      product_profile='None')
    current_user = request.user
    mypayment.set_customer_info(name=current_user.user.full_name, email=current_user.email,
                                address1=current_user.user.address_1,
                                address2=current_user.user.address_1, city=current_user.user.city, postcode=current_user.user.zipcode, country=current_user.user.country,
                                phone=current_user.user.phone)

    mypayment.set_shipping_info(shipping_to=current_user.user.full_name, address=current_user.user.address_1,
                                city= current_user.user.city,
                                postcode=current_user.user.zipcode,
                                country=current_user.user.country)
    response_data = mypayment.init_payment()
    print(response_data)

    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            bank_id = payment_data['bank_tran_id']
            messages.success(request,f"Your Payment Completed Successfully! Page will be redirected!")
            return HttpResponseRedirect(reverse("payment:purchase", kwargs={'val_id':val_id, 'tran_id':tran_id,'bank_id':bank_id,}))
        elif status == 'FAILED':
            messages.warning(request, f"Your Payment Failed! Please Try Again! Page will be redirected!")

    return render(request, "payment/complete.html", context={})


@login_required
def purchase(request, val_id, tran_id,bank_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    orderId = tran_id
    order.ordered = True
    order.orderId = orderId
    order.paymentId = val_id
    order.bank_id = bank_id
    order.save()
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse("shop_app:home"))

@login_required
def order_details(request):
    pending_order = Cart.objects.filter(user=request.user,purchased =False)
    completed_order = Cart.objects.filter(user=request.user,purchased=True)
    status = Order.objects.filter(user=request.user,ordered=True)

    context={'pending_order':pending_order,'completed_order':completed_order,'status':status}
    return render(request,'payment/order.html',context)


