from django.urls import path
from pdf_ai import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
]
