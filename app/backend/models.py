from django.conf import settings
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
import random,string,pyqrcode,tempfile,os

# Create your models here.
class Event(models.Model):
    name = models.CharField("Event Name",max_length=100)
    namecode = models.CharField("Shortcut",max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    autoreg = models.CharField(max_length=32,blank=True)
    password = models.CharField("Passwort",max_length=32,blank=True)
    
    @classmethod
    def getfromsession(cls,request):
        try:
            return cls.objects.get(id = request.session["eid"])
        except:
            return None
        
    def __str__(self):
        return self.name
        
    def can_edit(self,request):
        return ( request.user == self.user or request.user.is_superuser )
        
    def get_url(self):
        return "%s%s" % (settings.BASE_ADDRESS,reverse("event.enter", kwargs={"shortcut": self.namecode}))

    def get_qrcode(self):
        qr = pyqrcode.create( self.get_url(), encoding = "utf-8" )
        fd, fname = tempfile.mkstemp()
        os.close(fd)
        qr.svg(fname,scale=2)
        with open(fname) as f:
            lines = f.readlines()
        os.remove(fname)
        return "".join( [ x.strip() for x in lines ] )
        
    def genkey(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

    def save(self, *args, **kwargs):
        if not self.autoreg:
            self.autoreg = self.genkey()
        super(Event, self).save(*args, **kwargs)

class Participant(models.Model):
    name = models.CharField("Name",max_length=100, default="-")
    email = models.EmailField("E-Mail",null=True,blank=True,default="")
    phone = models.CharField("Telefonnummer",max_length=100,null=True,blank=True,default="")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    subcode = models.CharField("Anmeldecode",max_length=16,blank=True)
    participation_choices = ( (0,"---"),(1,"ich komme"),(2,"ich komme nicht"),(3,"weiß noch nicht"))
    participation = models.IntegerField('Teilnahme',choices=participation_choices, default=0)
    
    @classmethod
    def getfromsession(cls,request):
        try:
            return cls.objects.get(id = request.session["pid"])
        except:
            return None

    def __str__(self):
        if self.event:
            return "%s: %s" % (str(self.event),self.name)
        else:
            return "-: %s" % self.name
            
    def participation_cute(self):
        if self.participation == 0:
            return "---"
        elif self.participation == 1:
            return "ich komme"
        elif self.participation == 2:
            return "ich komme nicht"
        else:
            return "weiß noch nicht"
    
    def genkey(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))

    def save(self, *args, **kwargs):
        if not self.subcode:
            self.subcode = self.genkey()
        super(Participant, self).save(*args, **kwargs)

class Contribution(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return "%s: %s (%s)" (self.event.name,self.name,str(self.user))
