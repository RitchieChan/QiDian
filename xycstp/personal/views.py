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


def personal(request):
    if request.method == "GET":
        account = request.session.get('account', None)  # 取出登陆时session存的account
        # account = request.GET.get('account',None)
        if account == None:
            return redirect('/account/login/')
        users = User.userObj.filter(account=account)
        if users:
            userId = users[0].id
            teacherRole = Teacher.teacherObj.filter(user_id=userId)
            studentRole = Student.studentObj.filter(user_id=userId)
            if teacherRole:

                #老师认证
                auth_obj = authenticate.objects.get(pk=teacherRole[0].authenticate_id)
                file_obj = request.FILES.get('0')
                cid = request.POST.get('cid')
                if cid == "1":
                    auth_obj.teacherLicense = file_obj
                    auth_obj.teacherStatus = 1
                elif cid == "2":
                    auth_obj.studentLicense = file_obj
                    auth_obj.studentStatus = 1
                elif cid == "3":
                    auth_obj.idCard = file_obj
                    auth_obj.idStatus = 1
                elif cid == "4":
                    auth_obj.EnglishLevel = file_obj
                    auth_obj.EnglishStatus = 1
                elif cid == "5":
                    auth_obj.Else = file_obj
                    auth_obj.ElseStatus = 1
                auth_obj.save()

                teacherId = teacherRole[0].id
                teachingClass = Class.objects.filter(teacher_id=teacherId)
                studentUser = []
                students = []
                for course in teachingClass:
                    relations = Relation.objects.filter(
                        belong_class_id=course.id)
                    for relation in relations:
                        userId1 = Student.studentObj.get(
                            id=relation.student_id).user_id
                        studentUser.append(User.userObj.get(id=userId1))
                studentUser = set(studentUser)
                chatData = []
                for stuUser in studentUser:
                    messages = Conversation.converObj.filter(
                        Q(sender_id=users[0].id, receiver_id=stuUser.id) | Q(sender_id=stuUser.id, receiver_id=users[0].id))
                    lastMessage = messages.last()
                    chatData.append((stuUser, messages, lastMessage))
                return render(request, 'personalTeacher.html', {"Class": teachingClass, "user": users[0], "chatData": chatData, "obj": auth_obj})
            elif studentRole:
                student = studentRole[0]
                Classes = student.belongClass.all()
                teacherUser = []
                for course in Classes:
                    teacherId = course.teacher_id
                    userId1 = Teacher.teacherObj.get(id=teacherId).user_id
                    teacherUser.append(User.userObj.get(id=userId1))
                return render(request, 'personalStudent.html', {"Class": Classes, "user": users[0], "teachers": teacherUser})
        else:
            account = request.session.get(
                'account', None)  # 取出登陆时session存的account
    elif request.method == "POST":
        account = request.session.get('account', None)  #取出登陆时session存的account
        # account = request.GET.get('account',None)
        if account == None:
            return redirect('/account/login/')
        users = User.userObj.filter(account = account)
        if users:
            userId = users[0].id
            teacherRole = Teacher.teacherObj.filter(user_id = userId)
            if teacherRole:

                #老师认证
                auth_obj = authenticate.objects.get(pk=teacherRole[0].authenticate_id)
                file_obj = request.FILES.get('0')
                cid = request.POST.get('cid')
                if cid == "1":
                    auth_obj.teacherLicense = file_obj
                    auth_obj.teacherStatus = 1
                elif cid == "2":
                    auth_obj.studentLicense = file_obj
                    auth_obj.studentStatus = 1
                elif cid == "3":
                    auth_obj.idCard = file_obj
                    auth_obj.idStatus = 1
                elif cid == "4":
                    auth_obj.EnglishLevel = file_obj
                    auth_obj.EnglishStatus = 1
                elif cid == "5":
                    auth_obj.Else = file_obj
                    auth_obj.ElseStatus = 1
                auth_obj.save()

                return render(request,'personalTeacher.html',{"obj":auth_obj})


def get(request):
    if request.method == 'GET':
        sender = request.GET['sender']  # 获取sender 参数 对话的发送者
        receiver = request.GET['receiver']  # 获取 receiver参数 对话的接受者
        id_send = User.userObj.filter(userName=sender)[0].id  # 筛选在数据库中的ID
        id_receive = User.userObj.filter(userName=receiver)[0].id  # 筛选在数据库中的ID
        messages = Conversation.converObj.filter(
            Q(sender_id=id_receive, receiver_id=id_send) | Q(sender_id=id_send, receiver_id=id_receive))
        # 筛选对话者的数据
        return render(request, 'communication.html',
                      {'id_send': id_send, 'id_receive': id_receive, 'messages': messages})
        #   返回页面和页面所需要的的数据
    if request.method == 'POST':  # 还未编写
        return HttpResponse()


