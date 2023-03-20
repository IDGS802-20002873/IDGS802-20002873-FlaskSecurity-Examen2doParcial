import os
import uuid
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from project.models import Role, productos

from werkzeug.utils import secure_filename
from . import db

main = Blueprint('main',__name__)

@main.errorhandler(404)
def error_404_handler(e):
        return render_template('404.html'), 404

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/administrador')
@login_required
@roles_required('admin')
def admin():
   
    producto= productos.query.all()
    return render_template('productos.html',producto=producto)


@main.route('/administrador', methods=['POST'])
@login_required
@roles_required('admin')
def admin_post():
    producto= productos.query.all()
    nombre = request.form.get('txtNombre')
    marca = request.form.get('txtMarca')
    precio = request.form.get('txtPrecio')
    img=str(uuid.uuid4())+'.png'
    imagen=request.files['imagen']
    ruta_imagen = os.path.abspath('project\\static\\img')
    imagen.save(os.path.join(ruta_imagen,img))       
  
    new_product= productos(nombre,marca,precio,img)
    
    db.session.add(new_product)
    
    db.session.commit()

    flash('El producto se guardo correctamente')
    
    return redirect(url_for('main.admin'))



@main.route('/delete/<id>')
@login_required
def delete(id):
    producto=productos.query.get(id)
    imagen=productos.query.get(id)
    os.remove('project/static/img/{}'.format(str(imagen.img)))
    db.session.delete(producto)
    db.session.commit()
    flash('Se eliminó correctamente')
    return redirect(url_for('main.admin'))

@main.route('/update/<id>')
@login_required
def update(id):
    producto=productos.query.get(id)
    imagen=productos.query.get(id)
    print(producto.id)
    return render_template('productos.html',nombre=producto.name,precio=int(producto.precio),
                           marca=str(producto.marca),
                           imagen=imagen.img, update=True,
                           id=producto.id)
   
@main.route('/updateCom/<id>',methods=['POST'])
@login_required
def updateComfim(id):
           
    img=request.form.get('img')
    os.remove('project/static/img/{}'.format(str(img)))
    imagen=request.files['imagen']
    ruta_imagen = os.path.abspath('project\\static\\img')
    imagen.save(os.path.join(ruta_imagen,img))       
    
    idproducto=id
    producto=productos.query.get(idproducto)
    producto.name = request.form.get('txtNombre')
    producto.marca = request.form.get('txtMarca')
    producto.precio = request.form.get('txtPrecio')
    db.session.commit()  
    
    flash('El producto se modificó correctamente')
    return redirect(url_for('main.admin'))
   
@main.route('/galeria')
@login_required
def galeria():
    producto= productos.query.all()
    
    if len(producto )==0:
       producto=0
    
    print(current_user.admin)
        
    return render_template('galeria.html',producto=producto)



    







