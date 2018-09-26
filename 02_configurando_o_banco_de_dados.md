# Configurando o banco de dados
Vamos configurar o banco de dados da nossa aplicação, como dissemos nos primeiros capítulos vamos construir uma aplicação para vender café online. Basicamente nossa aplicação precisa de 4 tabelas: `usuário`, `produto`, `venda` e `produto_venda`.

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
Geralmente quando estamos criando uma aplicação real evitamos controlar o banco de dados "na mão", pois precisamos pensar em mapear nossas tabelas em objetos, escrever comandos SQL seguros, controlar transações com o banco de dados, gerenciar conexões, etc.
Para fazer esse trabalho "sujo" vamos contar com a ajuda do `ORM SQLAlchemy`! O `SQLAlchemy` é um framework maduro e muito utilizado na comunidade Python. O `Flask` tem um _wrapper_ que facilita a configuração e uso do `SQLAlchemy` no `Flask`, vamos adicioná-lo em nossa aplicação.
```sh
user@: poetry add flask-sqlalchemy
```
Como banco de dados iremos utilizar o `PostgreSQL`, para isso vamos adicionar a biblioteca `psycopg2` que implementa a `DBAPI`.
```sh
user@: poetry add psycopg2
```
Outro ponto que devemos nos atentar é que em aplicações reais o banco pode sofrer atualizações (inserção/remoção de campos, adicionar uma nova tabela). Existem ferramentas que nos auxiliam no versionamento da estrutura do banco de dados, elas são conhecidas como ferramentas de _migração_.

Vamos adicionar mais um _plugin_ para o nosso projeto chamado `Flask-Migrate`, que será responsável por cuidar dessa parte para nós.
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
A ideia quando utilizamos `ORM` é mapear as tabelas do sistema em objetos, dessa forma podemos trabalhar em um nível mais alto sem nos preocuparmos com comandos `SQL` puros.
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
Agora que os modelos foram mapeados precisamos gerar a migração inicial, ela será a responsável por gerar todas as tabelas que acabamos de definir. Como dissemos anteriormente o `Flask-Migrate` será o responsável por controlar as migrações do nosso projeto. A primeira coisa a ser feita é criar o repositório de migrações com o comando `flask db init`, esse comando irá criar uma pasta `migrations` no diretório raíz do projeto.
> O conteúdo da pasta `migrations` deve ser adicionado para o controle de versão junto com os demais arquivos de código.

Agora vamos criar a migração inicial com o comando `flask db migrate`, ao executar esse comando será gerado um arquivo python com com dois métodos `upgrade` e `downgrade`, o primeiro método contém código para "incrementar" a versão do banco e o segundo "volta" a versão do banco antes da migração atual ser aplicada.

> Sempre verifique o arquivo gerado, nem sempre o conteúdo dos métodos `upgrade` e `downgrade` serão satisfatórios.

O arquivo gerado deve se parecer com esse:
```python
"""empty message

Revision ID: 0b7627b06ae6
Revises:
Create Date: 2018-09-24 20:58:49.182442

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0b7627b06ae6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('uuid', postgresql.UUID(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('value', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('user',
    sa.Column('uuid', postgresql.UUID(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('email')
    )
    op.create_table('sale',
    sa.Column('uuid', postgresql.UUID(), nullable=False),
    sa.Column('value', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('user_uuid', postgresql.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('product_sale',
    sa.Column('uuid', postgresql.UUID(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('value', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('product_uuid', postgresql.UUID(), nullable=False),
    sa.Column('sale_uuid', postgresql.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_uuid'], ['product.uuid'], ),
    sa.ForeignKeyConstraint(['sale_uuid'], ['sale.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_sale')
    op.drop_table('sale')
    op.drop_table('user')
    op.drop_table('product')
    # ### end Alembic commands ###
```
Agora vamos executar o comando que irá de fato criar as tabelas, para que a migração seja executada usamos o comando `flask db upgrade`. Vamos até o banco de dados e verificar se as tabelas foram criadas.
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
Vamos criar alguns registros e efetuar algumas operações básicas para entender melhor como trabalhar com o `ORM`, para isso vamos conectar no `shell` da nossa aplicação com o comando `flask shell`.
> Após executar o comando `flask shell` será habilitado o prompt padrão do Python. O prompt padrão é muito pobre e podemos melhorá-lo instalando `flask-shell-ipython`. Esse pacote deve ser inserido como pacote de desenvolvimento: `poetry add -D flask-shell-ipython`.

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

