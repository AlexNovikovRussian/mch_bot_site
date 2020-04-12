from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from auth_system.forms import MosRuForm
from django.contrib.auth import login
from django.contrib.auth import logout as lout
from auth_system.models import MosUser
from django.contrib.auth.models import User
from time import time

def get_client_get(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def reg(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            elif request.POST.get('next'):
                return HttpResponseRedirect(request.POST.get('next'))
        
            return HttpResponseRedirect(reverse("AuthSystem:dashboard"))
    else:
        form = UserCreationForm()
    return render(request, 'reg.html', {"form" : form})

def auth(request):
    context = {}
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            elif request.POST.get('next'):
                return HttpResponseRedirect(request.POST.get('next'))
             
            return HttpResponseRedirect(reverse("AuthSystem:dashboard"))
    else:
        form = AuthenticationForm()
        
    if request.GET.get('next'):
        context['next_'] = request.GET.get('next')
    elif request.POST.get('next'):
        context['next_'] = request.POST.get('next')

    context['form'] = form
    return render(request, 'auth.html', context)
    
def test(request):
    return HttpResponse(request.user.is_authenticated)

@login_required()
def add_mosru(request):
    try:
        mosuser = MosUser.objects.get(user_id=request.user.id)
    except MosUser.DoesNotExist:
        if request.method == "POST":
            form = MosRuForm(data=request.POST)
            if form.is_valid():
                dt = form.cleaned_data.copy()
                dt['user'] = request.user

                u = MosUser(user = dt['user'], mosLogin = dt['mosLogin'], mosPassword = dt['mosPassword'])
                u.save()

                if request.GET.get('next'):
                    return HttpResponseRedirect(request.GET.get('next'))
                elif request.POST.get('next'):
                    return HttpResponseRedirect(request.POST.get('next'))
                
                return HttpResponseRedirect(reverse("AuthSystem:dashboard"))
        else:
            form = MosRuForm()
        return render(request, "addmosru.html", {'form':form})
    return HttpResponseRedirect(reverse("AuthSystem:edit_mosru"))
    

def detail(request, user_id):
    options = {}

    user = get_object_or_404(User, id=user_id)
    options['user_'] = user
    try:
        mosuser = MosUser.objects.get(user_id=user_id)
        options["mosuser_exist"] = True
        options["mosuser"] = mosuser

        a = list(mosuser.mosPassword)[:2]
        options["passlets"] = ""
        for l in a:
            options["passlets"] += l
        options["passlets"] += "*" * (len(list(mosuser.mosPassword)) - 2)
    except MosUser.DoesNotExist:
        options["mosuser_exist"] = False
    return render(request, "detail.html", options)

@login_required        
def edit_mosru(request):
    try:
        mosuser = MosUser.objects.get(user_id=request.user.id)
    except MosUser.DoesNotExist:
        return HttpResponseRedirect(reverse("AuthSystem:add_mosru"))
    if request.method == "POST":
        form = MosRuForm(data=request.POST)
        if form.is_valid():
            dt = form.cleaned_data.copy()

            mosuser.mosLogin = dt["mosLogin"]
            mosuser.mosPassword = dt['mosPassword']
            mosuser.save()

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            elif request.POST.get('next'):
                return HttpResponseRedirect(request.POST.get('next'))
            
            return HttpResponseRedirect(reverse("AuthSystem:dashboard"))
    else:
        form = MosRuForm()
    return render(request, "editmosru.html", {'form':form})

@login_required
def dashboard(request):
    return HttpResponseRedirect(reverse("AuthSystem:detail", args=(request.user.id,)))

@login_required
def logout(request):
    lout(request)
    return render(request, 'logout.html')

@login_required
def addvk(request):
    return render(request, 'addvk.html')

    