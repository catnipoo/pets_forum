from django.conf.urls import url,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #登录
url(r'^login/$',views.LoginView.as_view()),
    #注册
url(r'^register/$',views.RegisterView.as_view()),
#退出
url(r'^logout/$',views.LogOutView.as_view(),name='logout'),
url(r'^userinfo/$',views.UserinfoView.as_view(),name='info'),
url(r'^userbaseinfo/$',views.UserbaseinfoView.as_view(),name='baseinfo'),
url(r'^userpic/$',views.UserpicView.as_view()),
url(r'^userpass/$',views.UserpassView.as_view()),
url(r'^userfollow/$',views.UserfollowView.as_view()),
url(r'^userfans/$',views.UserfansView.as_view()),
url(r'^usertrends/$',views.UsertrendsView.as_view()),
url(r'^relase/$',views.RelaseView.as_view()),
url(r'^userbaseinfo/$',views.UserbaseinfoView.as_view()),
url(r'^personinfo/(?P<user_id>\d+)/$',views.PersoninfoView.as_view()),
# 判断用户名是否重复
url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',views.UsernameCountView.as_view()),
# 判断手机是否重复
url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$',views.MobileCountView.as_view()),

url(r'^emails/verification/$', views.EmailVerifyView.as_view(), name="verify"),
]