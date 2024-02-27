# from app import settings 
from otp_generator.otp import generate_otp
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

# custom modules 
from .models import (
    OneTimePassword, 
)



def send_email_with_otp_to_user(email, request):
    # generate 6 digit random otp
    otp = generate_otp(length=6) 
    
    user = user.objects.get(email=email)
    current_site = get_current_site(request=request)
    
    # send email
    # from_email = settings.DEFAULT_FROM_EMAIL
    from_email = "shamim@naiyani.com" 
    subject = "Important: Account Verification!"
    body = f"Hi {user.first_name}! Welcome to {current_site}! Please verify your account with the\n one time passcode(OTP).\nYour OTP is {otp}"
    email_message = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[user.email]
    )
    
    # send
    email_message.send(fail_silently=True)
    # save the otp token in the database for further varification 
    OneTimePassword.objects.create(user=user, code=otp)
    
    