from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmprestimoViewSet, RegistroView, LoginView, LivroViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'livros', LivroViewSet, basename='livro') # O prefixo 'livros' cria a rota /api/livros/
router.register(r'emprestimos', EmprestimoViewSet, basename='emprestimo')
urlpatterns = [

    path('', include(router.urls)),
    # O .as_view() é o que transforma a classe em uma função que o Django entende
    path('registrar/', RegistroView.as_view(), name='registrar'),
    path('login/', LoginView.as_view(), name='login'),


]


if settings.DEBUG:
    # 4 ESPAÇOS manuais aqui antes do urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

