from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.job_list, name='job-list'),
    path('resumes/upload/', views.resume_upload, name='resume-upload'),
    path('applications/', views.apply_for_job, name='apply-for-job'),
    path('my-applications/',views.my_applications,name='my-applications'),
    path('applications/<int:pk>/status/',views.update_application_status,name='update-application-status'),
]
