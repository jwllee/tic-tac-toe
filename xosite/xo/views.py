from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello world. You're at xo index.")


def board_3x3(request):
    context = {}
    return render(request, 'xo/3x3.html', context)


def board_4x4(request):
    context = {}
    return render(request, 'xo/4x4.html', context)
