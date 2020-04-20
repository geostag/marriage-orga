from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import Http404,HttpResponse,HttpResponseBadRequest,HttpResponseNotFound,HttpResponseForbidden, HttpResponseRedirect
from event.forms import EnterForm, EnterWithCodeForm
from backend.models import Event, Participant, Contribution, Ci

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
                    p = Participant.objects.filter(subcode = formC.cleaned_data['partcode']).order_by("id")[0]
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
                    # try: partcode????
                    try:
                        p = Participant.objects.filter(subcode = form.cleaned_data['password']).order_by("id")[0]
                        if p.event == event:
                            request.session["pid"] = p.id
                            request.session["eid"] = event.id
                            return HttpResponseRedirect(reverse("event.participate"))
                    except:
                        pass
                    form.add_error(None,"Anmeldung fehlgeschlagen")
                    
    c = {"formC": formC, "form": form, "event": event }
    return render(request,"event/enter.html" ,c)
    
def participate(request):
    e = Event.getfromsession(request)
    if not e:
        return HttpResponseRedirect( reverse("event.enter") )
    p = Participant.getfromsession(request)
    if not p:
        # autogenerate a participant
        p = Participant(event=e)
        p.save()
        request.session["pid"] = p.id
        return render(request,"event/my-code.html" ,{ "code": p.subcode })
        
    guests = Participant.objects.filter(subcode = p.subcode)
    
    cis = []
    for c in e.contribution_set.all():
        try:
            ci = c.ci_set.get(subcode = p.subcode)
        except:
            ci = Ci(contribution=c,subcode=p.subcode)
            ci.save()
        cis.append(ci)
    c = { "guests": guests, "cis": cis }
    return render(request,"event/participate.html" ,c)

def participant_set(request):
    e = Event.getfromsession(request)
    p = Participant.getfromsession(request)
    if not e or not p:
        raise PermissionDenied("Event nicht gefunden")
        
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
        raise PermissionDenied("Event nicht gefunden")
    g = Participant(event=e,subcode=p.subcode)
    g.save()
    return HttpResponseRedirect(reverse("event.participate"))

def participant_remove(request,gid):
    e = Event.getfromsession(request)
    p = Participant.getfromsession(request)
    if not e or not p:
        raise PermissionDenied("Event nicht gefunden")
    g = Participant.objects.get(id = int(gid))
    g.delete()
    return HttpResponseRedirect(reverse("event.participate"))
    

def ci_set(request):
    e = Event.getfromsession(request)
    p = Participant.getfromsession(request)
    if not e or not p:
        raise PermissionDenied("Event nicht gefunden")
        
    ci = Ci.objects.get(id = request.POST.get("id"))
    ci.name = request.POST.get("value")
    ci.save()
    return HttpResponse("saved")
