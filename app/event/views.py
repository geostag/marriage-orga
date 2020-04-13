from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import Http404,HttpResponse,HttpResponseBadRequest,HttpResponseNotFound,HttpResponseForbidden, HttpResponseRedirect
from event.forms import EnterForm, EnterWithCodeForm
from backend.models import Event, Participant

# Create your views here.

def leave(request):
    request.session.pop("eid")
    request.session.pop("pid")
    return HttpResponseRedirect(reverse("landingpage"))

def enter(request,shortcut=None):
    if shortcut:
        event = Event.objects.get(namecode=shortcut)
    else:
        event = None
    form = EnterForm()
    formC = EnterWithCodeForm()
    if request.POST:
        if request.POST.get("partcode"):
            # enter with partcode
            formC = EnterWithCodeForm(request.POST)
            if formC.is_valid():
                try:
                    p = Participant.objects.get(subcode = formC.cleaned_data['partcode'])
                    e = p.event
                    request.session["pid"] = p.id
                    request.session["eid"] = e.id
                    return HttpResponseRedirect(reverse("event.participate"))
                except:
                    formC.add_error(None,"Anmeldung fehlgeschlagen")
        else:
            # enter with event + password
            form = EnterForm(request.POST)
            if form.is_valid():
                if not event:
                    event = Event.objects.get(namecode=form.cleaned_data['shortcut'])
                if event and event.password == form.cleaned_data['password']:
                    request.session["eid"] = event.id
                    return HttpResponseRedirect(reverse("event.participate"))
                else:
                    form.add_error(None,"Anmeldung fehlgeschlagen")
                    
    c = {"formC": formC, "form": form, "event": event }
    return render(request,"event/enter.html" ,c)
    
def participate(request):
    e = Event.getfromsession(request)
    if not e:
        raise Http404
    p = Participant.getfromsession(request)
    if not p:
        # autogenerate a participant
        p = Participant(event=e)
        p.save()
        request.session["pid"] = p.id
        return render(request,"event/my-code.html" ,{ "code": p.subcode })
        
    guests = Participant.objects.filter(subcode = p.subcode)
    c = { "guests": guests }
    return render(request,"event/participate.html" ,c)

def participant_set(request):
    e = Event.getfromsession(request)
    p = Participant.getfromsession(request)
    if not e or not p:
        return HttpResponseForbidden("event or participant not set")
        
    g = Participant.objects.get(id = request.POST.get("gid"))
    n = request.POST.get("name")
    v = request.POST.get("value")
    if n == "name":
        g.name = v
    elif n == "email":
        g.email = v
    elif n == "phone":
        g.phone = v
    elif n == "participation":
        g.participation = v
    else:
        return HttpResponseBadRequest("name not given '%s'" % n)
        
    g.save()
    return HttpResponse("saved")
    
def participant_add(request):
    e = Event.getfromsession(request)
    p = Participant.getfromsession(request)
    if not e or not p:
        return HttpResponseForbidden("event or participant not set")
    g = Participant(event=e,subcode=p.subcode)
    g.save()
    return HttpResponseRedirect(reverse("event.participate"))

def participant_remove(request,gid):
    e = Event.getfromsession(request)
    p = Participant.getfromsession(request)
    if not e or not p:
        return HttpResponseForbidden("event or participant not set")
    g = Participant.objects.get(id = int(gid))
    g.delete()
    return HttpResponseRedirect(reverse("event.participate"))