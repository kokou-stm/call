from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView
from .views import *

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/custom_password_reset_email.html'
    subject_template_name = 'registration/custom_password_reset_subject.txt'
    extra_email_context = {
        'custom_message': 'Nous sommes là pour vous aider.',
    }

urlpatterns = [
    path('generate_agora_token/', generate_agora_token, name='generate_agora_token'),
    path('', index, name='index'),
    # login-section
    path('login/', connection, name='login'),
    path('code/', code, name='code'),
    path('register/', register, name="register"),
    path('logout/', deconnexion, name='logout'),
    path('chat_ai/', chat_ai, name='chat_ai'),
    path('chat_view/', chat_view, name='chat_view'),
    
    path('forgotpassword/', forgotpassword, name='forgotpassword'),
    path(
        'mot-de-passe-oublie/',
        CustomPasswordResetView.as_view(),
        name='password_reset'
    ),path('mot-de-passe-oublie/envoye/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reinitialiser/complet/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

    
    



