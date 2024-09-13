from django.contrib import admin
from .models import Usuario, Contato, Item, Emprestimo

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')  # Campos que serão exibidos na lista

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'ano', 'status')

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('item', 'contato', 'data_emprestimo', 'data_devolucao', 'devolvido')
