# urls.py
from django.urls import path
from .views import OCRView

urlpatterns = [
    path('image_result/', OCRView.as_view(), name='ocr_view'),
]
