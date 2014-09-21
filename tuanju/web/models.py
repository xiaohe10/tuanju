from django.db import models

# Create your models here.
class tuanju(models.Model):
    name = models.CharField(max_length =64)
    icon = models.FileField(upload_to='icons')
    url = models.TextField()
    tuanju_type = models.CharField(max_length = 64)
    order = models.IntegerField(default=0)

    def list(self,tuanju_type):
        if tuanju_type == '':
            list =  tuanju.objects.all().order_by('order')
        else:
            list = tuanju.objects.filter(tuanju_type=tuanju_type).order_by('order')

        for t in list:
            t.icon = '/media/'+t.icon.__str__()
        return list
