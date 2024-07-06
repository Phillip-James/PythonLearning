"""为app： accounts定义url模式"""

from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    #包含默认身份验证URL
    path('', include ('django.contrib.auth.urls')),
    #注册页面
    path('register/', views.register, name='register'),
]