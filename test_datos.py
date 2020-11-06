#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apptrivia import db
from models.models import Categoria, Pregunta, User, Respuesta

db.drop_all()
db.create_all()

# categorias
c_geogra = Categoria(descripcion="Geografía")
c_deporte = Categoria(descripcion="Deportes")

# preguntas
q_Laos = Pregunta(text="¿Cuál es la capital de Laos?",categoria=c_geogra)
q_Armenia = Pregunta(text="¿Cuál es la población aproximada de Armenia?",categoria=c_geogra)
q_Mundial = Pregunta(text="¿En qué país se jugó la Copa del Mundo de 1962?",categoria=c_deporte)

# respuestas
r_Laos1 = Respuesta(text="Montevideo",pregunta=q_Laos,resultado=False)
r_Laos2 = Respuesta(text="Quito",pregunta=q_Laos,resultado=False)
r_Laos3 = Respuesta(text="Vientián",pregunta=q_Laos,resultado=True)

r_Armenia1 = Respuesta(text="5.035.000",pregunta=q_Armenia,resultado=False)
r_Armenia2 = Respuesta(text="2.965.000",pregunta=q_Armenia,resultado=True)
r_Armenia3 = Respuesta(text="4.325.000",pregunta=q_Armenia,resultado=False)

r_Mundial1 = Respuesta(text="Argentina",pregunta=q_Mundial,resultado=False)
r_Mundial2 = Respuesta(text="Chile",pregunta=q_Mundial,resultado=True)
r_Mundial3 = Respuesta(text="Brasil",pregunta=q_Mundial,resultado=False)

#Usuarios
q_u1 = User(name = "valeria", email = "vsantini@antel.com.uy", is_admin = True)
# el pass lo seteamos con el método set_password para que se guarde con hash
q_u1.set_password("admin1");
# por defecto, el usuario no es admin
q_u2 = User(name = "juan", email = "juan@antel.com.uy")
q_u2.set_password("juan");

db.session.add(c_geogra)
db.session.add(c_deporte)



db.session.add(q_u1)
db.session.add(q_u2)
db.session.commit()

#db.session.add(q_Laos)
#db.session.add(q_Armenia)
#db.session.add(q_Mundial)

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

