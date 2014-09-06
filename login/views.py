from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from contest.models import Contestant

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def userLogin(request):
    if request.method=='GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home')
        elif 'e' in request.GET:
            return render(request, 'login.html',{'error':'1'})
        else:
            return render(request, 'login.html',{},context_instance=RequestContext(request))
    else:
        user=authenticate(username=request.POST['uname'],password=request.POST['passwd'])
        if user is not None and user.is_active:
            login(request,user)
            return HttpResponseRedirect('/home')
        else:
            return HttpResponseRedirect('/login?e=1')

@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def home(request):
    ret={}
    if 'message' in request.GET:
        ret={'message':request.GET['message']}
    ret['r']=request
    return render(request, 'slide-puzzle.html',ret)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def welcome(request):
    logout(request)
    ret = {}
    c = Contestant.objects.all().order_by('-level', 'score')[:50]
    r = range(1,len(c) + 1)
    ret['c'] = zip(r, c)
    return render(request, 'welcome.html', ret)

def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/')

def autherror(request):
    logout(request)
    return render(request, 'autherror.html')
