
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name = 'home-request'),
    path('register/', views.register_view, name = 'register-request'),
    path('login/', views.login_view, name = 'login-request'),
    path('logout/', views.logout_view, name = 'logout-request'),
    path('otpverify/', views.otpVerify_view, name = 'otpverify-request'),

    path('addbank/', views.addBank_view, name = 'addbank-request'),
    path('uploadtransactions/', views.uploadTransactions_view, name = 'uploadtransactions-request'),
    
]