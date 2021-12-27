from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required



app_name = 'RNC'

urlpatterns = [
    #path('upload/',views.upload_excel_meas, name='upload_excel_meas'),
    path('',views.RNC.as_view(),name='home'),
    path('<int:pk>/',views.RNC_DetailViews.as_view(),name='detail'),
    path('create/',views.RNC_CreateView.as_view(),name='create'),
    path('<pk>/update/',views.RNC_UpdateView.as_view(),name='update'),
    path('<pk>/delete/',views.RNC_DeleteView.as_view(),name='delete'),
    ]  


# urlpatterns = [
#     #path('upload/',views.upload_excel_meas, name='upload_excel_meas'),
#     path('',login_required(views.RNC.as_view()),name='home'),
#     path('<int:pk>/',login_required(views.RNC_DetailViews.as_view()),name='detail'),
#     path('create/',login_required(views.RNC_CreateView.as_view()),name='create'),
#     path('<pk>/update/',login_required(views.RNC_UpdateView.as_view()),name='update'),
#     path('<pk>/delete/',login_required(views.RNC_DeleteView.as_view()),name='delete'),
#     ]  
