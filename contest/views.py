#Author : Rajeev S <rajeevs1992@gmail.com>, Dept. Of CSE
#Dyuthi'13 Govt. Engg. College Thrissur

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect,HttpResponse
from contest.models import Level,Contestant,Wrong,Log
from django.contrib.auth import logout
from django.contrib.auth.models import User


@login_required
def home(request):
    try:
        c = Contestant.objects.get(user__email = request.user.email)
    except:   
        return HttpResponseRedirect('/register')
    ret = {}
    if 'message' in request.GET:
        ret = {'message':request.GET['message']}
    try:
        ret['l'] = Level.objects.get(number = c.level)
    except Exception as e:
        ret['message'] = e
        return render(request, 'wait.html', ret)
    if 'level' in request.GET:
        ret['l'].new = True 
    return render(request, ret['l'].template, ret)

@login_required
def register(request):
    if request.method == 'GET':
        ret = {}
        ret['user'] = request.user
        try:
            c = Contestant.objects.get(user = request.user)
            return HttpResponseRedirect('/home')
        except Exception as e:
            ret['message'] = e
            return render(request, 'register.html', ret)
    else : 
        try:
            c = Contestant.objects.filter(user = request.user)
            if c:
                return HttpResponseRedirect('/home')
            c = Contestant(user = request.user, 
                           college = request.POST['college'], 
                           mobile = request.POST['mobile'], 
                           level = 1, 
                           bonus = 1,
                           openingLevel = 1)
            c.save()
        except Exception as e:
            return HttpResponseRedirect('/register/?message=All Fields are mandatory! %s'%e)
        return HttpResponseRedirect('/home')

@login_required
def inc(request):
    if request.is_ajax():
        c = Contestant.objects.get(user = request.user)
        c.clicks += 1
        c.save()
        return HttpResponse()
    else:
        u = User.objects.get(pk = request.user.id)
        u.is_active = False
        u.save()
        logout(request)
        return HttpResponseRedirect('/login/?message=Hack attempt prevented,your account has been suspended')

def slide(contestant, request):
    if contestant.clicks < 40:
        return -1
    else:
        return True
def sudoku(contestant, request):
    pass
#################################
solution = {}
solution['slide'] = slide
solution['sudoku'] = sudoku
#################################
@login_required        
def level_complete(request):
    if request.method == 'POST':
        try:
            c = Contestant.objects.get(user = request.user)
        except:
            return HttpResponseRedirect('/logout')
        l = Level.objects.get(number = c.level)
        answer = request.POST['ans']
        answer = answer.lower().strip().replace(' ','')
        log = Log(contestant = c, level = l, answer = request.POST['ans'])
        log.save()
        if answer in l.answer.split(';') and answer:
            c.level = c.level + 1
            score = Contestant.objects.filter(level = c.level).count()
            c.score = score
            c.save()
#            return HttpResponseRedirect('/home/?level=new')
            return HttpResponseRedirect('/passed')
        else:
            return HttpResponseRedirect('/level/wrong/?message=That does\'nt look like a solution!!')
    else:
        return HttpResponse('I am smarter than you')
@login_required        
def bonus_complete(request):
    pass

def hitlist(request):
    ret = {}
    c = Contestant.objects.all().order_by('-level', 'score')[:100]
    r = range(1,len(c) + 1)
    ret['c'] = zip(r, c)
    return render(request, 'hitlist.html', ret)

def allcontest(request):
    ret = {}
    c = Contestant.objects.all().order_by('-level', 'score')
    r = range(1,len(c) + 1)
    ret['c'] = zip(r, c)
    return render(request, 'allcontest.html', ret)

@login_required        
def passed(request):
    ret = {}
    c = Contestant.objects.get(user = request.user)
    ret['c'] = c
    return render(request, 'passed.html',ret)

@login_required        
def wrong(request):
    ret = {}
    ret['w'] = Wrong.objects.filter(active = True).order_by('?')[0]
    return render(request, 'wrong.html', ret)
