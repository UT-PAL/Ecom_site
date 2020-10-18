
from django.urls import path
from shop_app import views
from .views import SearchResultsView
app_name = 'shop_app'
urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('product/<pk>/', views.product_detail.as_view(), name='product_detail'),
    path('review/<pk>/', views.review_details, name='review_detail'),
    path('reviewed/<pk>/', views.review_now, name='reviewed_product'),
    path('not_reviewed/<pk>/', views.not_review, name='not_review'),
    path('search/',views.search,name='search'),
    path('search_result/',SearchResultsView.as_view(),name='search_result')
    ]
