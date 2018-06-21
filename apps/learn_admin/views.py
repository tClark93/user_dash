from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import UserManager, User, Post, Comment

def index(request):
    return render(request, 'learn_admin/index.html')

def login(request):
    return render(request, 'learn_admin/sign_in.html')

def loginUser(request):
    if User.objects.filter(email=request.POST['email']):
        user = User.objects.get(email=request.POST['email'])
        request.session['first_name']=user.first_name
        request.session['email']=user.email
        print('post is working')
        print(request.POST['password'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print("password match")
            if user.is_admin == 'Admin':
                return redirect('/dashboard/admin')
            return redirect('/dashboard')
    messages.error(request, 'Username and Password do not match')
    print (request.method)
    return redirect('/login')

def register(request):
    return render(request, 'learn_admin/register.html')

def home(request):
    user = User.objects.get(email=request.session['email'])
    if user.is_admin == 'Admin':
        return redirect('/dashboard/admin')
    if user.is_admin == 'Peasant':
        return redirect('/dashboard')
    return redirect ('/')

def dashboard(request):
    context = {
        'users': User.objects.all(),
    }
    return render(request, 'learn_admin/dashboard.html', context)

def adminDash(request):
    user = User.objects.get(email = request.session['email'])
    if user.is_admin != 'Admin':
        return redirect('/dashboard')
    context = {
        'users': User.objects.all(),
    }
    return render(request, 'learn_admin/admin.html', context)

def registerUser(request):
    errors = User.objects.valid(request.POST)
    request.session['first_name'] = request.POST['first_name']
    request.session['last_name'] = request.POST['last_name']
    request.session['email'] = request.POST['email']
    if len(errors):
        for message in errors:
            messages.error(request, message)
        return redirect('/register')
    tempPass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'], email=request.POST['email'],password=tempPass)
    user = User.objects.get(email=request.session['email'])
    if user.is_admin == Admin:
        return redirect('/dashboard/admin')
    return redirect('/dashboard')

def edit(request,id):
    context = {
        'profile':User.objects.get(id=id)
    }
    return render(request, 'learn_admin/edit_user.html', context)


def newuser(request):
    return render(request, 'learn_admin/newuser.html')

def createnew(request):
    errors = User.objects.valid(request.POST)
    if len(errors):
        for message in errors:
            messages.error(request, message)
        return redirect('/users/new')
    tempPass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'], email=request.POST['email'],password=tempPass)
    return redirect('/dashboard/admin')

def profile(request):
    context = {
        'profile':User.objects.get(email=request.session['email'])
    }
    return render(request, 'learn_admin/edit_self.html', context)

def changeinfo(request):
    errors = User.objects.validinfo(request.POST)
    user = User.objects.get(email=request.session['email'])
    if len(errors):
        for message in errors:
            messages.error(request, message)
        return redirect('/profile') 
    user.first_name=request.POST['first_name']
    user.last_name=request.POST['last_name']
    user.email=request.POST['email']
    user.save()
    request.session['email'] = request.POST['email']
    return redirect('/profile') 

def changepass(request):
    errors = User.objects.validpass(request.POST)
    user = User.objects.get(email=request.session['email'])
    if len(errors):
        for message in errors:
            messages.error(request, message)
        return redirect('/profile') 
    tempPass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user.password=tempPass
    user.save()
    return redirect('/profile') 

def changedesc(request):
    user = User.objects.get(email=request.session['email'])
    user.description=request.POST['desc']
    user.save()
    return redirect('/profile') 

def adminchangeinfo (request):
    errors = User.objects.validinfo(request.POST)
    user = User.objects.get(id=request.POST['id'])
    if len(errors):
        for message in errors:
            messages.error(request, message)
        return redirect('/profile') 
    user.first_name=request.POST['first_name']
    user.last_name=request.POST['last_name']
    user.email=request.POST['email']
    user.is_admin=request.POST['level']
    id = request.POST['id']
    return redirect('/dashboard/admin') 

def adminchangepass (request):
    errors = User.objects.validpass(request.POST)
    user = User.objects.get(id=request.POST['id'])
    if len(errors):
        for message in errors:
            messages.error(request, message)
        return redirect('/profile') 
    tempPass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user.password=tempPass
    user.save()
    return redirect('/dashboard/admin') 

def remove(request, id):
    User.objects.get(id=id).delete()
    return redirect('/dashboard/admin')

def userwall(request, id):
    request.session['id'] = id
    context = {
        'profile': User.objects.get(id=id),
        'posts': Post.objects.all(),
        'comments': Comment.objects.all()
    }
    return render(request, 'learn_admin/user_wall.html',context)

def post(request):
    poster = User.objects.get(email=request.session['email'])
    reciever = User.objects.get(id=request.session['id'])
    request.session['first_name'] = poster.first_name
    Post.objects.create(content=request.POST['post'], written_by=poster, written_on=reciever)
    return redirect('/users/show/'+request.session['id'])

def comment(request):
    user = User.objects.get(email=request.session['email'])
    post = Post.objects.get(id=request.POST['hidden'])
    Comment.objects.create(content=request.POST['comment'],commented_by=user,post=post)
    print(request.POST['comment'])
    return redirect('/users/show/'+request.session['id'])

def logoff(request):
    print('logging off')
    request.session.clear()
    print(request.session)
    return redirect('/')