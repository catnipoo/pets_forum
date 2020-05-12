from django import http

import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from pymysql import DatabaseError

from apps.trends.models import Channel, Trends, ImgInfo
from apps.users.models import User, UserRelation
from pets_forum.settings import logger
from utils.secret import SecretOauth

class FollowView(View):
    def get(self,request,user_id):
        user = request.user
        person = User.objects.get(id=user_id)
        user_rel = UserRelation.objects.create(target_user=person.id,user_id=user,status=1)
        user_rel.save()
        ste = '/personinfo/' + user_id + '/'
        return redirect(ste)

class UnFollowView(View):
    def get(self,request,user_id):
        user = request.user
        person = User.objects.get(id=user_id)
        user_rel = UserRelation.objects.filter(target_user=person.id,user_id=user,status=1).delete()
        ste = '/personinfo/' + user_id + '/'
        return redirect(ste)

class RelaseView(View):
    def get(self,request):
        channels = Channel.objects.all()
        context = {
            'channels':channels
        }
        return render(request,'relase.html',context=context)
    def post(self,request):
        user_id = request.user.id
        title = request.POST.get('title')
        content = request.POST.get('content')
        channel = request.POST.get('category')
        trends = Trends.objects.create(title=title,user_id_id=user_id,content=content,channel_id_id=channel)
        print('______________+++++++++')
        print(trends)
        images = request.FILES.getlist('images')
        for i in images:
            img = ImgInfo()
            img.img = i
            img.trends_id = trends
            img.save()
        return render(request,'user_trends_list.html')



class UsertrendsView(View):
    def get(self,request):
        user = request.user.id
        trends = Trends.objects.filter(user_id_id=user).order_by('-create_time')
        for i in trends:
            time = str(i.create_time).split(' ')[0]
            i.time = time
        context = {
            'trends':trends
        }
        return render(request,'user_trends_list.html',context=context)


class PersoninfoView(View):
    def get(self,request,user_id):
        person = User.objects.get(id=user_id)
        trends = Trends.objects.filter(user_id_id=user_id)
        user_rel = UserRelation.objects.filter(user_id=request.user).filter(target_user=user_id).count()
        for i in trends:
            i.create_time = str(i.create_time)[0:16]
        context = {
            'person':person,
            'trends':trends,
            'user_rel':user_rel
        }
        return render(request,'person_info.html',context)



class UserpassView(View):
    def get(self,request):
        return render(request,'user_pass_info.html')

class UserfollowView(View):
    def get(self,request):
        user_fol = UserRelation.objects.filter(user_id=request.user)
        user_list = []
        for i in user_fol:
            u = User.objects.get(id=i.target_user)
            user_list.append(u)
        context = {
            'user_fol':user_fol,
            'user_list':user_list
        }
        return render(request,'user_follow.html',context)

class UserfansView(View):
    def get(self,request):
        user_fan = UserRelation.objects.filter(target_user=request.user.id)
        user_list = []
        for i in user_fan:
            u = User.objects.get(id=i.user_id_id)
            user_list.append(u)
        context = {
            'user_fan': user_fan,
            'user_list': user_list
        }
        return render(request,'user_fans.html',context)

class UserpicView(View):
    def get(self,request):
        return render(request,'user_pic_info.html')
    def post(self,request):
        user = request.user
        avatar = request.FILES.get('avatar')
        user.default_image = avatar
        user.save()
        context = {
            'user':user
        }
        return redirect(reverse('users:baseinfo'))
class UserbaseinfoView(View):
    def get(self,request):
        user = request.user
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
            'default_image': request.user.default_image,
            'user':user
        }
        print('*************')
        print(context)
        return render(request,'user_base_info.html',context=context)

class MobileCountView(View):
    def get(self, request, mobile):
        # 1.接收参数


        # 2.校验 是否为空 正则

        # 3.务逻辑判断-- 数据库有没有--返回count
        count = User.objects.filter(mobile=mobile).count()

        # 4.返回响应对象
        return http.JsonResponse({'code': 200, 'errmsg': 'OK', 'count': count})


# 2.判断用户名是否重复
class UsernameCountView(View):
    def get(self, request, username):
        # 1.接收参数

        # 2.校验 是否为空 正则

        # 3.务逻辑判断-- 数据库有没有--返回count
        count = User.objects.filter(username=username).count()

        # 4.返回响应对象
        return http.JsonResponse({'code': 200, 'errmsg': 'OK', 'count': count})


class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        username = request.POST.get('name')
        password = request.POST.get('pass')
        # 2.校验参数
        if not all([username, password]):
            return http.HttpResponseForbidden('参数不齐全')
        # 2.1 用户名
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 2.2 密码
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')

        # 3.验证用户名和密码--django自带的认证
        from django.contrib.auth import authenticate, login
        user = authenticate(username=username, password=password)

        if user is None:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})

        # 保持登登录状态login()
        login(request, user)

        # 操作 next
        next = request.GET.get('next')

        if next:
            response = redirect(next)
        else:
            response = redirect(reverse('trends:index'))

        # 存用户名到 cookie 里面去
        response.set_cookie('username', user.username, max_age=1 * 24 * 3600)

        # 5.跳转到首页
        return response

class RegisterView(View):
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('repassword')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        if not all([username, password, password2,email, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('参数email有误')

        try:
            user = User.objects.create_user(username=username, password=password, email=email ,mobile=mobile)
        except DatabaseError:
            return render(request, 'login.html', {'register_errmsg': '注册失败'})

        from django.contrib.auth import login
        login(request, user)
        return redirect(reverse('trends:index'))


class LogOutView(View):
    def get(self, request):
        from django.contrib.auth import logout
        logout(request)
        response = redirect(reverse('trends:index'))
        response.delete_cookie('username')
        return response

class UserinfoView(LoginRequiredMixin,View):
    def get(self,request):
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
            'default_image':request.user.default_image
        }
        return render(request, 'user.html', context=context)

class EmailVerifyView(LoginRequiredMixin,View):
    def get(self,request):
        # 1.接收参数  request.GET
        token = request.GET.get('token')

        # 解密
        data_dict = SecretOauth().loads(token)

        user_id = data_dict.get('user_id')
        email = data_dict.get('email')

        # 2.校验
        try:
            user = User.objects.get(id=user_id, email=email)
        except Exception as e:
            print(e)
            return http.HttpResponseForbidden('token无效的!')

        # 3. 修改 email_active
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('激活邮件失败')

        # 4. 返回
        return redirect(reverse('users:info'))