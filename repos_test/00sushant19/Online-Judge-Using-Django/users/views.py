from pyexpat import model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:

            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('user_register')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('user_register')

            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1)
                user.save()
                messages.success(request, f'Account Created for {username}!')
                return redirect('user_login')

        else:
            messages.info(request, 'passwords don\'t matching')
            return redirect('user_register')

    else:
        return render(request, 'register.html', {'title': 'Register - Let-Us-Code'})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, 'logged in')
            return redirect('problem_page')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('user_login')
    else:
        return render(request, 'login.html', {'title': 'Login - Let-Us-Code'})


def logout(request):
    auth.logout(request)
    return redirect('problem_page')


