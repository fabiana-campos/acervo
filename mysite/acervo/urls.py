from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name="login"),
    path('cadastro/', views.CadastroView.as_view(), name="cadastro"),
]