"""ecom_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.views import (
  PasswordResetView,
PasswordResetDoneView,
PasswordResetConfirmView,
PasswordResetCompleteView,
PasswordChangeView
)
from login_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('login_app.urls')),
    path('', include('shop_app.urls')),
    path('order/', include('order.urls')),
    path('pay/', include('payment.urls')),

    url(r'^accounts/password/change/$', PasswordChangeView.as_view(),
        {'template_name': 'registration/password_change_form.html'},
        name="password_change"),
    url(r'^accounts/password/reset/$',  PasswordResetView.as_view(),
        {'template_name': 'registration/password_reset_form.html'},
        name="password_reset"),

    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), {'template_name': 'registration/password_reset_confirm.html'},
        name="password_reset_confirm"),
    url(r'^accounts/password/reset/done/$', PasswordResetDoneView.as_view(),
        {'template_name': 'registration/password_reset_done.html'}, name="password_reset_done"),
    url(r'^accounts/password/com/$', PasswordResetCompleteView.as_view(),
        {'template_name': 'registration/password_reset_complete.html'}, name="password_reset_complete"),


]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

