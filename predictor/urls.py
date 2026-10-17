# Project Title: LaptopPilot
# Subject: Software Testing and Quality Assurance
# Team Members:
# USN1: 4NI23IS252
# Name1: Dayanand Shivananda Sagar
# USN2: 4NI23IS253
# Name2: Chandan Shridhar Hegde
# USN3: 4NI24IS408
# Name3: Harsha S
# USN4: 4NI24IS412
# Name4: Mohammad Masood Hassan HA
# Date of code writing: 14-09-2026 to 25-09-2026

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict-price/', views.predict_price, name='predict_price'),
    path('patterns/', views.patterns, name='patterns'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-email/<uidb64>/<token>/', views.verify_email_view, name='verify_email'),
    path('resend-verification/', views.resend_verification_view, name='resend_verification'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_view, name='reset_password'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
