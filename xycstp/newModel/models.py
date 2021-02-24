from enum import IntEnum, unique
from django.db import models
from .myparser import *
from abc import ABCMeta, abstractmethod
# Create your models here.


class UserManager(models.Manager):  # 用户管理类 可以用来创建用户和返回未被删除用户
    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(isDelete=False)

    def createUser(self, account, phoneNum, userName, password, email):  # 用于创建用户
        #
        user = self.model()
        user.account = account
        user.phoneNum = phoneNum
        user.userName = userName
        user.password = password
        user.email = email
        # user.isTeacher = isTeacher
        return user

# User表是老师表和学生表的公共基表


class User(models.Model):
    # 用户类字段
    # 账号
    userObj = UserManager()
    account = models.CharField(max_length=15)
    # 手机号
    phoneNum = models.CharField(max_length=20)
    # 昵称
    userName = models.CharField(max_length=20)
    # 密码
    passWord = models.CharField(max_length=20)
    # 邮箱
    email = models.CharField(max_length=20)
    # 是否删除
    isDelete = models.BooleanField(default=False)

    def __str__(self):  # 后台返回学生名字
        return self.userName


# 用户详细信息类，是学生详细信息表和老师详细信息表的公共基表,暂时设计为抽象表
class UserDetailInfo(models.Model):
    # 年龄
    age = models.IntegerField(blank=True, null=True)
    # 性别 True为男，False为女
    gender = models.BooleanField(default=True, blank=True, null=True)
    # 自我介绍（个性签名）
    introduction = models.CharField(max_length=50, blank=True, null=True)
    # 头像
    headSculpture = models.ImageField(blank=True, null=True)
    # 地址
    address = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        abstract = True

    def getGender(self):
        if self.gender == True:
            return "男"
        else:
            return "女"


class StudentDetail(UserDetailInfo):
    # 学生详细信息专属字段
    # 年级(设计为整数型是为了用paser.py里面的那套解析方案)
    grade = models.IntegerField(blank=True, null=True)
    # 是否需要老师
    isNeedTeacher = models.BooleanField(default=True, blank=True, null=True)
    # 老师需求
    NeedWhatTeacher = models.CharField(max_length=50, blank=True, null=True)
    # relatedStudent相关联的学生(一对一绑定到学生对象)
    relatedStudent = models.OneToOneField(
        "Student", on_delete=models.CASCADE, related_name="detailInfo")

    def getGrade(self):
        return GradeMap[self.grade]


class TeacherDetail(UserDetailInfo):
    # 老师详细信息专属字段
    # 大学专业
    major = models.CharField(max_length=20, blank=True, null=True)
    # 就读或毕业的大学
    education = models.CharField(max_length=20, blank=True, null=True)
    # 教学经验
    experience = models.CharField(max_length=100, blank=True, null=True)
    # 个人视频中心链接
    VedioCenter = models.CharField(max_length=50, blank=True, null=True)
    # relatedTeacher相关联的老师(一对一绑定到老师对象)
    relatedTeacher = models.OneToOneField(
        "Teacher", on_delete=models.CASCADE, related_name="detailInfo")
    
   
   


# 老师类管理器
class TeacherManager(models.Manager):
    def get_queryset(self):
        return super(TeacherManager, self).get_queryset().filter(user__isDelete=False)


# 老师表，内含user字段与用户表一对一
class Teacher(models.Model):
    # 重写老师查询器
    teacherObj = TeacherManager()

    # user字段
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, related_name="teacher")
    # 老师表的特殊字段
    # 老师详细信息(通过关键字与老师详细信息相关联)detailInfo
    # 通过学生关联老师，老师通过字段students.all()可以获得学生查询集
    # teacher的隐含属性，可以用.tags.all()获得挂载在老师对象上的所有擅长学科标签


    #认证
    authenticate = models.OneToOneField("authenticate", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.userName

    # 获得相应的学生（查询集）
    # def getStudents(self):
    #     return self.students.all()

# 学生类管理器


class StudentManager(models.Manager):
    def get_queryset(self):
        return super(StudentManager, self).get_queryset().filter(user__isDelete=False)

# 学生表，内含user字段与用户表一对一


class Student(models.Model):
    # 重写学生查询器
    studentObj = StudentManager()

    # user字段
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, related_name="student")
    # 学生表的特殊字段(通过关键字与学生详细信息相关联)detailInfo
   
    belongClass = models.ManyToManyField(
        "Class", related_name="belongClass", blank=True,through="Relation")

    # 此处将学生和课程多对多绑定

    def __str__(self):
        return self.user.userName

    # 获得相应的老师（查询集）
    # def getTeachers(self):
    #     return self.teachers.all()


