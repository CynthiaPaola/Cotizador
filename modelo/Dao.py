from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, INTEGER, String, FLOAT
from sqlalchemy.orm import relationship

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db=SQLAlchemy()

#Flores
class flores(db.Model):
    __tablename__='flores'
    idFlor=Column(INTEGER, primary_key=True)
    nombre=Column(String)
    precioUnitario=Column(FLOAT)
    precioPaquete=Column(FLOAT)

    def consultaIndividual(self,id):
        return self.query.get(id)
    
    def consultaGeneral(self):
        return self.query.all()
    
    def editar(self):
        db.session.merge(self)
        db.session.commit()    

    def agregar(self):
        db.session.add(self)
        db.session.commit()  

    def eliminarCate(self,id):
        c=self.consultaIndividual(id)
        db.session.delete(c)
        db.session.commit()        

    def eliminacionLogica(self,id):
        c=self.consultaIndividual(id)
        c.estatus='Inactivo'
        c.editar() 

class insumos(db.Model):
    __tablename__='insumos'
    id_insumo=Column(INTEGER, primary_key=True)

# Usuario
class Usuario(UserMixin,db.Model):
    __tablename__='usuario'
    idUsuario=Column(INTEGER,primary_key=True)
    nombreCompleto=Column(String,nullable=False)
    user=Column(String,unique=True)
    password_hash=Column(String(128),nullable=False)
    tipo=Column(String,nullable=False)

    @property #Implementa el metodo Get (para acceder a un valor)
    def password(self):
        raise AttributeError('El password no tiene acceso de lectura')

    @password.setter #Definir el metodo set para el atributo password_hash
    def password(self,password):#Se informa el password en formato plano para hacer el cifrado
        print('password '+password)
        self.password=generate_password_hash(password)
        print(' hash '+self.password_hash)


    def validarPassword(self,password):
        print('password '+password)
        print(' hash '+self.password)

        return check_password_hash(self.password_hash,password)
    #Definición de los métodos para el perfilamiento
    def is_authenticated(self):
        return True

    def is_active(self):
        if self.estatus=='Activo':
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idUsuario

    def is_admin(self):
        if self.tipo=='Administrador':
            return True
        else:
            return False
    
    def is_vendedor(self):
        if self.tipo=='Vendedor':
            return True
        else:
            return False
    
    #Definir el método para la autenticacion
    def validar(self,user,password):
        usuario=Usuario.query.filter(Usuario.user==user).first()
        #print(usuario.email)
        if usuario!=None and usuario.validarPassword(password) and usuario.is_active():
            return usuario
        else:
            return None
    #Método para agregar una cuenta de usuario
    def agregar(self):
        db.session.add(self)
        db.session.commit()


    