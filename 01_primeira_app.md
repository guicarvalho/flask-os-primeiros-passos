# Primeira App
Vamos criar nossa primeira aplicação Flask. Para isso precisamos instalar o Flask no projeto que criamos previamente.
```sh
user@: cd ~/coffee-shop  # informe o caminho onde criou o projeto com o comando poetry new
user@: poetry add flask
```
Pronto, agora vamos criar o arquivo que será o ponto de partida da aplicação `touch coffee-shop/app.py`. Edite o arquivo com o conteúdo:
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World'
```
Acabamos de criar o nosso primeiro `hello world` em `Flask`. Como a maioria dos frameworks web `Python`, o `Flask` vem com um servidor de desenvolvimento que podemos utilizar durante a fase de construção da nossa aplicação.
> Apesar de ser possível NÃO use o servidor de desenvolvimento do Flask em ambiente de produção!
Para rodar devemos `exportar` duas variáveis de ambiente: `FLASK_APP` informa o caminho do módulo onde está definida a aplicação `Flask` e `FLASK_ENV` informa em qual ambiente a aplicação está sendo executada:
```sh
user@: FLASK_APP=coffee_shop/app.py FLASK_ENV=development flask run
* Serving Flask app "coffee_shop/app.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 331-156-771
```
O servidor irá iniciar em [http://localhost:5000](http://localhost:5000), ao abrir o navegador será exibida a mensagem `Hello World`.

### Recebendo parâmetros na URL
Vamos alterar um pouco nossa aplicação para deixar a mensagem dinâmica ao invés de exibir apenas `hello world`, vamos exibir `Hello <user>` onde `user` será passado por `query string`.
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    user = request.args.get('user', 'anônimo')
    return f'Hello {user}!'
```
Agora ao recarregar a página o texto `Hello anônimo` deve aparecer, se passarmos o parâmetro informando o usuário `http://localhost:5000?user=JohnDoe` a mensagem deve ser `Hello JohnDoe`.

### Criando uma nova rota para somar dois números
Podemos ter `N` rotas em nossa aplicação, para isso basta adicionar `@app.route` com caminhos únicos. Vamos criar uma nova rota que irá ser responsável por somar dois números.
```python
@app.route('/<a>/<b>')
def calculate_sum(a, b):
    return a + b
```
Agora podemos executar [http://localhost:5000/1/2](http://localhost:5000/1/2). Conforme esparado o resultado deve ser `3`, porém ao analisar a saída vemos que o resultado foi `12`. Isso acontece pois os argumentos foram recebidos como `str`.
Para resolver isso podemos converter os parâmetros para `int`:
```python
@app.route('/<a>/<b>')
def calculate_sum(a, b):
    return str(int(a) + int(b))
```
Agora se executarmos novamente a mesma `URL` vamos receber o valor `3`. Essa forma está correta mas não é a melhor forma no `Flask` para converter valores recebidos pela `URL`. Podemos dizer ao `Flask` quais os tipos dos `argumentos` que esperamos receber por parâmetro:
```python
@app.route('/<a:int>/<b:int>')
def calculate_sum(a, b):
    return str(a + b)
```
Agora além dos valores já serem convertidos automaticamente caso o usuário passe um valor que não seja um `int` válido a requisição irá retornar um `404` uma vez que não existe a `URL` requisitada.

### Restringindo métodos pelo verbo HTTP
O protocolo HTTP implementa diversos métodos, os mais conhecidos são `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD` e `OPTIONS`. Os métodos devem ser utilizados de acordo com a necessidade, por exemplo se quisermos criar uma rota onde podemos apenas ler os dados (_read-only_) então a rota só deve permitir chamadas com o verbo `GET`, e quando a requisição para essa rota não for `GET` a resposta deve ser `405 Method not Allowed` informando que o método não é permitido.
Vamos criar uma rota em nossa aplicação onde o usuário irá informar o nome e idade de uma pessoa, essa rota deve permitir apenas chamadas com o verbo `POST`.
```python
from http import HTTPStatus

from flask import Flask, jsonify, request

app = Flask(__name__)
people = []

@app.route('/new/person', methods=['POST'])
def add_person():
    people.append(request.json)
    return jsonify(request.json), HTTPStatus.CREATED
```
Vamos chamar a rota utilizando o `curl`.
```sh
user@: curl -X POST -H "Content-Type: application/json" -d }' http://localhost:5000/new/person
{
  "age": 24,
  "name": "Guilherme"
}
```
Se fizermos a mesma chamada mas dessa vez com outro verbo que não seja `POST` vamos receber uma resposta com código de status `405`.
```sh
user@: curl -X GET -H "Content-Type: application/json" -d }' http://localhost:5000/new/person
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>405 Method Not Allowed</title>
<h1>Method Not Allowed</h1>
<p>The method is not allowed for the requested URL.</p>
```
Uma rota pode aceitar mais de um verbo e para isso devemos adicionar os verbos desejados na lista de verbos permitidos.
```python
@app.route('/people', methods=['POST', 'GET'])
def people_route():
    if request.method == 'POST':
        people.append(request.json)
        return jsonify(request.json), HTTPStatus.CREATED
    return jsonify(people)
```
No exemplo acima criamos uma rota para cadastrar e listar as pessoas cadastradas. Quando a requisição for `POST` o registro é inserido, quando for `GET` todos os registros inseridos na lista serão retornados.
```sh
user@: curl -X POST -H "Content-Type: application/json" -d }' http://localhost:5000/people
{
  "age": 24,
  "name": "Guilherme"
}
```
```sh
user@: curl http://localhost:5000/people
[
  {
    "age": 24,
    "name": "Guilherme"
  }
]
```

## Exercícios
1. Crie uma aplicação Flask para calcular o IMC, a aplicação deve preencher os seguintes pré requisitos:

    a. Crie uma rota para cadastrar as pessoas (nome, idade, sexo, número e peso).

    b. Crie uma rota para listar todos os usuários cadastrados, ordenado por resultado do melhor para o pior (coluna nível quanto menor melhor). Imprima o valor do IMC e qual a situação (confira a tabela abaixo).

> Para calcular o IMC divide-se o peso (em kilogramas) pela altura (ao quadrado): peso / (altura * altura).

| Resultado	| Situação | Nível |
|---	|--- | ---
| Abaixo de 17 | Muito abaixo do peso | 5 |
| Entre 17 e 18,49  | Abaixo do peso | 1 |
| Entre 18,5 e 24,99 | Peso normal | 0 |
| Entre 25 e 29,99 | Acima do peso | 2 |
| Entre 30 e 34,99 | Obesidade I | 3 |
| Entre 35 e 39,99 | Obesidade II (severa) | 4 |
| Acima de 40 | Obesidade III (mórbida) | 6 |
