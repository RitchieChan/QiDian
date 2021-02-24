from django.shortcuts import render
from newModel.models import *
# Create your views here.


def manager(request):
    if request.method == "GET":
        objList = authenticate.objects.all()
        return render(request, 'manager.html', {"objList": objList})
    else:
        idnum = request.POST.get('id')
        obj = authenticate.objects.get(pk=idnum)

        number = request.POST.get('number')
        number = int(number)
        number1 = number // 10
        number = number - number1 * 10

        if number1 == 1:
           obj.teacherStatus = number
        elif number1 == 2:
            obj.studentStatus = number
        elif number1 == 3:
            obj.idStatus = number
        elif number1 == 4:
            obj.EnglishStatus = number
        elif number1 == 5:
            obj.ElseStatus = number
        obj.save()
        objList = authenticate.objects.all()
        return render(request, 'manager.html', {"objList": objList})