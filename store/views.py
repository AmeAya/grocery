from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import *


def homeView(request):
    return render(request=request, template_name='home.html')


def signInView(request):
    if request.method == 'GET':
        return render(request=request, template_name='sign_in.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        # authenticate - Если найден юзер в БД с таким имейлом и паролем то возвращает его, иначе None
        if user is not None:
            login(request, user)
            # login - Авторизует юзера user и дает ему csrf_token, sessionid
            return redirect('home_url')
        context = {
            'error': 'Не верный логин и/или пароль',
            'email': email
        }
        return render(request=request, template_name='sign_in.html', context=context)


def signUpView(request):
    if request.method == 'GET':
        return render(request=request, template_name='sign_up.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        birth_date = request.POST.get('birth_date')
        try:
            Customer.object.get(email=email)
        except Customer.DoesNotExist:
            customer = Customer(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                birth_date=birth_date
            )
            customer.set_password(password)
            customer.save()
            return redirect('sign_in_url')
        else:
            context = {
                'error': 'This email is already taken!',
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'birth_date': birth_date
            }
            return render(request=request, template_name='sign_up.html', context=context)


def signOutView(request):
    logout(request)  # Встроенная функция, которая выкидывает из системы юзера(Видит юзера по request.user)
    return redirect('home_url')  # Перенаправляем по url 'home_url'
