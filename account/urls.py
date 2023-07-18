from django.urls import path
from account.views import UserChangePasswordView, UserPasswordResetView, UserRegistrationView, UserLoginView, UserprofileView, SendPasswordResetEmailView, SendVerifyEmailView, UserVerifyView



urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register' ),
    path('send-verify-email/', SendVerifyEmailView.as_view(), name='send-verify-email' ),
    path('verify-user/<uid>/<token>/', UserVerifyView.as_view(), name='verify-user' ),
    
    path('login/', UserLoginView.as_view(), name='login' ),
    path('profile/', UserprofileView.as_view(), name='profile' ),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword' ),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email' ),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password' ),


]