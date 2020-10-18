from django.conf.urls import url
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, resolve_url

from django.urls import reverse

# authentication

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# forms and models


from login_app.forms import SignupForm, ProfileForm

# Create your views here.
from login_app.models import Profile, User
from shop_app.models import Reviews


def sign_up(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully !")
            return HttpResponseRedirect(reverse('login_app:login'))
    return render(request, 'login_app/sign_up.html', context={'form': form})


def user_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
            return HttpResponseRedirect(reverse('shop_app:home'))

    return render(request, 'login_app/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, "You are logged out !")
    return HttpResponseRedirect(reverse('shop_app:home'))


@login_required
def user_profile(request):
    form = ProfileForm()
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Change Saved!!")
            form = ProfileForm(instance=profile)
        return HttpResponseRedirect(reverse('login_app:view_profile'))

    return render(request, 'login_app/change_profile.html', context={'form': form})

@login_required
def view_profile(request):
    return render(request, 'login_app/profile.html')
@login_required
def others_profile(request,p):
    profile = Profile.objects.get(user=p)
    print(profile)
    return render(request, 'login_app/others_profile.html',context={'profile':profile})




