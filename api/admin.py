from django.contrib import admin

from django.contrib import admin
from .models import Livro, Emprestimo # Importa seus modelos

# Registro simples
admin.site.register(Livro)
admin.site.register(Emprestimo)
