from django.shortcuts import render
from django.http import HttpResponse

def Index(request):
    return render(request, 'Index.html')

def Test(request):
    return HttpResponse(u"歡迎光臨!")