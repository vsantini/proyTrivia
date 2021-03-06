from apptrivia import app, db
import random, datetime
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

from flask_principal import AnonymousIdentity, RoleNeed, UserNeed, identity_loaded, identity_changed, Identity

from models.models import Categoria, Pregunta, Respuesta, User

from flask import render_template, redirect, url_for, flash, request, session, jsonify, current_app, g

from forms.login import LoginForm
from forms.register import RegisterForm

# para poder usar Flask-Login
login_manager = LoginManager(app)


@app.route('/')
@app.route('/index')
def index():
    session.clear()

    session['time'] = datetime.datetime.now()
    session['ya_gano'] = False
    return redirect(url_for('login'))

@app.route('/trivia/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mostrarcategorias'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            # funcion provista por Flask-Login, el segundo parametro gestion el "recordar"
            login_user(user, remember=form.remember_me.data)
            #agrego a identity
            app_actual = current_app._get_current_object()
            identity_changed.send(app_actual, identity=Identity(user.id))

            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('mostrarcategorias')
            return redirect(next_page)

        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('login'))
    # no loggeado, dibujamos el login con el form vacio
    return render_template('login.html', form=form, subtitulo="Bienvenidos a la trivia!!", texto="Diviertanse!! Juegue con sus amigos")



@app.route('/trivia/categorias', methods=['GET'])
@login_required
def mostrarcategorias():
    categorias = Categoria.query.all()
    #vengo de que gane
    if (session['ya_gano']):
        #inicializo variables
        session['time'] = datetime.datetime.now()
        for cat in categorias:
            session[str(cat.id)] = False
        session['ya_gano'] = False
    return render_template('categorias.html', categorias=categorias, subtitulo="Seleccione categoria")


@app.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
@login_required
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)
    return render_template('preguntas.html', categoria=categ, pregunta=pregunta)


@app.route('/trivia/<int:id_pregunta>/resultado/<int:id_respuesta>', methods=['GET'])
@login_required
def mostrarrespuesta(id_pregunta, id_respuesta):
    pregunta =  Pregunta.query.get(id_pregunta)
    respuesta = Respuesta.query.get(id_respuesta)
    #session['categorias'][str(pregunta.categoria_id)] = respuesta.resultado
    #session['x'] = 'TEST'
    if respuesta.resultado:
        #Grabo en la sesion que esta categoria esta ok
        session[str(pregunta.categoria_id)] = True
        if todasCatOk():
            tiempo = datetime.datetime.now() - session['time']
            session['ya_gano'] = True
            win_user = User.get_by_id(current_user.id)
            if (best_time(win_user, new_time=tiempo)):
                win_user.best_time = tiempo
                db.session.commit()
                users = User.query.all()
                return render_template('finJuego.html', tiempo= tiempo, users=users)
    return render_template('resultado.html', pregunta = pregunta, resultado=respuesta.resultado)

def best_time(user, new_time):
    if (user.best_time == None or user.best_time > new_time):
        return True
    else:
        return True;


def todasCatOk():
    categorias = Categoria.query.all();
    for cat in categorias:
        if ((not (str(cat.id) in session)) or (session[str(cat.id)]) == False):
            return False
    return True


#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route("/trivia/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            flash('El email {} ya está siendo utilizado por otro usuario'.format(email))
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=username, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            return redirect(url_for('index'))

    return render_template("register.html", form=form)


@app.route('/trivia/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

##############################
#            Errores:        #
##############################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def servererror(e):
    return render_template('500.html')

@app.errorhandler(403)
def authError(e):
    return render_template('403.html')

@app.errorhandler(401)
def authError2(e):
    return render_template('403.html')


##############################
#            PRINCIPAL :     #
##############################

# Flask-Principal: Agregamos las necesidades a una identidad, una vez que se loguee el usuario.
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Seteamos la identidad al usuario
    identity.user = current_user

    # Agregamos una UserNeed a la identidad, con el id del usuario actual.
    if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

    # Agregamos a la identidad la lista de roles que posee el usuario actual.
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.rolename))







