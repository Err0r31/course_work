from django.contrib import admin
from django.urls import path, include
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),  
    path('accounts/', include('accounts.urls')),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)