### Relacionamentos
Para ilustrar como os relacionamentos são feitos no `SQLALchemy` vamos criar dois novos modelos `Parent` e `Child`. Vamos utiliza-los para exemplificar os 4 tipos mais comuns de relação: `One To Many`, `Many To One`, `One To One` e `Many To Many`.

#### One To Many
Um relacionamento `one to many` coloca uma `chave-estrangeira` na tabela `child` referenciando o `parent`, `relationship()` é então especificado no `parent`, como uma coleção de items representados por `child`.

```python
class Parent(db.Model):
  __tablename__ = 'parent'

  uuid = db.Column(UUID, primary_key=True)
  children = db.relationship('Child')

  def __repr__(self):
    return f'Parent (uuid: {self.uuid})'

class Child(db.Model):
  __tablename__ = 'child'

  uuid = db.Column(UUID, primary_key=True)
  parent_uuid = db.Column(UUID, db.ForeignKey('parent.uuid'))

  def __repr__(self):
    return f'Child (uuid: {self.uuid}, parent_uuid: {self.parent_uuid})'
```

Vamos executar algumas operações no `shell` para entender como os registros estão sendo referenciados. Abra o `shell` `flask shell`.
```python
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from app import db

# cole o código que escrevemos acima...

# Adiciona parent
db.session.add(Parent(uuid=uuid4().hex))
assert Parent.query.count() == 1

# Recupera parent criado
parent = Parent.query.one()

# Adiciona 3 child com referencia para o parent criado acima
db.session.add_all([Child(uuid=uuid4().hex, parent_uuid=parent.uuid) for _ in range(3)])
assert Child.query.count() == 3

# Acessa todos os child referenciados a "ele" acessando o relationship `children`
assert len(parent.children) == 3
print(parent.children)
```

Para estabelecer um relacionamento bidirecional em um `one-to-many`, onde o lado `oposto` é um `many-to-one`, vamos especificar um `relationship()` adicional e conectar os dois usando um parâmetro `relationship.back_populate`.
```python
class Parent(db.Model):

    __tablename__ = 'parent'

    uuid = db.Column(UUID, primary_key=True)
    children = db.relationship('Child', back_populates='parent')

    def __repr__(self):
        return f'Parent (uuid: {self.uuid})'


class Child(db.Model):

    __tablename__ = 'child'

    uuid = db.Column(UUID, primary_key=True)
    parent_uuid = db.Column(UUID, db.ForeignKey('parent.uuid'))
    parent = db.relationship('Parent', back_populates='children')

    def __repr__(self):
        return f'Child (uuid: {self.uuid}, parent_uuid: {self.parent_uuid})'
```

No `shell` podemos conferir se o mapeamento reverso vou criado.
```python
from app import Child

c1 = Child.query.first()
print(c1.parent)
```

Alternativamente, a opção `backref` pode ser usada em um único `relationship()` ao invés de usar `back_populates`.
```python
class Parent(db.Model):

    __tablename__ = 'parent'

    uuid = db.Column(UUID, primary_key=True)
    children = db.relationship('Child', back_ref='parent')

    def __repr__(self):
        return f'Parent (uuid: {self.uuid})'


class Child(db.Model):

    __tablename__ = 'child'

    uuid = db.Column(UUID, primary_key=True)
    parent_uuid = db.Column(UUID, db.ForeignKey('parent.uuid'))

    def __repr__(self):
        return f'Child (uuid: {self.uuid}, parent_uuid: {self.parent_uuid})'
```

Acessando o `shell` novamente podemos ver que o resultado permanece o mesmo.
```python
from app import Child

c1 = Child.query.first()
print(c1.parent)
```

#### Many To One

#### One To One

#### Many To Many
