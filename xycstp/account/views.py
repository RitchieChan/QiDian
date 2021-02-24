from django.shortcuts import render
from newModel.models import *
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core import serializers
import os
from django.conf import settings
import json
# Create your views here.


def login(request):
    if request.method == "GET":
        account = request.session.get('account', None)
        if account:
            return redirect('/personal/')
        else:
            return render(request,'login.html',{})
    elif request.method == "POST":
        passWord = request.POST.get("passWord",None)
        content = request.POST.get("content",None)
        isRememberPSW = request.POST.get("isRememberPSW",0)
        if content.find("@")>=0:
            email = content
            users = User.userObj.filter(email = email,passWord = passWord)
        else:
            phoneNum = content
            users = User.userObj.filter(phoneNum = phoneNum,passWord = passWord)
        if users:
            request.session['account'] = users[0].account  #登陆成功之后存account进session
            if isRememberPSW:
                request.session.set_expiry(None)
            else:
                request.session.set_expiry(0)   #设置关闭浏览器session就失效
            return HttpResponse(json.dumps({'state':True,'account':users[0].account}))
        else:
            return HttpResponse(json.dumps({'state':False}))


def register(request):
    if request.method == "POST":
        step = int(request.POST.get("step",0))
        step += 1
        return render(request,'register.html',{"step":step})
    else:
        step = int(request.GET.get("step",0))
        step += 1
        return render(request,'register.html',{"step":step})


# #老师认证
# def authenticate(request):
#     if request.method == "GET":
#         return render(request, 'authenticate.html')
#     elif request.method == "POST":
#         account1 = request.session.get('account1', None)  #取出注册时session存的account1
#         if account1 == None:
#             return redirect('/account/register/')
#         users = User.userObj.filter(account = account1)
#         if users:
#             userId = users[0].id

#             #问题：老师注册认证时要不要先给个老师账号？因为authenticate模型是与Teacher模型关联的，
#             #不给的话，可能还要在User模型里关联authenticate。
#             teacherRole = Teacher.teacherObj.filter(user_id = userId)
#             if teacherRole:
#                 file_obj = request.FILES.get('0')
#                 cid = request.POST.get('cid')

#                 #新建老师认证数据
#                 if cid == "1":
#                     models.authenticate.objects.create(
#                         teacherLicense=file_obj
#                     )
#                     obj = authenticate.objects.last()
#                     obj.teacherStatus = 1
#                 elif cid == "2":
#                     models.authenticate.objects.create(
#                         studentLicense=file_obj
#                     )
#                     obj = authenticate.objects.last()
#                     obj.studentStatus = 1
#                 elif cid == "3":
#                     models.authenticate.objects.create(
#                         idCard=file_obj
#                     )
#                     obj = authenticate.objects.last()
#                     obj.idStatus = 1
#                 elif cid == "4":
#                     models.authenticate.objects.create(
#                         EnglishLevel=file_obj
#                     )
#                     obj = authenticate.objects.last()
#                     obj.EnglishStatus = 1
#                 elif cid == "5":
#                     models.authenticate.objects.create(
#                         Else=file_obj
#                     )
#                     obj = authenticate.objects.last()
#                     obj.ElseStatus = 1

#                 teacherRole[0].authenticate_id = obj.id     #老师模型与老师认证模型关联起来
#                 obj.save()
#                 teacherRole[0].save()
#         return render(request, 'authenticate.html', {"obj": obj})



def findPW(request):
    if request.method == "POST":
        step = int(request.POST.get("step",0))
        step += 1
        return render(request,'findPW.html',{"step":step})
    else:
        step = int(request.GET.get("step",0))
        step += 1
        return render(request,'findPW.html',{"step":step})



def getVerificationCode(request):  #生成图片验证码
    import random
    import io
    from PIL import ImageDraw,ImageFont,Image
    def createcolor():
        red=random.randint(0,255)
        green=random.randint(0,255)
        blue=random.randint(0,255)
        return (red,green,blue)
    image=Image.new("RGB",(120,42),createcolor())
    imageDraw=ImageDraw.Draw(image,"RGB")
    imageFont=ImageFont.truetype("DejaVuSans.ttf",size=35)
    charsource="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    sum = ""
    for i in range(4):
        ch=random.choice(charsource)
        imageDraw.text((15+i*20,0),ch,fill=createcolor(),font=imageFont)
        sum+=ch
    request.session["verCode"]=sum
    for i in range(300):
        x = random.randint(0,120)
        y = random.randint(0, 42)
        imageDraw.point((x,y),fill=createcolor())
    byteIO=io.BytesIO()
    image.save(byteIO,"png")
    return  HttpResponse(byteIO.getvalue(),"image/png")