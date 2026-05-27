from django.urls import path

from .views import (
    forgot_password_page,
    login_page,
    logout_page,
    resend_verification_code,
    reset_password_page,
    signup_page,
    verify_email_page,
)


urlpatterns = [
    path("login/", login_page, name="login_page"),
    path("signup/", signup_page, name="signup_page"),
    path("verify-email/", verify_email_page, name="verify_email_page"),
    path("resend-verification/", resend_verification_code, name="resend_verification_code"),
    path("forgot-password/", forgot_password_page, name="forgot_password_page"),
    path("reset-password/", reset_password_page, name="reset_password_page"),
    path("logout/", logout_page, name="logout_page"),
]