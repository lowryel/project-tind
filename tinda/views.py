from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
                           
from tinda.models import TindaDates, UploadModel, Comment
from tinda.forms import NewTinda, CustomUserCreationForm, CommentForm
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def home(request):
    search_query=""
    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')
    gallery=UploadModel.objects.distinct().filter(Q(name__icontains=search_query)|
                                                  Q(owner__username__icontains=search_query)|
                                                  Q(category__name__icontains=search_query)).order_by('-timestamp')
    context={'gallery':gallery, 'search_query':search_query}
    return render(request, 'base.html', context)

@login_required(login_url='login')
def commentPost(request, pk):
    post=UploadModel.objects.get(id=pk)
    comment=Comment.objects.filter(post=post)
    for i in comment:
        print(i.post.owner)

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


@login_required(login_url='login')
def user_details(request):
    model=TindaDates.objects.get(username=request.user)
    mygallery=UploadModel.objects.filter(owner=request.user)
    form=NewTinda(instance=model)
    if request.method=='POST':
        
        form=NewTinda(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form,'model':model, 'owner_gallery':mygallery}
    return render(request, 'details.html', context)


class NewTindaCreateView(CreateView):
    form_class=NewTinda
    queryset=TindaDates.objects.all()
    template_name='tinda-form.html'
    success_url='/'


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
            messages.info(request, 'Invalid credentials')
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
            return redirect('/')
        else:
            messages.info(request, 'An error has occurred')
    return render(request, 'register.html', {'form':form})
