from django.shortcuts import render
from django.conf import settings

# Create your views here.

def landingpage(request):
    return( render(request,"frontend/base.html",{} ) )

def base(request):
    return( landingpage(request) )

def rendertemplate(request,template):
    return render(request,template,{})
    
