#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apptrivia import db
from models.models import  User, Role

# agregamos usuarios
u1 = User(name='admin', email='admin@antel.com.uy')
u2 = User(name='user2', email='bla2@antel.com.uy')
u1.set_password("admin123")
u2.set_password("bla2")
db.session.add_all([u1, u2])
#agregamos roles a los que estaban
u3 = User.query.filter_by(email="vsantini@antel.com.uy",).first()
u4 = User.query.filter_by(email="juan@antel.com.uy",).first()

db.session.commit()

db.session.add_all(
         [Role(rolename='admin', user=u1),
          Role(rolename='user', user=u1),  # multiples roles
          Role(rolename='user', user=u2),
          Role(rolename='user', user=u3),
          Role(rolename='user', user=u4)
          ])
db.session.commit()