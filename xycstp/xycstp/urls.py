from django.contrib import admin
from django.urls import path,include
from  errPage import views


#对应static
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  #主页
    path('account/', include('account.urls')), #账号，包括登陆注册找回密码
    path('personal/',include('personal.urls')),  #学生个人中心，包括显示个人信息，文件共享，聊天
    path('findTutor/', include('findTutor.urls')),   #找老师
    path('bbs/', include('bbs.urls')),  #论坛
    path('train/', include('train.urls')),  #题库
    path('manager/', include('manager.urls')),  #老师认证后台管理

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  #如果单纯的是上传，文件并不用来显示或者读取，就不用加这个


handler404 = views.page_not_found