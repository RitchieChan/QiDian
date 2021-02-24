from django.contrib import admin

# Register your models here.
# from .models import User, Conversation, FileAuthority


from .models import *
from .myparser import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['account', 'phoneNum',
                    'userName', 'passWord', 'email', 'isDelete']


@admin.register(authenticate)
class authenticatepythonAdmin(admin.ModelAdmin):
    list_display = ['teacherLicense', 'teacherStatus',
                    'studentLicense', 'studentStatus',  'idStatus', 'EnglishLevel', 'EnglishStatus',  'ElseStatus']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', ]


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['student', 'belong_class', ]


class TargetGradeSubjectInfo(admin.TabularInline):
    model = TargetGradeSubject
    extra = 2


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = [TargetGradeSubjectInfo]

    list_display = ['user', 'show_TargetStu']

    # 修改后没有了getStudents()的方法故删去此展示
    # def show_students(self, obj):
    #     stus = obj.getStudents()
    #     stuUserNames = [stu.userName for stu in stus]
    #     return stuUserNames

    def show_TargetStu(self, obj):
        targetStus = obj.tags.all()
        output = []
        for targetStu in targetStus:
            OneStr = "*"
            OneStr += LEVELMap[targetStu.LEVEL] + " "
            OneStr += GradeMap[targetStu.GradeStart] + \
                "~" + GradeMap[targetStu.GradeEnd] + " "
            OneStr += targetStu.SubjectsData
            output.append(OneStr)
        return output


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user',  'show_Need', 'show_isNeedTeacher']
# 'show_teachers',
    # def show_teachers(self, obj):
    #     return [tea.userName for tea in obj.teachers.all()]
    # filter_horizontal = ('teachers',)

    def show_Need(self, obj):
        return obj.detailInfo.NeedWhatTeacher

    def show_isNeedTeacher(self, obj):
        return obj.detailInfo.isNeedTeacher


@admin.register(TeacherDetail)
class TeacherDetailAdmin(admin.ModelAdmin):
    def show_basic(self, obj):
        basic = obj.relatedTeacher
        return basic.user.userName

    list_display = ['age', 'gender', 'major',
                    'education', 'experience', 'VedioCenter', 'introduction',
                    'headSculpture', 'show_basic']


@admin.register(StudentDetail)
class StudentDetailAdmin(admin.ModelAdmin):
    def show_basic(self, obj):
        basic = obj.relatedStudent
        return basic.user.userName

    list_display = ['age', 'gender', 'introduction', 'grade',
                    'headSculpture', 'show_basic']


@admin.register(TargetGradeSubject)
class TargetGradeSubjectAdmin(admin.ModelAdmin):
    def gradestart(self, obj):
        return GradeMap[obj.GradeStart]

    def gradeend(self, obj):
        return GradeMap[obj.GradeEnd]
    list_display = ['LEVEL', 'gradestart', 'gradeend', 'SubjectsData']


class ConverAdmin(admin.ModelAdmin):

    list_display = ['text', 'sender', 'receiver',
                    'createTime', 'isDelete']
    list_filter = ['text']
    search_fields = ['text']
    list_per_page = 5


# class UserFileAuthorityAdmin(admin.ModelAdmin):

#     list_display = ['fileUser', 'fileAuthority', ]
#     list_per_page = 5


# class FileAuthorityAdmin(admin.ModelAdmin):

#     list_display = ['creater',  'isDelete', ]
#     list_filter = ['creater']
#     search_fields = ['creater']
#     list_per_page = 5


# class UserFileAuthority(models.Model):
#     fileUser = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='fileUser')
#     fileAuthority = models.ForeignKey(
#         FileAuthority, on_delete=models.CASCADE, related_name='fileAuthority')
# class FileAuthority(models.Model):
#     creater = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='creater')
#     isDelete = models.BooleanField(default=False)
#     fileUser = models.ManyToManyField(User, through='UserFileAuthority')
# admin.site.register(User, UserAdmin)
admin.site.register(Conversation, ConverAdmin)
# admin.site.register(FileAuthority, FileAuthorityAdmin)
