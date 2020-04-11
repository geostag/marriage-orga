from django.db import models
from django.contrib.auth.models import User
import random,string

# Create your models here.

class Doubleoptinlog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    oikey = models.CharField(max_length=70)
    opt1 = models.DateTimeField(auto_now_add=True)
    opt2 = models.DateTimeField(null=True,blank=True)
    
    def genkey(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

    def save(self, *args, **kwargs):
        if not self.oikey:
            self.oikey = self.genkey()
        super(Doubleoptinlog, self).save(*args, **kwargs)

