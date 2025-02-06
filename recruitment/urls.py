from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('answer_questions/<int:application_id>/', views.answer_questions, name='answer_questions'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('job-applications/<int:job_id>/', views.job_applications, name='job_applications'),
    path('create-job-offer/', views.create_job_offer, name='create_job_offer'),
    path('edit-job-offer/<int:job_id>/', views.edit_job_offer, name='edit_job_offer'),
    path('delete-job-offer/<int:job_id>/', views.delete_job_offer, name='delete_job_offer'),
    path('logout/', views.logout_view, name='logout'),
    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
    # Nueva ruta para descarga segura de CVs
    path('download-cv/<str:application_id>/', views.download_cv, name='download_cv'),
]