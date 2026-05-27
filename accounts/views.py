import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from customers.models import Customer

from .models import User


def generate_code():
    return str(random.randint(100000, 999999))


def send_verification_email(user):
    code = generate_code()
    user.verification_code = code
    user.save()

    send_mail(
        subject="GBOMDIA Email Verification Code",
        message=f"Your GBOMDIA verification code is: {code}",
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_reset_email(user):
    code = generate_code()
    user.reset_code = code
    user.save()

    send_mail(
        subject="GBOMDIA Password Reset Code",
        message=f"Your GBOMDIA password reset code is: {code}",
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )


def login_page(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username_or_email", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            try:
                found_user = User.objects.get(email__iexact=username_or_email)
                user = authenticate(request, username=found_user.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None:
            messages.error(request, "Invalid login details.")
            return render(request, "accounts/login.html")

        if user.role == "customer" and not user.email_verified:
            messages.error(request, "Please verify your email before login.")
            return redirect("verify_email_page")

        login(request, user)

        if user.role in ["admin", "management", "operator"]:
            return redirect("enter_daily_cash")

        if user.role == "admin":
            return redirect("admin_dashboard")
        if user.role == "management":
            return redirect("management_dashboard")
        if user.role == "operator":
            return redirect("operator_dashboard")
        if user.role == "customer":
            return redirect("customer_dashboard")

        return redirect("home")

    return render(request, "accounts/login.html")


def signup_page(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone = request.POST.get("phone", "").strip()
        password1 = request.POST.get("password1", "").strip()
        password2 = request.POST.get("password2", "").strip()

        if not full_name or not email or not phone or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return render(request, "accounts/signup.html")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "accounts/signup.html")

        if Customer.objects.filter(phone=phone).exists():
            messages.error(request, "A customer profile with this phone already exists.")
            return render(request, "accounts/signup.html")

        username_base = email.split("@")[0]
        username = username_base
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{username_base}{counter}"
            counter += 1

        name_parts = full_name.split()
        first_name = name_parts[0] if name_parts else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role="customer",
            email_verified=False,
        )

        Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            is_active=True,
        )

        send_verification_email(user)

        request.session["pending_verification_email"] = email

        messages.success(
            request,
            "Account created successfully. A verification code has been sent to your email."
        )

        return redirect("verify_email_page")

    return render(request, "accounts/signup.html")


def verify_email_page(request):
    email = request.session.get("pending_verification_email")

    if not email:
        messages.error(request, "No email verification session found.")
        return redirect("signup_page")

    if request.method == "POST":
        code = request.POST.get("code", "").strip()

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            messages.error(request, "Account not found.")
            return redirect("signup_page")

        if user.verification_code == code:
            user.email_verified = True
            user.verification_code = ""
            user.save()

            messages.success(request, "Email verified successfully. You can now log in.")
            return redirect("login_page")

        messages.error(request, "Invalid verification code.")

    return render(request, "accounts/verify_email.html", {"email": email})


def resend_verification_code(request):
    email = request.session.get("pending_verification_email")

    if not email:
        messages.error(request, "No email verification session found.")
        return redirect("signup_page")

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        messages.error(request, "Account not found.")
        return redirect("signup_page")

    send_verification_email(user)

    messages.success(request, "A new verification code has been sent.")
    return redirect("verify_email_page")


def forgot_password_page(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return render(request, "accounts/forgot_password.html")

        send_reset_email(user)
        request.session["password_reset_email"] = email

        messages.success(request, "A password reset code has been sent to your email.")
        return redirect("reset_password_page")

    return render(request, "accounts/forgot_password.html")


def reset_password_page(request):
    email = request.session.get("password_reset_email")

    if not email:
        messages.error(request, "No password reset session found.")
        return redirect("forgot_password_page")

    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        password1 = request.POST.get("password1", "").strip()
        password2 = request.POST.get("password2", "").strip()

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/reset_password.html", {"email": email})

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            messages.error(request, "Account not found.")
            return redirect("forgot_password_page")

        if user.reset_code != code:
            messages.error(request, "Invalid reset code.")
            return render(request, "accounts/reset_password.html", {"email": email})

        user.set_password(password1)
        user.reset_code = ""
        user.save()

        if "password_reset_email" in request.session:
            del request.session["password_reset_email"]

        messages.success(request, "Password reset successfully. You can now log in.")
        return redirect("login_page")

    return render(request, "accounts/reset_password.html", {"email": email})


def logout_page(request):
    logout(request)
    return redirect("home")