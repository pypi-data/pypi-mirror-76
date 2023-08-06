# Zunzun Framework

Zunzun is a Python framework that uses other libraries to implement its features. Ones of them are:

- [injector](https://pypi.org/project/injector/) It's used to Dependency Injection.
- [click](https://pypi.org/project/click/) For creating commands line interface.
- [blinker](https://pypi.org/project/blinker/) Provides a fast dispatching system.
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/) The Python SQL Toolkit and Object Relational Mapper.

## Create an application

1. Clone the example application from https://github.com/aprezcuba24/zunzun_app
2. Create .env file base on .env.example
    - Configure database configuration
3. You can use vscode to open the application in a container.
4. Star the application using this command.
```
python manage.py core runserver
```
5. Open the browser in this url `http://localhost:8001/`

## Controller
We can create two types of controller, a function controller, or a class controller.

### Function controller

```python
from main import router


@router.post("/")
def register():
    return "Register"
```

### Class controller
To create a class controller we can use the following command

```
python zunzun.py maker controller Role --route="/role"
```

Where "Role" will be the name of the controller and "/role" the path to access the controller.

The command will generate the file `app/controllers/role.py`

```python
from zunzun import Response
from main import router

class RoleController:
    @router.get('/role')
    def index(self):
        return "RoleController Index"
```
In the class controller or in the function controller we can inject dependencies.
For example, if we have a service named "PaypalService" we can inject it, with the following code.
```python
from main import router
from app.services import PaypalService


@router.post("/")
def register(paypal: PaypalService):
    paypal.call_a_method()
    return "Register"
```
In a controller class, we can inject dependencies in the constructor or in any function.
```python
from zunzun import Response
from main import router
from app.services import PaypalService, SomeService

class RoleController:
    def __init__(self, some_service: SomeService):
        self.some_service = some_service

    @router.get('/role')
    def index(self, paypal: PaypalService):
        return "RoleController Index"
```
## Commands
Commands allow us to implement command line features. To do that we can use the following command.
```
python manager.py maker command role
```
Where "role" will be the name of the command. This command will create the following file `app/commands/role.py`.
```python
import click
from injector import singleton, inject
from zunzun import Command


@singleton
class roleCommand(Command):
    @inject
    def __init__(self):
        super().__init__("role")
        self.add_option("--some-option")
        self.add_argument("some-argument")

    def handle(self, some_option, some_argument):
        click.echo(
            f"roleCommand [some_argument: {some_argument}] [some_option: {some_option}]"
        )
```
To use the new command we can type the following in the console.
```
python manager.py app role "An argument value" --some-option="An option value"
```
## Listener
The listener allows us to implement the Event-Dispatcher pattern. To create a new listener with its signal we can use the following command.
```
python manager.py maker listener Role Role
```
Where the first word "Role" will be the listener name and the second will be the signal name.
The command will generate the following files:

- Signal file `app/signals/role.py`
- Listener file `app/listeners/role.py`

The signal file will have this code.
```python
from zunzun import Signal
from injector import singleton


@singleton
class RoleSignal(Signal):
    pass
```
The listener file will have this code.
```python
from injector import singleton


@singleton
class RoleListener:
    def __call__(self, sender, **kwargs):
        pass
```
## Services
We can create classes to implement any logic that we need. For example to create a service to integrate Paypal we can use the following command.
```
python manager.py maker service Paypal
```
The command will create the file `app/services/paypal.py` with the following code.
```python
from injector import singleton, inject


@singleton
class PaypalService:
    @inject
    def __init__(self):
        pass
```
## ORM
Zunzun uses **SQLAlchemy** to implement the ORM features. The framework uses two type of classes.

- The model represents a single row in the database.
- The repository is a class to implement the queries to the database.

To create the model and its repository we can use the following command.
```
python manager.py orm model_create Role
```
The model will be
```python
from zunzun import orm
from sqlalchemy import Column, Integer


class Role(orm.BaseModel):
    __tablename__ = "Role"
    id = Column(Integer, primary_key=True)
```
The repository will be
```python
from injector import singleton
from zunzun import orm
from app.model import Role


@singleton
class RoleRepository(orm.BaseRepository):
    def new(self, **kwargs):
        return Role(**kwargs)
```
## Dependency injection
The framework uses this pattern to manage dependencies. To know how you can use see the documentation on [inject](https://pypi.org/project/injector/)