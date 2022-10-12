from django.shortcuts import render

# Create your views here.


def temp(request):
    return render(request, 'app2/temp.html')


def add(request):
    return render(request, 'app2/add.html')


def sum(request):
    num1 = int(request.POST['num1'])
    num2 = int(request.POST['num2'])
    sum = num1 + num2
    context = {'sum': sum}
    return render(request, 'app2/sum.html', context)
