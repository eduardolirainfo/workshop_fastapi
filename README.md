FastAPI Workshop
Criando uma aplicação web com API usando FastAPI


Ambiente
Primeiro precisamos de um ambiente virtual para instalar as dependencias do projeto.

python -m venv .venv
E ativaremos a virtualenv

# Linux
source .venv/bin/activate
# Windows Power Shell
.\venv\Scripts\activate.ps1
Vamos instalar ferramentas de produtividade neste ambiente e para isso vamos criar um arquivo chamado requirements-dev.txt

ipython         # terminal
ipdb            # debugger
sdb             # debugger remoto
pip-tools       # lock de dependencias
pytest          # execução de testes
pytest-order    # ordenação de testes
httpx           # requests async para testes
black           # auto formatação
flake8          # linter
Instalamos as dependencias iniciais.

pip install --upgrade pip
pip install -r requirements-dev.txt
O Projeto
Nosso projeto será um microblog estilo twitter, é um projeto simples porém com funcionalidade suficientes para exercitar as principais features de uma API.

Vamos focar no backend, ou seja, na API apenas, o nome do projeto é "PAMPS" um nome aleatório que encontrei para uma rede social ficticia.

Funcionalidades
Usuários
Registro de novos usuários
Autenticação de usuários
Seguir outros usuários
Perfil com bio e listagem de posts, seguidores e seguidos
Postagens
Criação de novo post
Edição de post
Remoção de post
Listagem de posts geral (home)
Listagem de posts seguidos (timeline)
Likes em postagens
Postagem pode ser resposta a outra postagem
Estrutura de pastas e arquivos
Script para criar os arquivos do projeto.

# Arquivos na raiz
touch setup.py
touch {settings,.secrets}.toml
touch {requirements,MANIFEST}.in
touch Dockerfile.dev docker-compose.yaml

# Imagem do banco de dados
mkdir postgres
touch postgres/{Dockerfile,create-databases.sh}

# Aplicação
mkdir -p pamps/{models,routes}
touch pamps/default.toml
touch pamps/{__init__,cli,app,auth,db,security,config}.py
touch pamps/models/{__init__,post,user}.py
touch pamps/routes/{__init__,auth,post,user}.py

# Testes
touch test.sh
mkdir tests
touch tests/{__init__,conftest,test_api}.py
Esta será a estrutura final (se preferir criar manualmente)

❯ tree --filesfirst -L 3 -I docs
.
├── docker-compose.yaml        # Orquestração de containers
├── Dockerfile.dev             # Imagem principal
├── MANIFEST.in                # Arquivos incluidos na aplicação
├── requirements-dev.txt       # Dependencias de ambiente dev
├── requirements.in            # Dependencias de produção
├── .secrets.toml              # Senhas locais
├── settings.toml              # Configurações locais
├── setup.py                   # Instalação do projeto
├── test.sh                    # Pipeline de CI em ambiente dev
├── pamps
│   ├── __init__.py
│   ├── app.py                 # FastAPI app
│   ├── auth.py                # Autenticação via token
│   ├── cli.py                 # Aplicação CLI `$ pamps adduser` etc
│   ├── config.py              # Inicialização da config
│   ├── db.py                  # Conexão com o banco de dados
│   ├── default.toml           # Config default
│   ├── security.py            # Password Validation
│   ├── models
│   │   ├── __init__.py
│   │   ├── post.py            # ORM e Serializers de posts
│   │   └── user.py            # ORM e Serialziers de users
│   └── routes
│       ├── __init__.py
│       ├── auth.py            # Rotas de autenticação via JWT
│       ├── post.py            # CRUD de posts e likes
│       └── user.py            # CRUD de user e follows
├── postgres
│   ├── create-databases.sh    # Script de criação do DB
│   └── Dockerfile             # Imagem do SGBD
└── tests
    ├── conftest.py            # Config do Pytest
    ├── __init__.py
    └── test_api.py            # Tests da API
Adicionando as dependencias
Editaremos o arquivo requirements.in e adicionaremos

fastapi
uvicorn
sqlmodel
typer
dynaconf
jinja2
python-jose[cryptography]
passlib[bcrypt]
python-multipart
psycopg2-binary
alembic
rich
A partir deste arquivo vamos gerar um requirements.txt com os locks das versões.

pip-compile requirements.in
E este comando irá gerar o arquivo requirements.txt organizado e com as versões pinadas.

Instalação
O nosso objetivo é instalar a aplicação dentro do container, porém é recomendável que instale também no ambiente local pois desta maneira auto complete do editor irá funcionar.

pip install -e .
Containers
Vamos agora escrever o Dockerfile.dev responsável por executar nossa api

Dockerfile.dev

Build the container

docker build -f Dockerfile.dev -t pamps:latest .
Execute o container para testar

$ docker run --rm -it -v $(pwd):/home/app/api -p 8000:8000 pamps
INFO:     Will watch for changes in these directories: ['/home/app/api']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [1] using StatReload
INFO:     Started server process [8]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
Acesse: http://0.0.0.0:8000/docs

API

A API vai ser atualizada automaticamente quando detectar mudanças no código, somente para teste edite pamps/app.py e adicione

O próximo passo é executar com

docker compose up
Definindo os models com Pydantic
database

$ docker compose exec api /bin/bash
app@c5dd026e8f92:~/api$ # este é o shell dentro do container
IMPORTANTE!!!: todos os comandos serão executados no shell dentro do container!!!

E dentro do prompt do container rode:

$ alembic revision --autogenerate -m "initial"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'user'
  Generating /home/app/api/migrations/versions/ee59b23815d3_initial.py ...  done
