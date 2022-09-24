from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView
from django.contrib.auth.decorators import login_required
                           
from tinda.models import TindaDates, UploadModel, Comment
from tinda.forms import NewTinda, CustomUserCreationForm, CommentForm, UploadForm
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import calendar

def home(request):
    search_query=""
    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')
    gallery=UploadModel.objects.distinct().filter(Q(name__icontains=search_query)|
                                                  Q(user__username__icontains=search_query)|
                                                  Q(category__name__icontains=search_query)).order_by('-timestamp')
    context={'gallery':gallery, 'search_query':search_query}
    return render(request, 'base.html', context)

@login_required(login_url='login')
def commentPost(request, pk):
    post=UploadModel.objects.get(id=pk)
    comment=Comment.objects.filter(post=post)

    form=CommentForm()
    if request.method=='POST':
        form=CommentForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.info(request, 'Comment added successfully')
            return redirect('comment', pk)
        else:
            messages.info(request, 'An error has occurred')

    context={'comment':comment, 'post':post, 'form':form}
    return render(request, 'comment.html', context)

@login_required(login_url="login")
def galleryview(request):
    queryset=TindaDates.objects.get(user=request.user)
    model=UploadModel.objects.filter(user__username=request.user)
    # form=UploadForm()
    form=UploadForm(request.POST)
    if form.is_valid():
        user=form.save(commit=False)
        user.save()
        messages.info(request, "form submitted")
        return redirect('details')
        
    context={
        "model":model,
        "form":form,
        'queryset':queryset
    }
    return render(request, 'details.html', context)


class NewTindaCreateView(CreateView):
    form_class=NewTinda
    queryset=TindaDates.objects.all()
    template_name='tinda-form.html'
    success_url='new_tinda'


def loginPage(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        try:
            user=User.objects.get(username=username)
        except:
            user=None
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')        
    return render(request, 'login.html')

def lougoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    form=CustomUserCreationForm()
    if request.method=='POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.save()
            messages.info(request, 'User created successfully')
            login(request, user)
            return redirect('new_tinda')
        else:
            messages.info(request, 'An error has occurred')
    return render(request, 'register.html', {'form':form})
