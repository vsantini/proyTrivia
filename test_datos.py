#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apptrivia import db
from models.models import Categoria, Pregunta, User, Respuesta

db.drop_all()
db.create_all()

# categorias
c_geogra = Categoria(descripcion="Geografía")
c_deporte = Categoria(descripcion="Deportes")
c_historia = Categoria(descripcion="Historia")

# preguntas
q_Laos = Pregunta(text="¿Cuál es la capital de Laos?",categoria=c_geogra)
q_Armenia = Pregunta(text="¿Cuál es la población aproximada de Armenia?",categoria=c_geogra)
q_Mediterraneo = Pregunta(text="¿Cuál de estos países no tiene acceso al Mar Mediterráneo?",categoria=c_geogra)

q_Mundial = Pregunta(text="¿En qué país se jugó la Copa del Mundo de 1962?",categoria=c_deporte)
q_Rugby = Pregunta(text="¿Cuántos jugadores componen un equipo de rugby?", categoria=c_deporte)
q_Tenis = Pregunta(text="¿Cuántos Grand Slam tiene Roger Federer?", categoria=c_deporte)

q_Imperio = Pregunta(text="¿Cuál era la capital del imperio INCA?",categoria=c_historia)
q_Emperador = Pregunta(text="¿Quién fue el primer emperador romano?",categoria=c_historia)
q_Hitler= Pregunta(text="¿En qué país nació Adolf Hitler?",categoria=c_historia)

# respuestas
r_Laos1 = Respuesta(text="Montevideo",pregunta=q_Laos,resultado=False)
r_Laos2 = Respuesta(text="Quito",pregunta=q_Laos,resultado=False)
r_Laos3 = Respuesta(text="Vientián",pregunta=q_Laos,resultado=True)

r_Armenia1 = Respuesta(text="5.035.000",pregunta=q_Armenia,resultado=False)
r_Armenia2 = Respuesta(text="2.965.000",pregunta=q_Armenia,resultado=True)
r_Armenia3 = Respuesta(text="4.325.000",pregunta=q_Armenia,resultado=False)

r_Mediterraneo1 = Respuesta(text="Eslovenia",pregunta=q_Mediterraneo,resultado=False)
r_Mediterraneo2 = Respuesta(text="Serbia",pregunta=q_Mediterraneo,resultado=True)
r_Mediterraneo3 = Respuesta(text="Chipre",pregunta=q_Mediterraneo,resultado=False)

r_Mundial1 = Respuesta(text="Argentina",pregunta=q_Mundial,resultado=False)
r_Mundial2 = Respuesta(text="Chile",pregunta=q_Mundial,resultado=True)
r_Mundial3 = Respuesta(text="Brasil",pregunta=q_Mundial,resultado=False)

r_Rugby1 = Respuesta(text="17",pregunta=q_Rugby,resultado=False)
r_Rugby2 = Respuesta(text="13",pregunta=q_Rugby,resultado=False)
r_Rugby3 = Respuesta(text="15",pregunta=q_Rugby,resultado=True)

r_Tenis1 = Respuesta(text="22",pregunta=q_Tenis,resultado=False)
r_Tenis2 = Respuesta(text="20",pregunta=q_Tenis,resultado=True)
r_Tenis3 = Respuesta(text="15",pregunta=q_Tenis,resultado=False)

r_Imperio1 = Respuesta(text="Cuzco",pregunta=q_Imperio,resultado=True)
r_Imperio2 = Respuesta(text="Quito",pregunta=q_Imperio,resultado=False)
r_Imperio3 = Respuesta(text="Machu Picchu",pregunta=q_Imperio,resultado=False)

r_Emperador1 = Respuesta(text="Julio Cesar",pregunta=q_Emperador,resultado=False)
r_Emperador2 = Respuesta(text="Nerón",pregunta=q_Emperador,resultado=False)
r_Emperador3 = Respuesta(text="Cesar Augusto",pregunta=q_Emperador,resultado=True)

r_Hitler1 = Respuesta(text="Austria",pregunta=q_Hitler,resultado=True)
r_Hitler2 = Respuesta(text="Alemania",pregunta=q_Hitler,resultado=False)
r_Hitler3 = Respuesta(text="Holanda",pregunta=q_Hitler,resultado=False)

#Usuarios
q_u1 = User(name = "valeria", email = "vsantini@antel.com.uy", is_admin = True)
# el pass lo seteamos con el método set_password para que se guarde con hash
q_u1.set_password("admin1");
# por defecto, el usuario no es admin
q_u2 = User(name = "juan", email = "juan@antel.com.uy")
q_u2.set_password("juan");

db.session.add(c_geogra)
db.session.add(c_deporte)
db.session.add(c_historia)

db.session.add(q_u1)
db.session.add(q_u2)
db.session.commit()

# creamos otros usuarios (…) y los recorremos
categorias = Categoria.query.all()
for c in categorias:
    print(c.id, c.descripcion)
    # para cada categoria, obtenemos sus preguntas y las recorremos
    for p in c.preguntas:
        print(p.id, p.text)


cat = Categoria.query.get(1)
print(cat)