def conversation(request):  # 对话页面请求方法 因为方便测试原因就用了GET请求方式，需要在地址中传递sender和receiver参数
    if request.method == 'GET':
        sender = request.GET['sender']  # 获取sender 参数 对话的发送者
        receiver = request.GET['receiver']  # 获取 receiver参数 对话的接受者
        id_send = User.userObj.filter(userName=sender)[0].id  # 筛选在数据库中的ID
        id_receive = User.userObj.filter(userName=receiver)[0].id  # 筛选在数据库中的ID
        messages = Conversation.converObj.filter(
            Q(sender_id=id_receive, receiver_id=id_send) | Q(sender_id=id_send, receiver_id=id_receive))
        # 筛选对话者的数据
        return render(request, 'communication.html',
                      {'id_send': id_send, 'id_receive': id_receive, 'messages': messages})
        #   返回页面和页面所需要的的数据
    if request.method == 'POST':  # 还未编写
        return HttpResponse()


def post(request):  # 对话请求方法
    if request.method == 'POST':  # 判断是否是post方法，如果不是就返回错误
        post_type = request.POST.get('post_type')  # 接受页面传递的请求类型
        if post_type == 'get_chat':  # 判断是否获取对话的请求
            # 最后一条信息在数据库中的id，便于筛选新消息

            id_send = request.POST.get('id_send')  # 发送者ID
            send_data = request.POST.get("send_data")
            send_data = json.loads(send_data)
            print(id_send)
            dataList = []
            for data in send_data:
                id_receive = data['id_receive']  # 接受者者ID
                print(id_receive)
                if (data['last_chat_id']):
                    last_chat_id = int(data['last_chat_id'])
                else:
                    last_chat_id = 1

                messages = Conversation.converObj.filter(id__gt=last_chat_id).filter(
                    Q(sender_id=id_receive, receiver_id=id_send) | Q(sender_id=id_send, receiver_id=id_receive))
            # # 筛选需要的数据
                tempData = []
                for message in messages:
                    if message:
                        tempData.append((message.text,
                                         message.receiver_id, message.id, message.createTime))  # 所需数据用列表储存
                if tempData:
                    dataList.append(tempData)
            return JsonResponse(dataList, safe=False)  # 返回数据
            # return HttpResponse("as")
        if post_type == 'send_chat':  # 判断是否发送对话的请求
            text = request.POST.get('text')
            id_send = int(request.POST.get('id_send'))
            id_receive = int(request.POST.get('id_receive'))
            send_user = User.userObj.get(pk=id_send)
            receive_user = User.userObj.get(pk=id_receive)
            conversation = Conversation.converObj.createConver(
                text, send_user, receive_user)
            conversation.save()  # 获取发送消息的基本信息，保存在数据库中
            return HttpResponse()
    else:
        return HttpResponse('404error')


def file(request):  # 文件页面请求方法 ，需要在地址中传递authorityId参数
    classId = request.GET['classId']  # 接受id参数 用于筛选对应文件库文件
    filePath = FilePath.fpObj.filter(belong_class_id=classId)  # 获取路径对象集合
    return render(request, 'file.html', {'classId': classId, 'filePath': filePath})
#   返回页面和页面所需要的的数据


def filePost(request):  # 文件请求方法 与对话请求方法思想基本相同
    if request.method == "POST":
        postType = request.POST.get('postType')
     # 判断请求的类型
        if postType == 'loadFile':  # 对应上传文件类型 通过form表单上传
            classId = request.POST.get('classId')
            f = request.FILES['file']  # 获取文件
            course = Class.objects.get(
                pk=classId)  # 获取文件对应的文件库权限
            visitpath = 'http://ucwxb.xyz/static/upFiles/'+f.name  # 拼接形成文件在页面中的下载路径
            fp = FilePath.fpObj.createFilePath(
                f.name, visitpath, course)  # 创建对象
            fp.save()  # 保存文件路径
            filepath = os.path.join(settings.MEDIA_ROOT, f.name)  # 拼接文件储存路径
            with open(filepath, 'wb') as fp:  # 将文件写入储存路径
                for info in f.chunks():
                    fp.write(info)
            return redirect('/personal/file/?classId=' + classId)
            # 此处因为我不会用ajax传递文件...所以采用了表单传递文件，因此用了重定向跳转到原页面

        if postType == 'get_file':  # 获取文件 与获取对话思路相同
            lastFileId = int(request.POST.get('lastFileId'))
            authorityId = request.POST.get('classId')
            info = FilePath.fpObj.filter(
                id__gt=lastFileId).filter(belong_class_id=classId)
            data = []
            for inf in info:
                data.append((inf.name, inf.path,
                             inf.belong_class_id, inf.createTime))
            return JsonResponse(data, safe=False)

    else:
        return HttpResponse("404ERROR")


def chat(request):
    return render(request, 'chat.html')


def logout(request):
    del request.session['account']
    return redirect('/account/login/')
