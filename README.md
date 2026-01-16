# 📚 Sistema de Gerenciamento de Biblioteca (API)

Este projeto é uma API desenvolvida com **Django Rest Framework** para controle de acervo pessoal e empréstimos de livros.

## 🚀 Funcionalidades

- **Cadastro de Livros**: Gerencie seu acervo pessoal.
- **Controle de Empréstimos**: Registre para quem você emprestou seus livros.
- **Devolução com Avaliação**: Marque livros como devolvidos e registre uma nota (Ótimo, Bom, etc).
- **Histórico Inteligente**: Endpoint que separa automaticamente livros devolvidos de empréstimos ativos.
- **Autenticação Segura**: Apenas o dono do livro pode gerenciar seus empréstimos e visualizar seu histórico.

## 🛠️ Tecnologias Utilizadas

- Python / Django
- Django Rest Framework (DRF)
- SQLite (Banco de dados padrão)


### 🔌 Endpoints Principais

```text
Método | Endpoint | Descrição

- POST  /api/registrar/               - nome, email e senha (8 digitos)
  {
    "nome": "Seu Nome",
    "email": "usuario@email.com",
    "senha": "senha123" 
  }

- POST  /api/login/                   -  email e senha (8 digitos)
  {
    "email": "usuario@email.com",
    "senha": "senha123"
  }

- GET   /api/livros/historico/        - Retorna o histórico separado por status

- GET  /api/livros/                   - Lista todos os seus livros
  {
    "titulo": "Dom Casmurro",
    "autor": "Machado de Assis",
    "genero": "Clássico"
  }

- POST  /api/emprestimos/             - Registra um novo empréstimo
  {
    "livro": 3,
    "nome_destinatario": "Kelly",
    "email_destinatario": "kelly@email.com"
  }

- POST  /api/livros/{id}/devolucao/   - Registra a devolução e avaliação
  {
    "avaliacao": "O"
  }
- 🔑 Como utilizar o Token de Autenticação
Após realizar o login e receber o seu token, você deve incluí-lo no Header (Cabeçalho)
de todas as requisições protegidas (como cadastrar livros ou ver o histórico).

No Postman, siga estes passos:
Vá até a aba Headers.
No campo Key, digite: Authorization.
No campo Value, digite: Token seguido de um espaço e o seu código (Exemplo: Token 9944b091...).
Importante: Se você não enviar este cabeçalho, a API 
retornará um erro 401 Unauthorized, 
pois ela precisa saber quem é o dono dos livros que estão sendo consultados.

