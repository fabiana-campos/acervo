from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    nome = models.CharField(max_length=150)
    email = models.EmailField()
    senha = models.CharField(max_length=50)

class Item(models.Model):
    titulo = models.CharField(max_length=250)
    autor = models.CharField(max_length=250)
    imagem = models.ImageField(upload_to='imgs/')
    ano = models.CharField(max_length=10)
    status = models.CharField(
        max_length=20,
        choices=[
            ('emprestado', 'Emprestado'), ## serão usados no banco de dados
            ('disponivel', 'Disponível'), ##respostas exibidas para usuário
        ],
        null=True,
        blank=True
    )

class Contato(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
