import os
from flask import Flask, redirect, url_for, request, g

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_principal import Principal, Permission, RoleNeed
from flask_admin import AdminIndexView
from flask_bootstrap import Bootstrap

# instancia Flask
app = Flask(__name__)
#admin = Admin(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or \
    'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

# lee la config desde el archivo config.py
app.config.from_pyfile('config.py')

# inicializa la base de datos con la config leida
db = SQLAlchemy(app)

db.init_app(app)
migrate = Migrate()
# Se inicializa el objeto migrate
migrate.init_app(app, db)

bootstrap = Bootstrap(app)

class MyModelView(ModelView):
    def is_accessible(self):
        #return current_user.is_authenticated
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        return has_auth and has_perm

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

#agrego esto y se rompe todo
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        return has_auth and has_perm

admin = Admin(app, index_view=MyAdminIndexView())


# Flask-Principal: ---  Setup ------------------------------------
principal = Principal()
principal.init_app(app)

# Flask-Principal: Creamos un permiso con una sola necesidad que debe ser satisfecho para entrar al admin.
admin_permission = Permission(RoleNeed('admin'))



# rutas disponibles
from routes import *
from models.models import Categoria, Pregunta,User, Respuesta
from flask_login import LoginManager, current_user

# Los modelos que queremos mostrar en el admin
admin.add_view(MyModelView(Categoria, db.session))
admin.add_view(MyModelView(Pregunta, db.session))
admin.add_view(MyModelView(Respuesta, db.session))
admin.add_view(MyModelView(User, db.session))

# subimos el server (solo cuando se llama directamente a este archivo)
if __name__ == '__main__':
    app.run(debug=True)