Repare que o alembic identificou o nosso model User e gerou uma migration inicial que fará a criação desta tabela no banco de dados.

Podemos aplicar a migration rodando dentro do container:

$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> ee59b23815d3, initial
E neste momento a tabela será criada no Postgres, podemos verificar se está funcionando ainda dentro do container:

DICA pode usar um client como https://antares-sql.app para se conectar ao banco de dados.

$ pamps --help

 Usage: pamps [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the      │
│                                                              specified shell.                │
│                                                              [default: None]                 │
│ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the         │
│                                                              specified shell, to copy it or  │
│                                                              customize the installation.     │
│                                                              [default: None]                 │
│ --help                                                       Show this message and exit.     │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────╮
│ shell                        Opens interactive shell                                         │
│ user-list                    Lists all users                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
E cada um dos comandos:

$ pamps user-list
    Pamps users
┏━━━━━━━━━━┳━━━━━━━┓
┃ username ┃ email ┃
┡━━━━━━━━━━╇━━━━━━━┩
└──────────┴───────┘
e

$ pamps shell
Auto imports: ['settings', 'engine', 'select', 'session', 'User']

In [1]: session.exec(select(User))
Out[1]: <sqlalchemy.engine.result.ScalarResult at 0x7fb1aa275ea0>

In [2]: settings.db
Out[2]: <Box: {'uri': 'postgresql://postgres:postgres@db:5432/pamps', 'connect_args': {}, 'echo': False}>
Ainda não temos usuários cadastrados pois ainda está faltando uma parte importante criptografar as senhas para os usuários.


$ python -c "print(__import__('secrets').token_hex(32))"
b9483cc8a0bad1c2fe31e6d9d6a36c4a96ac23859a264b69a0badb4b32c538f8

# OU

$ openssl rand -hex 32
b9483cc8a0bad1c2fe31e6d9d6a36c4a96ac23859a264b69a0badb4b32c538f8
Agora vamos editar pamps/security.py e adicionar alguns elementos


$ pamps create-user --help

 Usage: pamps create-user [OPTIONS] EMAIL USERNAME PASSWORD

 Create user

╭─ Arguments ────────────────────────────────────────────────────╮
│ *    email         TEXT  [default: None] [required]            │
│ *    username      TEXT  [default: None] [required]            │
│ *    password      TEXT  [default: None] [required]            │
╰────────────────────────────────────────────────────────────────╯
E então

$ pamps create-user admin@admin.com admin 1234
created admin user

$ pamps user-list
         Pamps users
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ username ┃ email           ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ admin    │ admin@admin.com │
└──────────┴─────────────────┘

Database Migration
Agora precisamos chamar o alembic para gerar a database migration relativa a nova tabela post.

Dentro do container shell

$ alembic revision --autogenerate -m "post"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'post'
INFO  [alembic.ddl.postgresql] Detected sequence named 'user_id_seq' as owned by integer column 'user(id)', assuming SERIAL and omitting
  Generating /home/app/api/migrations/versions/f9b269f8d5f8_post.py ...  done
e aplicamos com

$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 4634e842ac70 -> f9b269f8d5f8, post
Pode testar no cli dentro do container
$ pamps shell
Auto imports: ['settings', 'engine', 'select', 'session', 'User', 'Post']

In [1]: session.exec(select(Post)).all()
Out[1]: []
Adicionando rotas de conteúdo
Agora os endpoints para listar e adicionar posts

GET /post/ lista todos os posts
POST /post/ cria um novo post (exige auth)
GET /post/{id} pega um post pelo ID com suas respostas
GET /post/user/{username} Lista posts de um usuário especifico
pamps/routes/post.py

A API final

NOTA Ainda está faltando adicionar models e rotas para seguir usuários e para dar like em post.

Testando
O Pipeline de testes será

Garantir que o ambiente está em execução com o docker compose
Garantir que existe um banco de dados pamps_test e que este banco está vazio.
Executar as migrations com alembic e garantir que funcionou
Executar os testes com Pytest
Apagar o banco de dados de testes
Vamos adicionar um comando reset_db no cli

NOTA muito cuidado com esse comando!!!



$ chmod +x test.sh


$ ./test.sh
[+] Running 3/3
 ⠿ Network fastapi-workshop_default  Created                      0.0s
 ⠿ Container fastapi-workshop-db-1   Started                      0.5s
 ⠿ Container fastapi-workshop-api-1  Started                      1.4s

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running stamp_revision f432efb19d1a ->
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> ee59b23815d3, initial
INFO  [alembic.runtime.migration] Running upgrade 4634e842ac70 -> f9b269f8d5f8, post

========================= test session starts =========================
platform linux -- Python 3.10.8, pytest-7.2.0, pluggy-1.0.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /home/app/api
plugins: order-1.0.1, anyio-3.6.2
collected 6 items

tests/test_api.py::test_post_create_user1 PASSED                [ 16%]
tests/test_api.py::test_reply_on_post_1 PASSED                  [ 33%]
tests/test_api.py::test_post_list_without_replies PASSED        [ 50%]
tests/test_api.py::test_post1_detail PASSED                     [ 66%]
tests/test_api.py::test_all_posts_from_user1 PASSED             [ 83%]
tests/test_api.py::test_all_posts_from_user1_with_replies PASSED [100%]

========================== 6 passed in 1.58s ==========================

[+] Running 3/3
 ⠿ Container fastapi-workshop-api-1  Removed                      0.8s
 ⠿ Container fastapi-workshop-db-1   Removed                      0.6s
 ⠿ Network fastapi-workshop_default  Removed                      0.5s
Desafios finais
Lembra-se do nosso database?

