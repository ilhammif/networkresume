from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required



app_name = 'Network_Overview_Current'

urlpatterns = [
    #path('upload/',views.upload_excel_meas, name='upload_excel_meas'),
    path('',views.Network_Overview_Current.as_view(),name='home'),
    path('<int:pk>/',views.Network_Overview_Current_DetailViews.as_view(),name='detail'),
    path('create/',views.Network_Overview_Current_CreateView.as_view(),name='create'),
    path('<pk>/update/',views.Network_Overview_Current_UpdateView.as_view(),name='update'),
    path('<pk>/delete/',views.Network_Overview_Current_DeleteView.as_view(),name='delete'),
    ]  


# urlpatterns = [
#     #path('upload/',views.upload_excel_meas, name='upload_excel_meas'),
#     path('',login_required(views.Network_Overview_Current.as_view()),name='home'),
#     path('<int:pk>/',login_required(views.Network_Overview_Current_DetailViews.as_view()),name='detail'),
#     path('create/',login_required(views.Network_Overview_Current_CreateView.as_view()),name='create'),
#     path('<pk>/update/',login_required(views.Network_Overview_Current_UpdateView.as_view()),name='update'),
#     path('<pk>/delete/',login_required(views.Network_Overview_Current_DeleteView.as_view()),name='delete'),
#     ]  
