from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required



app_name = 'Meas'

urlpatterns = [
    #path('upload/',views.upload_excel_meas, name='upload_excel_meas'),
    path('',views.Meas.as_view(),name='home'),
    path('<int:pk>/',views.Meas_DetailViews.as_view(),name='detail'),
    path('create/',views.Meas_CreateView.as_view(),name='create'),
    path('<pk>/update/',views.Meas_UpdateView.as_view(),name='update'),
    path('<pk>/delete/',views.Meas_DeleteView.as_view(),name='delete'),
    ]  


# urlpatterns = [
#     #path('upload/',views.upload_excel_meas, name='upload_excel_meas'),
#     path('',login_required(views.Meas.as_view()),name='home'),
#     path('<int:pk>/',login_required(views.Meas_DetailViews.as_view()),name='detail'),
#     path('create/',login_required(views.Meas_CreateView.as_view()),name='create'),
#     path('<pk>/update/',login_required(views.Meas_UpdateView.as_view()),name='update'),
#     path('<pk>/delete/',login_required(views.Meas_DeleteView.as_view()),name='delete'),
#     ]  
