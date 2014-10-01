from django.db import models
from pypinyin import pinyin
import pypinyin
import re
# Create your models here.
class tuanju(models.Model):
    name = models.CharField(max_length =64)
    icon = models.FileField(upload_to='icons')
    url = models.TextField()
    tuanju_type = models.CharField(max_length = 64)
    order = models.IntegerField(default=0)

    def list(self,tuanju_type,key=None,target=None):
        if not key:
            if tuanju_type == 'all':
                list =  tuanju.objects.all().order_by('name')
            else:
                list = tuanju.objects.filter(tuanju_type=tuanju_type).order_by('name')
        else:
            if tuanju_type == 'all':
                list = tuanju.objects.filter(name__contains = key).order_by('name')
            else:
                list = tuanju.objects.filter(tuanju_type=tuanju_type,name__contains = key).order_by('name')
        for t in list:
            name_pinyin = pinyin(t.name,style=pypinyin.INITIALS)
            shouzimu = name_pinyin[0][0][0]
            rematch = re.match(r'[a-zA-Z]',shouzimu)
            if not rematch:
                shouzimu = '#'
            t.shouzimu = shouzimu.upper()
            t.type = 'weixin'
            t.icon = '/media/'+t.icon.__str__()

        #add shouzimu
        newlist = []
        current_shouzimu = ''
        for t in list:
            if t.shouzimu == current_shouzimu:
                newlist.append(t)
                continue;
            else:
                current_shouzimu = t.shouzimu
                newlist.append({'name':current_shouzimu,'type':'shouzimu'})
            newlist.append(t)
        if target=='show':
            return newlist
        else:
            return list
