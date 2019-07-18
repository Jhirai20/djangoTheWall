from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    return render(request,'wall_app/index.html')

def register(request):
    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        Users.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'], email=request.POST['email'],pw_hash=bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()))
        messages.success(request,"Registration Complete")
        request.session['email'] = request.POST['email']
        return redirect('/success')



def login(request):
    try:
        user=Users.objects.get(email=request.POST['email'])
    except:
        messages.error(request,"User does not exist")
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode()):
        print("password match")
        request.session['email'] = request.POST['email']
        return redirect('/success')
    else:
        print("failed password")
        return redirect('/')

def success(request):
    while 'email' in request.session:
        user=Users.objects.get(email=f"{request.session['email']}")
        messages=Messages.objects.all()
        comments=Comments.objects.all()
        context ={
        'user':user.first_name,
        'messages':messages,
        'comments' :comments,
        }
        return render(request,'wall_app/success.html', context)
    else:
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def message(request):
    user=Users.objects.get(email=f"{request.session['email']}")
    Messages.objects.create(message=request.POST['message'],user=user)
    return redirect('/success')

def comment(request):
    user=Users.objects.get(email=f"{request.session['email']}") #WTF!!!!
    message=Messages.objects.get(id=f"{request.POST['message_id']}")
    Comments.objects.create(comment=request.POST['comment'],user=user,message=message)
    return redirect('/success')

def deletec(request):
    user=Users.objects.get(email=f"{request.session['email']}")
    comment=Comments.objects.get(id=f"{request.POST['commentid']}")
    print(comment.user.id)
    print(user.id)
    if user.id==comment.user.id:
        print("deleting")
        comment.delete()
        return redirect('/success')
    return redirect('/success')