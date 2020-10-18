from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView,DetailView

from shop_app.forms import ReviewForm,search
from shop_app.models import Product,Reviews,review_or_not
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
class home(ListView):
    model = Product
    template_name = 'shop_app/home.html'

class product_detail( LoginRequiredMixin ,DetailView):
    model = Product
    template_name = 'shop_app/product_detail.html'

class SearchResultsView(ListView):
    model = Product
    template_name = 'shop_app/search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')

        return Product.objects.filter(
            Q(name__icontains=query)| Q(name__icontains=query)
        )



@login_required
def review_details(request,pk):
    product = Product.objects.get(pk=pk)
    review_form = ReviewForm()
    already_reviewed = Reviews.objects.filter(product=product, user=request.user)
    review = review_or_not.objects.filter(product=product)
    if already_reviewed:
        reviewed = True
    else:
        reviewed = False
    if request.method == 'POST':
        review_form= ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return HttpResponseRedirect(reverse('shop_app:review_detail', kwargs={'pk': pk}))
    return render(request, 'shop_app/review.html',context={'review':review,'product': product, 'review_form': review_form, 'reviewed': reviewed, })



@login_required
def review_now(request, pk):
    product = Product.objects.get(pk=pk)
    user = request.user
    already_reviewed = review_or_not.objects.filter(product=product, user=user)
    if not already_reviewed:
        reviewed_post = review_or_not(product=product, user=user)
        reviewed_post.save()
    return HttpResponseRedirect(reverse('shop_app:review_details', kwargs={'pk':product.pk}))

@login_required
def not_review(request, pk):
    product = Product.objects.get(pk=pk)
    user = request.user
    already_reviewed= review_or_not.objects.filter(product=product, user=user)
    already_reviewed.delete()
    return HttpResponseRedirect(reverse('shop_app:review_details', kwargs={'pk':product.pk}))

