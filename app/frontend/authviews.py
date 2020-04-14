from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.utils import timezone
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User,Permission
from django.contrib.auth.decorators import permission_required, login_required
from django.http import Http404,HttpResponse,HttpResponseBadRequest,HttpResponseNotFound,HttpResponseForbidden, HttpResponseRedirect
from frontend.forms import LoginForm, RegisterForm, PasswordResetForm, PasswordChangeForm
from frontend.models import Doubleoptinlog
import random,urllib,string,datetime

def register(request):
    form = None
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            u = User(
                first_name = form.cleaned_data["first_name"],
                last_name = form.cleaned_data["last_name"],
                email = form.cleaned_data["email"],
                username = form.cleaned_data["email"].lower()
            )
            try:
                u.is_active = False
                u.set_password(form.cleaned_data["password"])
                u.save()
            except:
                form.add_error(None,_("Ein User mit dieser Email Adresse existiert bereits."))
            if u.id:
                do = Doubleoptinlog(user=u)
                do.save()
                mailbody = render_to_string("frontend/register-opt2-email.html",{"user":u,"oikey":do.oikey}, request=request)
                if settings.EMAIL_HOST:
                    send_mail("Schließen Sie ihre %s Registrierung ab" % settings.APP_NAME,
                        "Registrierung abschließen: %s%s" % (settings.BASE_ADDRESS,reverse('register_opt2',kwargs={"oikey":do.oikey})),
                        settings.OUR_EMAIL, 
                        [u.email],
                        html_message = mailbody
                    )
                else:
                    print("No EMAIL_HOST configured. Would send out this email: " + mailbody)
                    print("auto opt in: %s" % do.oikey)
                    #return register_opt2(request,do.oikey)
                    
                return render(request,"frontend/register_opt1.html", {} )
                
    else:
        form = RegisterForm()
    c = {"form": LoginForm(), "register": form, "registermode": True }
    return render(request,"frontend/login.html", c )

def register_opt2(request,oikey):
    try:
        do2 = Doubleoptinlog.objects.get(oikey=oikey)
    except:
        raise Http404
    do2.opt2 = timezone.now()
    do2.save()
    u = do2.user
    u.is_active = True
    u.save()
    auth.login(request,u)
    return HttpResponseRedirect(reverse("base"))
    
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("login"))
    
def login(request):
    
    if request.POST.get('next'):
        next = request.POST.get('next')
    else:
        next = request.GET.get('next')
    if not next:
        next = reverse("base")

    form = None
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']#.lower()
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request,user)
                    n = urllib.parse.urlencode({"next": next})
                    return HttpResponseRedirect( next )
                else:
                    form.add_error(None,"Ihr Account ist nicht aktiviert")
            else:
                form.add_error(None,"Anmeldung fehlgeschlagen")
    else:
        form = LoginForm()
    c = {"form": form, "register": RegisterForm(), "next": next, "registermode": False }
    return render(request,"frontend/login.html" ,c)
    

@login_required
def change_password(request):
    if request.POST:
        f = PasswordChangeForm(request.POST)
        if f.is_valid():
            c = Customer.get_object_fromsession(request)
            p = f.cleaned_data['password']
            u = request.user
            u.set_password(p)
            u.save()
            # preserve login status and customer selection
            auth.login(request,u)
            if c: 
                c.store2session(request)
                return HttpResponseRedirect(reverse("frontend.views.base"))
            else:
                return HttpResponseRedirect( reverse("select_customer") )
    else:
        f = PasswordChangeForm()
    c = {"form": f}
    return render(request,"frontend/password_change.html",c)

def reset_password(request):
    if request.POST:
        f = PasswordResetForm(request.POST)
        if f.is_valid():
            e = f.cleaned_data['email']
            user = User.objects.get(email=e)
            if user:
                user.set_password(None)
                user.is_active = False
                user.save()
                up = Uprofile.objects.get(user=user)
                do = Doubleoptinlog(uprofile=up)
                do.save()
                mailbody = render_to_string("frontend/password_reset-email.html",{"uprofile":up,"oikey":do.oikey}, request=request)
                if settings.EMAIL_HOST:
                    send_mail("%s passwort zurückgesetzt" % settings.APP_NAME,
                        "Ihr Passwort wurde zurückgesetzt. Bitte gehen Sie auf %s%s und ändern Sie Ihr Passwort." % (settings.BASE_ADDRESS,reverse('reset_password_step2',kwargs={"oikey":do.oikey})),
                        settings.OUR_EMAIL, 
                        [u.email],
                        html_message = mailbody
                    )
                else:
                    print("No EMAIL_HOST configured. Would send out this email: " + mailbody)
                    print("auto opt in: %s" % do.oikey)
                return render(request,"frontend/password_reset_step2.html")
            else:
                f.non_field_errors = "E-Mail Adresse nicht gefunden."
    else:
        f = PasswordResetForm()
        
    c = {"form": f}
    return render(request,"frontend/password_reset.html",c)
    
def reset_password_step2(request,oikey):
    try:
        do2 = Doubleoptinlog.objects.get(oikey=oikey)
    except:
        raise Http404
    do2.opt2 = timezone.now()
    do2.save()
    u = do2.uprofile.user
    u.is_active = True
    u.save()
    auth.login(request,u)
    return HttpResponseRedirect(reverse("change_password"))    
    
