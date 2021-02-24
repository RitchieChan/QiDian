from django.shortcuts import render

# Create your views here.
def bbs(request):
    return render(request,'bbs.html',{})