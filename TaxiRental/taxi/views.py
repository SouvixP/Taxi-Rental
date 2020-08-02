from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from . models import *
from django.urls import reverse
from taxi.helper import get_user
from taxi.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from django.conf import settings
from django.core.mail import send_mail
import random
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

EMAIL_HOST_USER='adriraj.alcheringa@gmail.com'

def index(request):
    return render(request,'taxi/index.html')

def info(request):
    return render(request,'taxi/info.html')

def dashboard(request):
    return render(request,'taxi/dashboard.html')

def contact(request):
    thank = False
    if request.method == 'POST':
        name = request.POST.get('Name')
        email = request.POST.get("Email")
        message = request.POST.get("Message")
        contact = Contact(name = name,email = email,message = message)
        contact.save()
        thank = True
    return render(request, 'taxi/contact.html', {'thank': thank})

def checkout(request):
    if request.method == 'POST':
       email = request.POST.get("Email")
       phone_no = request.POST.get("Phone Number")
       destination = request.POST.get("destination")
       car_type = request.POST.get("car_type")
       order = Order(email=email, phone_no=phone_no, destination=destination, car_type=car_type)
       order.save()
    #    print('Order is done.')
       amount=order.tot_price()
       request.session['amount']=amount
       request.session['destination'] = destination
       request.session['car_type'] = car_type
       request.session['email']=email
       return HttpResponseRedirect(reverse('payment'))
    else:
        return render(request, 'taxi/checkout.html')

def payment(request):
    amount=request.session['amount']
    destination = request.session['destination']
    car_type = request.session['car_type']
    email = request.session['email']
    otp_sent = False
    
    if request.method == 'POST':
        to_list=[email, EMAIL_HOST_USER]
        otp = random.randrange(1000,9999)
        message='Your OTP for the ride is '+ str(otp)
        from_email=EMAIL_HOST_USER
        subject='OTP for ride'
        send_mail(subject,message,from_email,to_list,fail_silently=False)
        otp_sent=True
        return render(request, 'taxi/amount.html', {'otp_sent':otp_sent,'amount': amount,'destination':destination,'car_type':car_type})
    
    return render(request, 'taxi/amount.html', {'otp_sent':otp_sent,'amount': amount,'destination':destination,'car_type':car_type})

def sign_in(request):
  # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(sign_in_url)

def callback(request):
  # Get the state saved in session
  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)

  # Get the user's profile
  user = get_user(token)

  # Save token and user
  store_token(request, token)
  store_user(request, user)

  return HttpResponseRedirect(reverse('taxi/'))

def handle_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        license_no = request.POST['license_no']
        pass1 = request.POST['pass1']  
        pass2 = request.POST['pass2']

        user = User.objects.create_user(username=username, first_name=first_name,last_name=last_name,email=email,password=pass1)
        user1 = Driver.objects.create(licence_no=license_no,user=user)
        user1.save()
        messages.success(request,"Your account has been successfully created")
        return redirect('HomePage')

    else:
        return HttpResponse('404-Not Found')

def handle_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass']

        user = authenticate(username=username, password=pass1)
        if user:
            login(request,user)
        else:
            messages.success(request, 'Invalid login details!!!')
        return redirect('HomePage')
    return HttpResponse('handle_login')

@login_required
def handle_logout(request):
    logout(request)
    return redirect('HomePage')