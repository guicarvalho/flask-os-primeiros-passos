# Preparando o ambiente de desenvolvimento
Para esse curso vamos criar uma API para locação de imóveis, para isso vamos utilizar `Python`, `Flask`, `Postgre` e algumas bibliotecas.
Para evitar a instalação local do `Postgre` vamos utilizar um container Docker, assim como vamos instalar o `Pyenv` para gerenciar as versões do `Python` e o `Poetry` para gerenciar as dependências do nosso projeto. Como editor de texto vamos utilizar o `VSCode` e o sistema operacional base será o `Debian`.

## Instalando VSCode
O processo de instalação do `VSCode` é bem simples no `Debian`, basta baixar [baixar](https://code.visualstudio.com/docs/setup/linux#_debian-and-ubuntu-based-distributions) o pacote `.deb` e executar no terminal ou com um cliente de instalação de pacotes.

## Instalando Docker Engine + Docker Compose
Da mesma forma a instalação do `Docker` é bem simplificada para os sistemas derivados do `Debian` basta seguir os passos descritos nesse [tutorial](https://docs.docker.com/install/linux/docker-ce/debian/).

### Criando container Postgre
Como dissemos anteriormente, não vamos instalar o `Postgre` diretamente em nosso sistema operacional (_sinta-se livre para fazê-lo caso queira_). Ao invés disso vamos criar um container `Docker`.
```sh
user@: docker -v
Docker version 18.06.1-ce, build e68fc7a

user@: docker run --name flask-course-pg -p 9988:5432 -e POSTGRES_PASSWORD=root -e POSTGRES_USER=root -d postgres
1208bd7183eed0c145d57b82ada98e10e280b45d20d882ccbaa880113612638f
```
O primeiro comando deve retornar a versão do `Docker` instalada em nossa máquina (_caso o comando não retorne a versão retorne ao passo de instalação_). Depois criamos um novo container chamado _flask-course-pg_ com o comando `docker run`, mapeamos ele na porta `9988` com usuário e senha `root`.
```sh
user@: docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
1208bd7183ee        postgres            "docker-entrypoint.s…"   38 seconds ago      Up 35 seconds       0.0.0.0:9988->5432/tcp   flask-course-pg
```

### Criando o banco de dados
Agora que o banco está rodando, podemos criar o nosso banco de dados, para isso vamos rodar o `psql` via terminal.
> Fique a vontade para escolher um cliente de banco de dados visual como _PgAdmin4_ caso preferir.
```sh
user@: docker exec -ti flask-course-pg psql

postgres=# CREATE DATABASE coffee_shop WITH OWNER "root" ENCODING "UTF8" LC_COLLATE="en_US.utf8" LC_CTYPE="en_US.utf8";
CREATE DATABASE

postgres=# Ctrl+D
```

## Instalando o Pyenv
O `Pyenv` é um utilitário que permite instalar `N` versões da linguagem `Python` no sistema operacional de uma maneira muito simples através do seu _CLI_. Antes de fazer a instalação do `Pyenv` devemos instalar alguns pacotes que são pré requisitos para o seu funcionamento. Os pacotes para cada sistema operacional podem ser encontrados nesse link na _Wiki_ do _repositório_: [common build problems](https://github.com/pyenv/pyenv/wiki/Common-build-problems).
A forma mais simples de instalar o `Pyenv` é utilizando um outro projeto chamado [pyenv-installer](https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer).

## Instalando o Poetry
Vamos instalar o nosso gerenciador de dependências, para essa tarefa vamos utilizar o `Poetry`.
> Novamente fique a vontade para utilizar o gerenciador de pacotes que mais te agrada: Pipenv, pip, etc.
Vamos baixar o `Python 3.7` e definir como versão global, para isso vamos utilizar o `pyenv`.
```sh
user@ pyenv install 3.7.0
user@: pyenv global 3.7.0
user@: python -V
Python 3.7.0

user@ pip install poetry
```

### Criando o nosso projeto
Como dissemos anteriormente vamos utilizar o `Poetry` como gerenciador de pacotes. O CLI do `Poetry` tem vários recursos interessantes [veja mais aqui](https://poetry.eustace.io/docs/cli/#commands) e um deles serve justamente para criar uma estrutura inicial de projeto.
```sh
user@: poetry new coffee-shop
user@: tree
├── coffee_shop
│   └── __init__.py
├── pyproject.toml
├── README.rst
└── tests
    ├── __init__.py
    └── test_coffee_shop.py

2 directories, 5 files
```
Para verificar se o projeto foi criado com sucesso, listamos os arquivos com o comando `tree`. Agora podemos instalar as dependências (_pytest_) e executar os testes unitários criados:
```sh
user@: pytest -v
tests/test_coffee_shop.py::test_version PASSED
```
> Caso o terminal não reconheça o comando `pytest -v` carregue as dependências para o contexto do shell com o comando `poetry shell`.
