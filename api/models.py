from django.db import models

from django.utils import timezone as django_timezone 
from django.db import models
from datetime import date
import datetime
from django.contrib.auth.models import User # Usando o padrão de mercado

class Livro(models.Model):
    nome = models.CharField(max_length=45)
    autor = models.CharField(max_length=30)
    data_cadastro = models.DateField(default=date.today)
    emprestado = models.BooleanField(default=False)
    categoria = models.CharField(max_length=30)
    # Agora apontando para o User padrão do Django
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Emprestimo(models.Model):
    choices = [
        ('P', 'Péssimo'),
        ('R', 'Ruim'),
        ('B', 'Bom'),
        ('O', 'Ótimo'),
    ]
    # Usuário que pegou emprestado (se tiver cadastro)
    nome_cadastrado = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    nome_destinatario = models.CharField(max_length=30, blank=True, null=True)
    data_emprestimo = models.DateTimeField(default=django_timezone.now)
    data_devolucao = models.DateTimeField(blank=True, null=True)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    avaliacao = models.CharField(max_length=1, choices=choices, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.nome_cadastrado or self.nome_destinatario} | {self.livro}"