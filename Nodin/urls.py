from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required



app_name = 'Nodin'

urlpatterns = [
    #path('upload/',views.upload_excel_meas, name='upload_excel_meas'),
    path('',views.Nodin.as_view(),name='home'),
    path('<int:pk>/',views.Nodin_DetailViews.as_view(),name='detail'),
    path('create/',views.Nodin_CreateView.as_view(),name='create'),
    path('<pk>/update/',views.Nodin_UpdateView.as_view(),name='update'),
    path('<pk>/delete/',views.Nodin_DeleteView.as_view(),name='delete'),
    ]  


# urlpatterns = [
#     #path('upload/',views.upload_excel_meas, name='upload_excel_meas'),
#     path('',login_required(views.Site_Profile.as_view()),name='home'),
#     path('<int:pk>/',login_required(views.Site_Profile_DetailViews.as_view()),name='detail'),
#     path('create/',login_required(views.Site_Profile_CreateView.as_view()),name='create'),
#     path('<pk>/update/',login_required(views.Site_Profile_UpdateView.as_view()),name='update'),
#     path('<pk>/delete/',login_required(views.Site_Profile_DeleteView.as_view()),name='delete'),
#     ]  
