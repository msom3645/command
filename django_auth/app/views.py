from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from auth1 import settings
from .tokens import generate_token
from threading import Thread, Timer


def home(request):
    
    return render(request, 'app/index.html')


#REGISTRATION --------------------------------------------------------

class EmailThread(Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        Thread.__init__(self)

    def run(self):
        self.email_message.send()



def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, 'User already exists')
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, 'Email already exists')
            return redirect('signup')

        if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters')
        if pass1 != pass2:
            messages.error(request, 'Passwords did`t match')
        if not username.isalnum():
            messages.error(request, 'Username must be Alpha-Numeric')
            return redirect('signup' )

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        #EMAIL
        current_site = get_current_site(request)
        email_subject = 'Confirm Your Email'
        msg = render_to_string('app/email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })

        email_msg = EmailMessage(
            email_subject, 
            msg,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )

        EmailThread(email_msg).start()

        # REMOVE FROM DB NOT ACTIVATED USERS
        def delInactive():
            user = User.objects.filter(email=email).first()
            if not user.is_active:
                user.delete()
        t = Timer(35, delInactive)
        t.start()
        
    return render(request,'app/signup.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist ):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'app/activation_failed.html')

# LOGIN ------------------------------------
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user =  authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request,'app/index.html', {'fname':fname})
        else:
            messages.error(request, 'Bad Credentials')
            return redirect('home')
    return render(request,'app/signin.html')

def signout(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully!')
    return redirect('home')




def test1(request, uidb64, token, xx):
    
    user = User.objects.filter(email = 'q@q.ru').first()
    def delInactiva():
        if not user.is_active():
            user.delete()
    t = Timer(25, delInactive)
    t.start()
    

    return render(request, 'app/test1.html')