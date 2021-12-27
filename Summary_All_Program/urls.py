from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'Summary_All_Program'

urlpatterns = [
    #path('upload/',views.upload_excel_meas, name='upload_excel_meas'),
    path('',views.Summary_All_Program.as_view(),name='home'),
    path('<int:pk>/',views.Summary_All_Program_DetailViews.as_view(),name='detail'),
    path('create/',views.Summary_All_Program_CreateView.as_view(),name='create'),
    path('<pk>/update/',views.Summary_All_Program_UpdateView.as_view(),name='update'),
    path('<pk>/delete/',views.Summary_All_Program_DeleteView.as_view(),name='delete'),
    
    path('filter/',views.SAP_Filter_List_View.as_view(),name='homef'),
    path('filter/<int:pk>/',views.SAP_Filter_DetailViews.as_view(),name='detailf'),
    path('filter/create/',views.SAP_Filter_CreateView.as_view(),name='createf'),
    path('filter/<pk>/update/',views.SAP_Filter_UpdateView.as_view(),name='updatef'),
    path('filter/<pk>/delete/',views.SAP_Filter_DeleteView.as_view(),name='deletef'),
    path('Filter_Processing/',views.SAP_Filter_Processing.as_view(),name='SAPF_Processingf'),
    ]  

"""
    path('summary_all_program/',views.summary_all_program_form.as_view(),name='summary_all_program'),
    path('no_curr/',views.network_overview_curr.as_view(),name='no_curr'),
"""
# urlpatterns = [
#     #path('upload/',views.upload_excel_meas, name='upload_excel_meas'),
#     path('',login_required(views.Summary_All_Program.as_view()),name='home'),
#     path('<int:pk>/',login_required(views.Summary_All_Program_DetailViews.as_view()),name='detail'),
#     path('create/',login_required(views.Summary_All_Program_CreateView.as_view()),name='create'),
#     path('<pk>/update/',login_required(views.Summary_All_Program_UpdateView.as_view()),name='update'),
#     path('<pk>/delete/',login_required(views.Summary_All_Program_DeleteView.as_view()),name='delete'),
    
#     path('filter/',login_required(views.SAP_Filter_List_View.as_view()),name='homef'),
#     path('filter/<int:pk>/',login_required(views.SAP_Filter_DetailViews.as_view()),name='detailf'),
#     path('filter/create/',login_required(views.SAP_Filter_CreateView.as_view()),name='createf'),
#     path('filter/<pk>/update/',login_required(views.SAP_Filter_UpdateView.as_view()),name='updatef'),
#     path('filter/<pk>/delete/',login_required(views.SAP_Filter_DeleteView.as_view()),name='deletef'),
#     path('Filter_Processing/',login_required(views.SAP_Filter_Processing.as_view()),name='SAPF_Processingf'),
#     ]  