from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.personal, name=""),
    # path('test/', views.test),
    path('conversation/', views.conversation),
    path('post/', views.post),
    path('file/', views.file),  # 对应文件共享页面，需要在地址中传参数格式?classId=1
    path('filePost/', views.filePost, name="filePost"),  # 用于处理文件请求
    path('chat/', views.chat),
    path('logout/', views.logout),
]
