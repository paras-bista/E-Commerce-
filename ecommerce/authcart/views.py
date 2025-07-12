from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .utils import account_activation_token
import logging

logger = logging.getLogger(__name__)

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass1']
        conform_password = request.POST['pass2']
        
        if password != conform_password:
            messages.warning(request, "Password doesn't match")
            return render(request, 'signup.html')
        
        try:
            if User.objects.get(email=email):
                messages.error(request, "Email already exists")
                return render(request, 'signup.html')
        except User.DoesNotExist:
            try:
                # Create inactive user
                user = User.objects.create_user(email, email, password)
                user.is_active = False  # User must verify email to activate account
                user.save()
                
                # Generate activation email
                current_site = get_current_site(request)
                mail_subject = 'Activate your E-commerce Account'
                message = render_to_string('activate_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                
                try:
                    # Send activation email
                    send_mail(
                        subject=mail_subject,
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email],
                        fail_silently=False,
                        html_message=message
                    )
                    messages.success(request, 'Please check your email to activate your account. You must activate your account before logging in.')
                    return redirect('login')
                except Exception as e:
                    logger.error(f"Failed to send activation email: {str(e)}")
                    user.delete()  # Delete user if email fails
                    messages.error(request, "Failed to send activation email. Please try again.")
                    return render(request, 'signup.html')
                    
            except Exception as e:
                logger.error(f"Error in signup process: {str(e)}")
                messages.error(request, "An error occurred during signup. Please try again.")
                return render(request, 'signup.html')
    
    return render(request, 'signup.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for confirming your email. Your account is now active and you can login.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or has expired!')
        return redirect('login')

def handlelogin(request):
    if request.method == "POST":
       username = request.POST['email'] 
       password = request.POST['password'] 
       myuser = authenticate(username=username, password=password)

       if myuser is not None:
           login(request, myuser)
           messages.success(request, "You have successfully logged in.")
           return redirect('/')
       else:
           messages.error(request, "Invalid email or password")
           return redirect('/auth/login')

    
    return render(request, 'login.html')

def handlelogout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('/auth/login')
