from django.urls import path, re_path
from .views import ProductList, ProductDetail

urlpatterns = [
    path('', ProductList.as_view()),
    path('<int:pk>/', ProductDetail.as_view()),
]