class TargetGradeSubject(models.Model):
    LEVEL = models.IntegerField(blank=True, null=True)
    # 用年级的代号始末来代表年级范围
    GradeStart = models.IntegerField(blank=True, null=True)
    GradeEnd = models.IntegerField(blank=True, null=True)
    # 在SubjectsData中直接用字符串（中文）来表示学科，学科之间用空格间隔
    # 如： "语文 数学 英语 物理"
    SubjectsData = models.CharField(max_length=40, default="")
    # 相关联的老师
    relatedTeacher = models.ForeignKey(
        "Teacher", on_delete=models.CASCADE, related_name="tags")
    # 获得年级开始的序号代表的中文意思

    def GradeStartToChinese(self):
        return GradeMap[self.GradeStart]
    # 获得年级结束的序号代表的中文意思
    # 如1~3表示一年级~三年级

    def GradeEndToChinese(self):
        return GradeMap[self.GradeEnd]
    # 获得学科列表

    def getSubjectList(self):
        return self.SubjectsData.split()

# 将学生和老师联系在一起


# def connectTeacherStudent(teacher, student):
#     student.teachers.add(teacher)

class Class(models.Model):  
    name =models.CharField(max_length=40, default="")
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='course')  
# 课程类，与老师多对一绑定

class Relation(models.Model):  # 中间模型 此处为了方便测试创建了学生与课程的中间模型，可以去除
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='relation') 
    belong_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='relation')  




class ConverManager(models.Manager):  # 对话管理类 可以用来创建用户和返回未被删除对话
    def get_queryset(self):
        return super(ConverManager, self).get_queryset().filter(isDelete=False)

    def createConver(self, text, sender, receiver):  # 用于创建对话

        conversation = self.model()
        conversation.text = text
        conversation.sender = sender
        conversation.receiver = receiver
        return conversation


class Conversation(models.Model):
    # 对话管理对象
    converObj = ConverManager()
    # 对话内容
    text = models.CharField(max_length=200, db_column='text')
    # 发送者 和用户类绑定
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')

    # 收到者 和用户类绑定
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    # 是否删除
    isDelete = models.BooleanField(default=False)
    # 发送时间
    createTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # 后台返回学生名字
        return self.text




class FilePathManager(models.Manager):  # 文件路径管理类
    def get_queryset(self):
        return super(FilePathManager, self).get_queryset().filter(isDelete=False)

    def createFilePath(self, name, path, course):  # 用于创建文件路径对象

        filePath = self.model()
        filePath.name = name
        filePath.path = path
        filePath.belong_class = course
        return filePath


class FilePath(models.Model):  # 文件路径 储存共享文件的访问路径
    fpObj = FilePathManager()  # 创建管理对象
    name = models.CharField(max_length=50, db_column='name')  # 文件名
    path = models.CharField(max_length=200, db_column='path')  # 访问路径
    isDelete = models.BooleanField(default=False)  # 是否删除
    createTime = models.DateTimeField(auto_now_add=True)  # 创建时间
    belong_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='belong_class')
    # 与课程绑定，用于区分文件属于哪个课程

    def __str__(self):  # 后台返回学生名字
        return self.name



#老师认证类
class authenticate(models.Model):
    teacherLicense = models.ImageField(upload_to='img', null=True)
    teacherStatus = models.IntegerField(default=0)

    studentLicense = models.ImageField(upload_to='img', null=True)
    studentStatus = models.IntegerField(default=0)

    idCard = models.ImageField(upload_to='img', null=True)
    idStatus = models.IntegerField(default=0)

    EnglishLevel = models.ImageField(upload_to='img', null=True)
    EnglishStatus = models.IntegerField(default=0)

    Else = models.ImageField(upload_to='img', null=True)
    ElseStatus = models.IntegerField(default=0)