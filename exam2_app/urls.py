from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('registerpage', views.registerpage),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('add_jobs_page', views.add_jobs_page),
    path('add_a_job', views.add_a_job),
    path('cancel', views.cancel),
    path('job_info/<id>', views.job_info),
    path('delete/<id>', views.delete),
    path('edit_jobs_page/<id>', views.edit_jobs_page),
    path('edit/<id>', views.edit),
    path('add_to_myjob/<id>',views.add_to_myjob),
    path('remove_from_myjob/<id>', views.remove_from_myjob)
    
]