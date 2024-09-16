from django.db import models

class Contato(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome

class Item(models.Model):
    titulo = models.CharField(max_length=250)
    autor = models.CharField(max_length=250)
    imagem = models.ImageField(upload_to='imgs/', null=True, blank=True)  # imagem é opcional
    ano = models.CharField(max_length=10)
    status = models.CharField(
        max_length=20,
        choices=[
            ('emprestado', 'Emprestado'),
            ('disponivel', 'Disponível'),
        ],
        default='disponivel'
    )

    def __str__(self):
        return self.titulo

class Emprestimo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # O item que foi emprestado
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)  # Para quem o item foi emprestado
    data_emprestimo = models.DateField()
    data_devolucao = models.DateField(null=True, blank=True)  # Campo opcional para data de devolução
    devolvido = models.BooleanField(default=False)  # Se o item já foi devolvido ou não

    def __str__(self):
        return f'{self.item.titulo} emprestado para {self.contato.nome}'
