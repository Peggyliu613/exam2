from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *


def index(request):
    return render(request, 'index.html')

def login(request):
    if not request.POST['email']:
        return redirect('/')

    errors=Users.objects.validator_login(request.POST)
    if errors:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')
    
    user=Users.objects.get(email=request.POST['email'])
    request.session['user']=user.id
    return redirect('/dashboard')

def registerpage(request):
    return render(request, 'register.html')

def register(request):
    errors=Users.objects.validator(request.POST)

    if errors:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/registerpage')
    else:
        f=request.POST['first_name']
        l=request.POST['last_name']
        e=request.POST['email']
        p=request.POST['password']
        p_hash= bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()
        Users.objects.create(first_name=f, last_name=l, email=e, password=p_hash)

        user=Users.objects.get(email=request.POST['email'])
        request.session['user']=user.id
    return redirect('/dashboard')

def dashboard(request):
    if 'user' not in request.session or request.session['user'] == None:
        return redirect('/')

    context={
        "user":Users.objects.get(id=request.session['user']),
        "all_jobs":Jobs.objects.all(),
    }
    return render(request, 'dashboard.html', context)


def add_jobs_page(request):
    context={
        "user":Users.objects.get(id=request.session['user']),
        "all_jobs":Jobs.objects.all(),
    }
    return render(request, 'add_jobs.html', context)

def add_a_job(request):
    errors=Jobs.objects.validator(request.POST)

    if errors:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/add_jobs_page')
    else:
        t=request.POST['title']
        d=request.POST['desc']
        l=request.POST['location']
        user=Users.objects.get(id=request.session['user'])
        o=request.POST['other']
        
        a=[]
        for i in range(1,4):
            try:
                a.append(request.POST[f'category{i}'])
            except:
                print(f'category{i} not exit')
        c=""
        for i in a:
            c=c+i+", "
        
        c=c[:-2]
        
        if request.POST['other']:
            c+=request.POST['other']

        Jobs.objects.create(title=t, desc=d, location=l, uploaded_by=user, category=c)
    return redirect('/dashboard')

def job_info(request, id):
    context={
        "user":Users.objects.get(id=request.session['user']),
        "the_job":Jobs.objects.get(id=id),
    }
    return render(request, 'job_info.html', context)

def delete(request, id):
    the_job=Jobs.objects.get(id=id)
    the_job.delete()
    return redirect('/dashboard')

def cancel(request):
    return redirect('/dashboard')

def edit_jobs_page(request, id):
    context={
        "user":Users.objects.get(id=request.session['user']),
        "the_job":Jobs.objects.get(id=id),
    }
    return render(request, 'edit_jobs.html', context)

def edit(request, id):
    errors=Jobs.objects.validator(request.POST)

    if errors:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect(f'/edit_jobs_page/{id}')
    else:
        the_job=Jobs.objects.get(id=id)
        the_job.title=request.POST['title']
        the_job.desc=request.POST['desc']
        the_job.location=request.POST['location']
        the_job.save()

    return redirect('/dashboard')

def logout(request):
    request.session['user']=None
    return redirect('/')

def add_to_myjob(request, id):
    the_job=Jobs.objects.get(id=id)
    user=Users.objects.get(id=request.session['user'])
    user.jobs_added.add(the_job)
    return redirect('/dashboard')

def remove_from_myjob(request, id):
    the_job=Jobs.objects.get(id=id)
    user=Users.objects.get(id=request.session['user'])
    user.jobs_added.remove(the_job)
    return redirect('/dashboard')