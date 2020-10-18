from django.contrib import admin

# Register your models here.
from shop_app.models import Category,Product,Reviews,review_or_not
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Reviews)
admin.site.register(review_or_not)