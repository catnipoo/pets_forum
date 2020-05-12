from django.conf.urls import url,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
url(r'^$',views.IndexView.as_view(),name='index'),
url(r'^trends/$',views.TrendsView.as_view()),
url(r'^trendsdetail/(?P<trend_id>\d+)/$',views.DetailView.as_view()),
url(r'^upload/$',views.UploadView.as_view()),

url(r'^show/$',views.ShowView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)