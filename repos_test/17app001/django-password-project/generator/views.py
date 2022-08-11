from django.http import HttpResponse
from django.shortcuts import render
import random
# Create your views here.


def password(request):
    length = request.GET['length']
    input_length = request.GET.get('input-length')
    length = input_length if input_length else length
    # a~z
    password_words = [chr(i) for i in range(97, 123)]
    # 大寫
    if request.GET.get('uppercase'):
        password_words += [chr(i) for i in range(65, 91)]
    # 數字
    if request.GET.get('number'):
        password_words += [chr(i) for i in range(48, 58)]
    # 特殊
    if request.GET.get('special'):
        password_words += list('@#$%^&*')

    password = ''.join([random.choice(password_words)
                        for i in range(eval(length))])

    return render(request, './password.html', {'password': password})


def index(request):

    return render(request, './index.html')
