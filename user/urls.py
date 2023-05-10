from . import views
from django.urls import path


urlpatterns = [
    path('', views.hello, name='hello'),
    path('create', views.create, name='create'),
    path('send', views.send, name='send'),
    path('accept', views.accept, name='accept'),
    path('reject', views.reject, name='reject'),
    path('delete', views.delete, name='delete'),
    path('outgoing', views.outgoing, name='outgoing'),
    path('incoming', views.incoming, name='incoming'),
    path('friend', views.friend, name='friend'),
    path('status', views.status, name='status'),
]
