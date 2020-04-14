from django.shortcuts import render
from django.template.loader import render_to_string 
from django.core.exceptions import PermissionDenied
from django.utils import translation
from django.conf import settings
from django.urls import reverse
from django.http import Http404,HttpResponse,HttpResponseBadRequest,HttpResponseNotFound,HttpResponseForbidden, HttpResponseRedirect
from backend.models import Event

# Create your views here.

def landingpage(request):
    e = Event.getfromsession(request)
    if e:
        return HttpResponseRedirect(reverse("event.participate"))
    else:
        return HttpResponseRedirect(reverse("event.enter"))
    return( render(request,"frontend/base.html",{} ) )

def base(request):
    return( landingpage(request) )

def rendertemplate(request,template):
    return render(request,template,{})
    
def set_language(request,lang):
    next = request.GET.get("next")
    translation.activate(lang)
    response = HttpResponseRedirect(next)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response
    
def status403(request, exception="Der Zugriff auf diese Seite ist nicht möglich."):
    print("FBD")
    tmpl = "frontend/status.html" 
    t = render_to_string(tmpl,{ "headline": "Zugriff nicht möglich", "exception": exception },request=request)
    return HttpResponse(t,status=403)
    
def status404(request, exception="Diese Seite wurde nicht gefunden."):
    tmpl = "frontend/status.html"
    t = render_to_string(tmpl,{ "headline": "Nicht gefunden", "exception": exception }, request=request)
    return HttpResponse(t,status=404)
    
def status500(request, exception="Aktuell finden Wartungsarbeiten statt. Bitte versuchen Sie es später nochmals."):
    tmpl = "frontend/status.html"
    t = render_to_string(tmpl,{ "headline": "Wartungsarbeiten", "exception": "interner Fehler" }, request=request)
    return HttpResponse(t,status=500) 
    