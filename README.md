# KMDb

**Versão 0.0.9**

## Instalação

Ao iniciar o projeto, no terminal, na raiz, rodar o comando no terminal:

./manage.py migrate

Para criar as tabelas.

Instalação será implementada.


## Sobre:

KMDb é uma plataforma para amantes de filmes. A plataforma possui cadastros para filmes e suas sinopses, análises e comentários.
A aplicação possui 3 tipos de usuários. O token identifica qual é o tipo de usuário, garantindo suas respectivas permissões dentro da plataforma. São eles:
* Administradores poderão cadastrar filmes para que críticos possam avaliar e usuários possam comentar.
* Críticos podem analisar filmes. Também é possível fazer a edição da análise.
* Usuários podem fazer comentários sobre os filmes.

Para visualizar os filmes (rota GET), não é preciso ter cadastro na plataforma. 

As rotas devem ser utilizadas como prefixo http://127.0.0.1:8000/

Exemplo, a rota que cria usuários, será http://127.0.0.1:8000/api/accounts


## Rotas e requisições


### Criação de usuários

/api/accounts/

método: POST

Cria conta de usuário.

Exemplo de requisição:

{
	"username":"user",
	"password":"1234",
	"first_name":"primeironome",
	"last_name":"sobrenome",
	"is_superuser":false,
	"is_staff":false
}

Caso o usuário seja adminstrador, podendo cadastrar filme, is_superuser deverá ser true.
Caso o usuário seja um avaliador, is_staff deverá ser true.

### Login

/api/login/

método: POST

Loga na conta. Obtém token de identificação.

Exemplo de requisição:

{
	"username":"user",
	"password":"1234"
}

### Cadastrar filmes

/api/movies/

método: POST
necessário Token de administrador

Exemplo de requisição:

{
	"title":"Efeito Borboleta",
	"duration":"113m",
	"genres":[
		{"name":"suspense"},
		{"name":"drama"},
		{"name":"ficção científica"}
	],
	"launch":"2004-01-01",
	"classification":0,
	"synopsis": "O estudante universitário Evan Treborn está aflito com dores de cabeça tão fortes que frequentemente desmaia. Enquanto está inconsciente, Evan pode viajar de volta no tempo para momentos de dificuldades na infância. Ele também pode alterar o passado para os amigos, como Kayleigh, que foi molestada pelo pai. Porém ao mudar o passado, ele pode alterar o presente, o que leva Evan a se encontrar em um pesadelo de realidades alternativas, incluindo uma onde ele está preso."
}

### Listar filmes

/api/movies/

método: GET

Lista todos os filmes cadastrados.

### Filtrar filme

/api/movies/<int: movie_id>

método: GET

Filtra filme pelo ID.

Também é possível filtrar por um campo de buscas
Nesse caso, a rota deverá ser:

/api/movies/

Exemplo de requisição:
{
	"title":"borbo"
}

### Deletar filme

/api/movies/<int: movie_id>

método: DELETE
necessário Token de administrador

Deleta filme pelo ID.

### Cadastrar análise

/api/movies/<int: movie_id>/review/

método: POST

{
	"stars":7,
	"review":"Excelente filme.",
	"spoilers":false
}

stars é a nota de 0 a 10 para o filme. 

### Editar análise

/api/movies/<int: movie_id>/review/

método: PUT

{
	"stars":10,
	"review":"Excelente filme. Nos faz pensar nas possibilidades de cada ação que tomamos diante da vida.",
	"spoilers":true
}

Edita análise já criada em algum filme. 

### Criar comentário

/api/movies/<int: movie_id>/comments/

método: POST

{
	"comment":"Amei. Virou filme favorito."
}

Cria comentário para determinado filme.

### Editar comentário

/api/movies/<int: movie_id>/comments/

método: PUT

{
"comment_id":1,
"comment":"Amei. Com certeza um filme que marcou para toda a vida."
}


## Testes

Para executar os testes, é necessário digitar no terminal, na raíz do projeto o seguinte comando:

TEST=TEST python manage.py test -v 2

Caso queira um relatório de testes, rodar o seguinte comando:

TEST=TEST python manage.py test -v 2 &> report.txt

