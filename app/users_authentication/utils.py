# from app import settings 
from otp_generator.otp import generate_otp
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

# custom modules 
from .models import (
    OneTimePassword, 
    User
)

from_email = "shamim@naiyani.com"


def send_email_with_otp_to_user(email, request):
    # generate 6 digit random otp
    otp = generate_otp(length=6) 
    
    user = User.objects.get(email=email)
    current_site = get_current_site(request=request)
    
    # send email
    # from_email = settings.DEFAULT_FROM_EMAIL 
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
    print(otp)
    
   
def send_password_reset_link_to_email(data):
    '''
            email_data = {
                'to': user.email,
                'subject': f"Password reset link from {current_site_domain}!",
                'body': email_body
            }
    '''
    email = EmailMessage(
        subject=data["subject"],      
        from_email=from_email,  
        body=data["body"],
        to=[data["to"]] 
    ) 
    
    email.send(fail_silently=True)


def send_new_password_to_email(data):
    email = EmailMessage(
        to=[data["to"]], 
        from_email=from_email,
        subject=data["subject"],
        body=data["body"] 
    )
    
    email.send(fail_silently=True)