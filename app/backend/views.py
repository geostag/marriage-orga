from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import Http404,HttpResponse, HttpResponseRedirect
from backend.models import Event, Participant
from backend.forms import DocumentForm

# Create your views here.

@login_required
def base(request):
    el = Event.objects.filter(user=request.user)
    if len(el) == 1:
        return HttpResponseRedirect(reverse("backend.event",kwargs = {"id": el[0].id } ))
    else:
        return( render(request,"backend/event_select.html",{ "eventlist": el } ) )

@login_required
def event(request,id):
    try: 
        e = Event.objects.get(id = int(id))
    except ObjectDoesNotExist:
        try:
            e = Event.objects.get(namecode = id)
        except ObjectDoesNotExist:
            raise Http404("Event nicht gefunden")
            
    if not e.can_edit(request):
        raise PermissionDenied("Event gesperrt")
        
    if request.POST:
        dform = DocumentForm(request.POST,request.FILES)
        if dform.is_valid():
            d = dform.save(commit=False)
            if not d.event == e:
                raise Http404("Falsches Event angegeben")
            dform.save()
        else:
            dform.add_error(None,"Es ist ein Fehler aufgetreten.")
    else:
        dform = DocumentForm(initial={'event': e})
        
    c = { 
        "mevent": e, 
        "guests": Participant.objects.filter(event=e), 
        "dform": dform,
        "documentlist": e.document_set.all()
    }
    return render(request,"backend/event.html",c)
            
@login_required
def participant_remove(request,id):
    try:
        p = Participant.objects.get(id = int(id))
    except:
        raise Http404("Teilnehmer nicht gefunden")
        
    e = p.event
    if not e.can_edit(request):
        raise PermissionDenied("Keine Event Berechtigung")
        
    p.delete()
    return HttpResponseRedirect( reverse( "backend.event", kwargs={"id": e.id } ) )
    
@login_required
def participant_add(request,id):
    try:
        e = Event.objects.get(id = int(id))
    except:
        raise Http404("Event nicht gefunden")
        
    if not e.can_edit(request):
        raise PermissionDenied("Keine Event Berechtigung")
        
    p = Participant(event = e)
    p.save()
    return HttpResponseRedirect( reverse( "backend.event", kwargs={"id": e.id } ) )
    
@login_required
def participant_set(request):
    id = request.POST.get("gid")
    try:
        p = Participant.objects.get(id = int(id))
    except:
        raise Http404("Teilnehmer nicht gefunden")
        
    e = p.event
    if not e.can_edit(request):
        raise PermissionDenied("Keine Event Berechtigung")
        
    n = request.POST.get("name")
    v = request.POST.get("value")
    if n == "name":
        p.name = v
    elif n == "email":
        p.email = v
    elif n == "subcode":
        p.subcode = v
    elif n == "phone":
        p.phone = v
    elif n == "participation":
        p.participation = v
    else:
        return HttpResponseBadRequest("name not given '%s'" % n)
        
    p.save()
    return HttpResponse("saved")
