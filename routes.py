# importamos la instancia de Flask (app)
from apptrivia import app
from flask import session
import random, datetime

# importamos los modelos a usar
from models.models import Categoria, Pregunta, Respuesta

from flask import render_template, redirect, url_for

@app.route('/')
def index():
    session.clear()

    session['time'] = datetime.datetime.now()
    #TODO: cargar por las categorias que estan en la base todas con False
    #session['categorias'] = {1: False, 2: False}

    #return "<h2>Bienvenidos a la Trivia</h2> "
    return redirect(url_for('mostrarcategorias'))

@app.route('/trivia/categorias', methods=['GET'])
def mostrarcategorias():
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)


@app.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)
    return render_template('preguntas.html', categoria=categ, pregunta=pregunta)


@app.route('/trivia/<int:id_pregunta>/resultado/<int:id_respuesta>', methods=['GET'])
def mostrarrespuesta(id_pregunta, id_respuesta):
    pregunta =  Pregunta.query.get(id_pregunta)
    respuesta = Respuesta.query.get(id_respuesta)
    #session['categorias'][str(pregunta.categoria_id)] = respuesta.resultado
    #session['x'] = 'TEST'
    if respuesta.resultado:
        #Grabo en la sesion que esta categoria esta ok
        session[str(pregunta.categoria_id)]=True
        if todasCatOk():
            tiempo = datetime.datetime.now() - session['time']
            return render_template('finJuego.html', tiempo= tiempo )
    return render_template('resultado.html', pregunta = pregunta, resultado=respuesta.resultado)

def todasCatOk():
    categorias = Categoria.query.all();
    for cat in categorias:
        if not (str(cat.id) in session):
            return False
    return True
