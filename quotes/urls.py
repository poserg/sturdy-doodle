from django.urls import path

from . import views

urlpatterns = [
    path("stocks", views.stocks, name="stocks"),
    path("bonds", views.bonds, name="bonds"),
    path("futures", views.futures, name="futures"),
    path("funds", views.funds, name="funds"),
    path("common", views.common_request, name="common"),
]