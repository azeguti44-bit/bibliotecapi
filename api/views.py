from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token # Precisamos disso para o Login
from rest_framework.permissions import AllowAny
from .serializers import LivroSerializer, EmprestimoSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Livro, Emprestimo
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from datetime import datetime
from django.utils import timezone as django_timezone 
from rest_framework.exceptions import ValidationError

class RegistroView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        nome = request.data.get('nome')
        email = request.data.get('email')
        senha = request.data.get('senha')

        # Validações (substituindo seus redirects por retornos de erro JSON)
        if not nome or not email:
            return Response({"erro": "Nome e email são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

        if len(senha) < 8:
            return Response({"erro": "Senha muito curta"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"erro": "Este email já está cadastrado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # O Django User já faz o hash da senha automaticamente com create_user
            user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
            return Response({"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"erro": "Erro interno no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        senha = request.data.get('senha')

        # authenticate através de criptografica verifica se o hash bate
        user = authenticate(username=email, password=senha)

        if user is not None:
            # Em vez de session, geramos um TOKEN - verifica se o usuário já tem um token se não, cria!
            # o token só é gerado quando o usuario faz o login
            # o token é a ponte de confiança entre o cliente e o servidor
            # o ID é só sua referência no banco de dados
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key, 
                "usuario_id": user.id,
                "mensagem": "Login realizado!"
            }, status=status.HTTP_200_OK)
        else:
            return Response({"erro": "Email ou senha inválidos"}, status=status.HTTP_401_UNAUTHORIZED)
        

class LivroViewSet(viewsets.ModelViewSet):
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # usuário só leia o que é dele.
        return Livro.objects.filter(usuario=self.request.user)
    
    # usuário só escreva/crie coisas para ele mesmo.
    def perform_create(self, serializer): 
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def devolucao(self, request, pk=None):
        livro = self.get_object()
        
         # 1. Buscamos o registro de empréstimo que ainda está aberto
        ultimo_emprestimo = Emprestimo.objects.filter(livro=livro, data_devolucao__isnull=True).last()

        # 2. SE encontramos um empréstimo aberto, fazemos as atualizações:
        if ultimo_emprestimo:

            avaliacao_recebida = request.data.get('avaliacao')
            # Encerra o registro de empréstimo com a hora atual
            ultimo_emprestimo.data_devolucao = django_timezone.now()         
            # Se o usuário enviou avaliação, salvamos ---
            if avaliacao_recebida:
                ultimo_emprestimo.avaliacao = avaliacao_recebida
            
            ultimo_emprestimo.save()

            # Avisa ao banco que o LIVRO agora está livre
            livro.emprestado = False
            livro.save()

            return Response({
                "mensagem": "Livro devolvido com sucesso!",
                "avaliacao": ultimo_emprestimo.avaliacao
            }, status=status.HTTP_200_OK)
        
        # 3. Caso não encontre um empréstimo aberto
        return Response(
            {"erro": "Não foi encontrado um empréstimo ativo para este livro."}, 
            status=status.HTTP_400_BAD_REQUEST
        )


    @action(detail=False, methods=['get'])
    def historico(self, request):
        # Buscamos todos os empréstimos dos livros que pertencem ao usuário logado
        emprestimos = Emprestimo.objects.filter(livro__usuario=request.user)

        # 1. Livros já devolvidos (com avaliação e data de devolução)
        devolvidos = emprestimos.filter(data_devolucao__isnull=False)

        # 2. Livros ainda emprestados (data_devolucao é null)
        pendentes = emprestimos.filter(data_devolucao__isnull=True)

        # Usamos o serializer para transformar os dados em JSON
        serializer_devolvidos = EmprestimoSerializer(devolvidos, many=True)
        serializer_pendentes = EmprestimoSerializer(pendentes, many=True)

        return Response({
            "devolvidos_com_avaliacao": serializer_devolvidos.data,
            "ainda_emprestados": serializer_pendentes.data
        })

class EmprestimoViewSet(viewsets.ModelViewSet):
    # pega todos os livro com emprestimo=true
    queryset = Emprestimo.objects.all()
    
    serializer_class = EmprestimoSerializer
    # Garante que só usuários logados (com Token) acessem
    permission_classes = [IsAuthenticated] 
  
    def perform_create(self, serializer):
        # Salva o empréstimo vinculando o usuário logado
        instance = serializer.save(nome_cadastrado=self.request.user)
        
        # 2. Pega o livro que foi enviado no JSON
        livro = instance.livro
        
        # 3. Atualiza o status do livro para emprestado
        if livro:
            livro.emprestado = True
            livro.save()
            print(f"Sucesso: Livro {livro.id} marcado como emprestado.")


  