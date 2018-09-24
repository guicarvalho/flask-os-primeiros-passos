# Configurando o banco de dados
Vamos configurar o banco de dados da nossa aplicação, como dissemos nos primeiros capítulos vamos construir uma aplicação para vender café online. Basicamente nossa aplicação precisa de 4 tabelas: usuário, produto, venda e produto_venda.

**Usuário**
| Campo | Tipo | Obrigatório | Único
| --- | --- | --- | -- |
| uuid | UUID | sim | sim |
| nome | Texto (50) | sim | não |
| email | Texto (80) | sim | sim |
| senha | Texto (20) | sim | não |
| ativo | Booleano | não | não |
| criado_em | Datetime | não | não |
| atualizado_em | Datetime | não | não |

**Produto**
| Campo | Tipo | Obrigatório | Único
| --- | --- | --- | -- |
| uuid | UUID | sim | sim |
| nome | Texto (50) | sim | não |
| estoque | Inteiro | sim | não |
| valor | Decimal (10,2) | sim | não |
| criado_em | Datetime | não | não |
| atualizado_em | Datetime | não | não |

**Venda**
| Campo | Tipo | Obrigatório | Único
| --- | --- | --- | -- |
| uuid | UUID | sim | sim |
| usuario_uuid | UUID | sim | não |
| valor | Decimal (10,2) | sim | não |
| criado_em | Datetime | não | não |

**Produto_Venda**
| Campo | Tipo | Obrigatório | Único
| --- | --- | --- | -- |
| uuid | UUID | sim | sim |
| produto_uuid | UUID | sim | não |
| quantidade | Inteiro | sim | não |
| valor | Decimal (10,2) | sim | não |
| venda_uuid | UUID | sim | não |

## Adicionando banco de dados na aplicação
Geralmente quando estamos criando uma aplicação profissional evitamos controlar o banco de dados "na mão", pois precisamos pensar em mapear nossas tabelas em objetos, escrever comandos SQL seguros, controlar transações com o banco de dados, gerenciar conexões, etc.
Para fazer esse trabalho "sujo" vamos contar com o `ORM SQLAlchemy`! O `SQLAlchemy` é um framework maduro e muito utilizado na comunidade Python. O `Flask` tem um _wrapper_ que facilita a configuração e uso do `SQLAlchemy` no `Flask`, vamos adicioná-lo em nossa aplicação.
```sh
user@: poetry add flask-sqlalchemy
```
Como banco de dados iremos utilizar o `PostgreSQL`, para isso vamos adicionar a biblioteca `psycopg2` que implementa a `DBAPI`.
```sh
user@: poetry add psycopg2
```
Outro ponto que devemos nos atentar é que em aplicações reais o banco pode sofrer atualizações (inserção/remoção de campos, adicionar uma nova tabela). Existe ferramentas que nos auxiliam no versionamento da estrutura do banco de dados, elas são conhecidas como ferramentas de _migração_.

Vamos adicionar mais um _plugin_ para o nosso projeto `Flask-Migrate`, que será responsável por cuidar dessa parte.
```sh
user@: poetry add flask-migrate
```

## Configurando Flask-SQLAlchemy e Flask-Migrate
Uma vez adicionado precisamos configurar o plugin. Vamos informar qual o _host_, _usuário_ e _senha_ para conectar com o nosso banco de dados.
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@localhost:9988/coffee_shop'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

