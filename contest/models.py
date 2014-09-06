from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Level(models.Model):
    number = models.IntegerField(default = 0, unique = True)
    name = models.CharField(max_length = 25)
    image = models.ImageField(upload_to = 'contest', null = True, blank = True)
    dialogue = models.CharField(max_length = 100, null = True, blank = True)
    answer = models.CharField(max_length = 50, null = True, blank = True)

    template = models.CharField(max_length = 25, default = 'level.html')
    attribute = models.TextField(max_length = 1000, blank = True, null = True)

    is_bonus = models.BooleanField(default = False)

    def __unicode__(self): 
        return str(self.number)


class Wrong(models.Model):
    image = models.ImageField(upload_to = 'teasers')
    heading = models.CharField(max_length = 100)
    active = models.BooleanField(default = True)

    def __unicode__(self): 
        return str(self.id)


class Contestant(models.Model):
    user = models.ForeignKey(User, unique = True)
    college = models.CharField(max_length = 128)
    mobile = models.CharField(max_length = 10)

    level = models.IntegerField()
    bonus = models.IntegerField()
    openingLevel = models.IntegerField()
   
    score = models.IntegerField(default = 0)

    def __unicode__(self): 
        return self.user.username

class Log(models.Model):
    contestant = models.ForeignKey(Contestant)
    level = models.ForeignKey(Level)
    answer = models.TextField(max_length = 1000)

    def __unicode__(self):

        return str(self.level.number) + '.' + self.answer

class ContestantAdmin(admin.ModelAdmin):
    list_display = ('user','level','mobile')
class LogAdmin(admin.ModelAdmin):
    list_display = ('contestant','level','answer')
    list_filter = ('contestant', 'level','answer')
    search_fields = ['contestant__user__first_name']
admin.site.register(Level)
admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Wrong)
admin.site.register(Log,LogAdmin)
