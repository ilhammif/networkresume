from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required



app_name = 'Site_Profile'

urlpatterns = [
    #path('upload/',views.upload_excel_meas, name='upload_excel_meas'),
    path('',views.Site_Profile.as_view(),name='home'),
    path('<int:pk>/',views.Site_Profile_DetailViews.as_view(),name='detail'),
    path('create/',views.Site_Profile_CreateView.as_view(),name='create'),
    path('<pk>/update/',views.Site_Profile_UpdateView.as_view(),name='update'),
    path('<pk>/delete/',views.Site_Profile_DeleteView.as_view(),name='delete'),
    ]  


# urlpatterns = [
#     #path('upload/',views.upload_excel_meas, name='upload_excel_meas'),
#     path('',login_required(views.Site_Profile.as_view()),name='home'),
#     path('<int:pk>/',login_required(views.Site_Profile_DetailViews.as_view()),name='detail'),
#     path('create/',login_required(views.Site_Profile_CreateView.as_view()),name='create'),
#     path('<pk>/update/',login_required(views.Site_Profile_UpdateView.as_view()),name='update'),
#     path('<pk>/delete/',login_required(views.Site_Profile_DeleteView.as_view()),name='delete'),
#     ]  
