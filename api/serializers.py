from rest_framework import serializers
from .models import Livro, Emprestimo
from django.contrib.auth.models import User

class LivroSerializer(serializers.ModelSerializer):
      # Isso faz o campo 'usuario' retornar o que está no __str__ do modelo User
    usuario = serializers.StringRelatedField(read_only=True)

    class Meta: 
        model = Livro
        fields = '__all__' # Isso diz ao Django para transformar todos os campos em JSON
      

class EmprestimoSerializer(serializers.ModelSerializer):
    
    #nome_cadastrado = serializers.PrimaryKeyRelatedField(
    nome_cadastrado = serializers.StringRelatedField(
        read_only=True, 
        label="Usuário Logado"
    )
   
    nome_destinatario = serializers.CharField(label="Destinatário (Nome ou Email)", 
        required=False,
        allow_blank=True
    )

    class Meta:
        model = Emprestimo
        # A ordem abaixo define como o formulário HTML será montado de cima para baixo
        fields = [
            'livro',
            'nome_cadastrado',     
            'nome_destinatario', 
            'data_emprestimo',
            'data_devolucao',
            'avaliacao'
        ]

        # Tornamos esses campos não obrigatórios para o POST de empréstimo
        extra_kwargs = {
            'avaliacao': {'required': False},
            'data_devolucao': {'required': False},
        }

    def validate_livro(self, value):
    # Se o livro já estiver marcado como emprestado, impede o novo registro
        if value.emprestado:
            raise serializers.ValidationError("Este livro já está emprestado e não pode sair novamente.")
        return value