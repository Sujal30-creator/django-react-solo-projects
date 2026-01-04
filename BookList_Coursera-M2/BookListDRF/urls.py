from django.urls import path
from . import views

urlpatterns = [
    path('books/<int:pk>',views.SingleBookView.as_view(), name= 'SingleBook'),
]