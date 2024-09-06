from django.shortcuts import render, redirect, get_object_or_404
#from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
#Crea una cookie por nosotros
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Tareas
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
  return render(request,'home.html')

def signup(request):
  if request.method == 'GET':
    return render(request, 'signup.html',{
      'form': UserCreationForm
    })
  else:
    if request.POST['password1'] == request.POST['password2']:
      #registrar usuario
      try:
        user= User.objects.create_user(username=request.POST['username'], 
        password= request.POST['password1'])
        user.save()
        login(request,user)
        return redirect('tasks')
        #return HttpResponse('Usuario creado correctamente')
      except IntegrityError:
        return render(request, 'signup.html',{
      'form': UserCreationForm,
      'error': 'Usuario ya existe.'
        })
      
    return render(request, 'signup.html',{
      'form': UserCreationForm,
      'error': 'Contraseñas no coinciden'
    })
  #return render(request,'signup.html',{
  #  'form': UserCreationForm
  #})

@login_required
def tasks(request):
    #tasks= Tareas.objects.all()
    tasks= Tareas.objects.filter(user=request.user, datecompleted__isnull= True)
    return render(request, 'tasks.html',{'tasks':tasks})

@login_required
def tasks_complete(request):
    #tasks= Tareas.objects.all()
    tasks= Tareas.objects.filter(user=request.user, datecompleted__isnull= False).order_by('-datecompleted')
    return render(request, 'tasks.html',{'tasks':tasks})

@login_required
def create_task(request):
  if request.method == 'GET':
    return render(request,'create_task.html',{
      'form': TaskForm
    })
  else:
    try:
      form= TaskForm(request.POST)
      new_task= form.save(commit=False)
      new_task.user= request.user
      new_task.save()
      return redirect('tasks')
    except ValueError:
      return render(request,'create_task.html',{
      'form': TaskForm,
      'error': 'Validar error presentado'
      })

@login_required
def task_detail(request,task_id):
  if request.method == 'GET':
    #task=Tareas.objects.get(pk=task_id)
    task=get_object_or_404(Tareas,pk=task_id, user=request.user)
    #Se va pasar la tarea y va llenar el formulario con la tarea
    form= TaskForm(instance= task)
    return render(request, 'task_detail.html',{'task': task, 'form': form})
  else:
    try:
      task=get_object_or_404(Tareas,pk=task_id, user=request.user)
      form= TaskForm(request.POST, instance= task)
      form.save()
      return redirect('tasks')
    except ValueError:
     return render(request, 'task_detail.html',{
       'task': task, 
       'form': form,
       'error': 'Problemas al editar.'
       })
    
@login_required
def task_complete(request, task_id):
  task= get_object_or_404(Tareas, pk=task_id, user= request.user)
  if request.method == 'POST':
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')
  
@login_required
def task_delete(request, task_id):
  task= get_object_or_404(Tareas, pk=task_id, user= request.user)
  if request.method == 'POST':
    task.delete()
    return redirect('tasks')

@login_required
def cerrarSesion(request):
  logout(request)
  return redirect('home')

def acceso(request):
  if request.method == "GET":
    return render(request, 'signin.html',{
      'form': AuthenticationForm
    })
  else:
    user= authenticate(request, username= request.POST['username'], password= request.POST['password'])
    if user is None:
      return render(request, 'signin.html',{
        'form': AuthenticationForm,
        'error': 'Acceso Incorrecto!!'
      })
    else:
      login(request,user)
      return redirect('tasks')
    #print(request.POST)
