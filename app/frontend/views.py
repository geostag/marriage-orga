from django.shortcuts import render
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
    