### Criando as tabelas
A ideia quando utilizamos `ORM` é mapear as tabelas do sistema em objetos, dessa forma podemos trabalhar em um nível mais alto sem nos preocuparmos com comandos `SQL`.
```python
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@localhost:9988/coffee_shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class User(db.Model):

    __tablename__ = 'user'

    uuid = db.Column(UUID, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'User (uuid: {self.uuid}, name: {self.name}, email: {self.email}, active: {self.active})'


class Product(db.Model):

    __tablename__ = 'product'

    uuid = db.Column(UUID, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'Product (uuid: {self.uuid}, name: {self.name}, stock: {self.stock}, value: {self.value})'


class Sale(db.Model):

    __tablename__ = 'sale'

    uuid = db.Column(UUID, primary_key=True)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    user_uuid = db.Column(UUID, db.ForeignKey('user.uuid'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Sale (uuid: {self.uuid}, value: {self.value}, user_uuid: {self.user_uuid})'


class ProductSale(db.Model):

    __tablename__ = 'product_sale'

    uuid = db.Column(UUID, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    product_uuid = db.Column(UUID, db.ForeignKey('product.uuid'), nullable=False)
    sale_uuid = db.Column(UUID, db.ForeignKey('sale.uuid'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'uuid: {self.uuid}, quantity: {self.quantity}, value: {self.value}, product_uuid: {self.product_uuid}, ' \
                'sale_uuid: {sale.uuid}'
```
Agora precisamos dizer ao `SQLAlchemy` para criar as tabelas no nosso banco de dados, para isso vamos conectar no `shell` da nossa aplicação com o comando `flask shell`.
> Após executar o comando `flask shell` será habilitado o prompt padrão do Python. O prompt padrão é muito pobre e podemos melhorá-lo instalando `flask-shell-ipython`. Esse pacote deve ser inserido como pacote de desenvolvimento: `poetry add -D flask-shell-ipython`.
```python
from coffee_shop.app import db
db.create_all()
```
Vamos até o banco de dados e verificar se as tabelas foram criadas.
```sh
user@: docker exec -ti flask-course-pg psql
root=# \c coffee_shop
coffee_shop=# \d
           List of relations
 Schema |     Name     | Type  | Owner
--------+--------------+-------+-------
 public | product      | table | root
 public | product_sale | table | root
 public | sale         | table | root
 public | user         | table | root
(4 rows)
```

### Manipulando registros no banco de dados
Vamos criar alguns registros e efetuar algumas operações básicas para entender melhor como trabalhar com o `ORM`.

### Inserindo registros
```python
from uuid import uuid4
from coffee_shop.app import db, User, Product

user = User(uuid=uuid4().hex, name='John Doe', password='123mudar', email='john@doe.com', active=True)
db.session.add(user)
db.session.commit()

p1 = Product(uuid=uuid4().hex, name='Café Orfeu Japy Torrado e Moído 250g', stock=5, value=31.50)

p2 = Product(uuid=uuid4().hex, name='Café Baronesa Torr. e Moído-1º lugar 250g', stock=2, value=57.90)

p3 = Product(uuid=uuid4().hex, name='Café Santo Grão Descafeinado Torrado e Moído 250g', stock=7, value=43.50)

db.session.add_all([p1, p2, p3])
db.session.commit()
```
Acabamos de inserir um usuário e três produtos na base de dados. Utilizamos os métodos `add` e `add_all` para inserir _objetos_ na sessão e posteriormente utilizamos o método `commit` para escrever os registros no banco de dados.

### Consultando registros
Outra necessidade é consultar os registros, essas consultas podem ser simples ou envolver uma série de critérios. Para consultar podemos utilizar os comandos `filter` e `filter_by`.
```python
products = Product.query.filter(Product.name.ilike('%Orfeu%')).all()
products[0].name
>>> 'Café Orfeu Japy Torrado e Moído 250g'

products = Product.query.filter_by(value=43.50).all()
products[0].name
>>> 'Café Santo Grão Descafeinado Torrado e Moído 250g'
```
Ambos comandos retornam o objeto `BaseQuery` onde podemos recuperar o _resultset_ ou adicionar mais critérios. Nos exemplos acima utilizamos o método `all` que irá retornar uma lista de objetos que atenderam a condição. Além do método `all` podemos utilizar os métodos `one`, `first` e `scalar`.

### Excluindo registros
Para remover os registros usamos o método `delete`, podemos usá-lo para apagar os registros retornados por uma consulta ou apagar todos os registros da base de dados.

```python
db.session.add_all([
    Product(uuid=uuid4().hex, name='Café Orfeu', stock=5, value=31.50),
    Product(uuid=uuid4().hex, name='Café Araraquara', stock=5, value=21.50),
    Product(uuid=uuid4().hex, name='Café Matão', stock=5, value=21.50),
])

db.session.commit()

assert Product.query.count() == 3

Product.query.filter(Product.name.contains('Orfeu')).delete(synchronize_session=False)
>>> 1

assert Product.query.count() == 2

Product.query.delete()
>>> 2
```
