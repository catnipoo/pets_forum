from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from apps.trends.models import ImgInfo, Trends, Commit
# 首页显示
from apps.users.models import User


class IndexView(View):
    def get(self,request):
        return render(request,'index.html')
# 推荐页显示
class TrendsView(LoginRequiredMixin,View):
    def get(self,request):
        trends = Trends.objects.all().order_by('-create_time')
        for i in trends:
            i.create_time = str(i.create_time)[0:16]
        context = {
            'trends':trends
        }
        return render(request,'trends.html',context=context)

class DetailView(View):
    def get(self,request,trend_id):
        trend = Trends.objects.get(id=trend_id)
        time = str(trend.create_time)[0:10]
        images = ImgInfo.objects.filter(trends_id_id=trend_id)
        author = User.objects.get(id=trend.user_id_id)
        len_img = ImgInfo.objects.filter(trends_id_id=trend_id).count()
        len_imgs = [i+1 for i in range(len_img)]
        commit_list = Commit.objects.filter(trends_id_id=trend_id).order_by('-create_time')
        # commit_count = Commit.objects.filter(trends_id_id=trend_id).count()
        # keys = [str(i+1) for i in range(commit_count)]
        # commits = {}
        print('+++++++++++++++++')
        # print(commits)
        for i in commit_list:
            i.create_time = str(i.create_time)[0:16]
        context = {
            'trend':trend,
            'images':images,
            'author':author,
            'len_img':len_imgs,
            'time':time,
            'commits':commit_list
        }
        return render(request,'detail.html',context=context)



class UploadView(View):
    def post(self,request):
        trends = Trends.objects.get(id=1)
        # print('========'+trends)
        for i in request.FILES.getlist('images'):
            img = ImgInfo()
            img.img = i
            img.trends_id = trends
            img.save()
        imgs = ImgInfo.objects.all()
        content = {
            'imgs': imgs,
        }
        return render(request, 'show.html', content)
        # return render(request,'show.html')
class ShowView(View):
    def get(self,request):
        imgs = ImgInfo.objects.all()
        content = {
            'imgs':imgs,
        }
        print(content)
        return render(request,'show.html',content)
