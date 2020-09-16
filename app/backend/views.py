from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import Http404,HttpResponse, HttpResponseRedirect
from backend.models import Event, Participant, Coli, Checkoutlist, Document, Ci
from backend.forms import DocumentForm, ColiForm

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
        
    g = Participant.objects.filter(event=e).order_by('subcode','id')
        
    c = { 
        "mevent": e, 
        "guests": g, 
        "stats": { 
            "guest": { "ja": g.filter(participation=1).count(), "nein": g.filter(participation=2).count(), "vlt": g.filter(participation=3).count(), "min": g.filter(participation=0).count() }
        }
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

@login_required
def coli_add(request,col_id):
    try:
        col = Checkoutlist.objects.get(id = int(col_id))
    except:
        raise Http404("Checkoutlist nicht gefunden")
        
    e = col.event
    if not e.can_edit(request):
        raise PermissionDenied("Keine Event Berechtigung")
    c = Coli(checkoutlist = col)
    c.save()
    return HttpResponseRedirect( reverse( "backend.event", kwargs={"id": e.id } ) )

@login_required
def coli_edit(request,coli_id):
    try:
        c = Coli.objects.get(id = int(coli_id))
    except:
        raise Http404("Item nicht gefunden")
        
    e = c.checkoutlist.event
    if not e.can_edit(request):
        raise PermissionDenied("Keine Event Berechtigung")
        
    if request.POST:
        coliform = ColiForm(request.POST,request.FILES,instance=c)
        if coliform.is_valid():
            c = coliform.save(commit=False)
            if not c.checkoutlist.event == e:
                raise Http404("Falsches Event angegeben")
            c.save()
            return HttpResponseRedirect( reverse( "backend.event", kwargs={"id": e.id } ) )
        else:
            coliform.add_error(None,"Es ist ein Fehler aufgetreten.")
    else:
        coliform = ColiForm(instance = c)
        
    c = { "form": coliform }
        
    return render(request,"backend/coli_edit.html",c)

@login_required
def coli_delete(request,coli_id):
    try:
        c = Coli.objects.get(id = int(coli_id))
    except:
        raise Http404("Item nicht gefunden")
        
    e = c.checkoutlist.event
    if not e.can_edit(request):
        raise PermissionDenied("Keine Event Berechtigung")

    c.delete()
    return HttpResponseRedirect( reverse( "backend.event", kwargs={"id": e.id } ) )
    
@login_required
def document_add(request,event_id):
    try:
        e = Event.objects.get(id = int(event_id))
    except:
        raise Http404("Event nicht gefunden")
        
    if not e.can_edit(request):
        raise PermissionDenied("Keine Event Berechtigung")
        
    d = Document(event = e)
    d.save()
    
    return HttpResponseRedirect( reverse("backend.document.edit", kwargs={"document_id": d.id }) )
        
@login_required
def document_edit(request,document_id):
    try:
        d = Document.objects.get(id = int(document_id))
    except:
        raise Http404("Dokument nicht gefunden")
        
    e = d.event
    if not e.can_edit(request):
        raise PermissionDenied("Keine Event Berechtigung")
        
    if request.POST:
        form = DocumentForm(request.POST,request.FILES,instance=d)
        if form.is_valid():
            d = form.save(commit=False)
            if not d.event == e:
                raise Http404("Falsches Event angegeben")
            d.save()
            return HttpResponseRedirect( reverse( "backend.event", kwargs={"id": e.id } ) )
        else:
            form.add_error(None,"Es ist ein Fehler aufgetreten.")
    else:
        form = DocumentForm(instance = d)
        
    c = { "form": form, "mevent": e }
    return render(request,"backend/document_edit.html",c)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def participant_list(request,id):
    try: 
        e = Event.objects.get(id = int(id))
    except ObjectDoesNotExist:
        try:
            e = Event.objects.get(namecode = id)
        except ObjectDoesNotExist:
            raise Http404("Event nicht gefunden")
            
    db = {}
    for p in Participant.objects.filter(event=e).order_by('subcode','id'):
        s = p.subcode
        if not s in db:
            db[s] = { "participants": [], "contributions": [], "colis": [] }
        db[s]["participants"].append(p)
        
    for s in db.keys():
        for c in Ci.objects.filter(subcode = s):
            if c.name != "" and c.name != "-":
                db[s]["contributions"].append( c )

    for s in db.keys():
        for c in Coli.objects.filter(subcode = s):
            db[s]["colis"].append( c )
            
    for d in e.checkoutlist_set.all():
        for c in d.coli_set.all():
            s = c.subcode
            if not s in db:
                db[s] = { "participants": [], "contributions": [], "colis": list( Coli.objects.filter(subcode = s) ) }
            
    db2 = []
    for s in db:
        db2.append( { "subcode": s, "participants": db[s]["participants"], "contributions": db[s]["contributions"], "colis": db[s]["colis"] } )
            
    return render(request,"backend/event_participantlist.html",{ "db": db2, "mevent": e } )