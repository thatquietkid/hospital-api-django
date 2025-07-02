# core/urls.py
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import health_check, welcome

urlpatterns = [
    path('health/', health_check, name='health'),
    path('', welcome, name='welcome'),
    path('signup/', views.SignupView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('patients/', views.PatientListCreateView.as_view()),
    path('patients/records/add', views.AddMedicalRecordView.as_view()),
    path('patients/<int:id>/records/', views.PatientMedicalRecordsView.as_view()),
]
