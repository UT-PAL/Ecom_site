
from django.urls import path, include, reverse_lazy
from login_app import views

app_name = 'login_app'

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('change_profile/', views.user_profile, name='profile'),
    path('view_profile/',views.view_profile,name='view_profile'),
    path('others_profile/<p>',views.others_profile,name='other_profile')


]