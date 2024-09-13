from django import forms
from .models import Item, Contato, Emprestimo

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['titulo', 'autor', 'imagem', 'ano', 'status']

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'telefone']

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['item', 'contato', 'data_emprestimo', 'data_devolucao']
