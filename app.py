import os
from flask import Flask, render_template, redirect, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__, template_folder='.') # Indica que los HTML están en la raíz

@app.route('/')
def inicio():
    return render_template('inicio_AOOM.html')

@app.route('/<pagina>.html')
def cargar_paginas(pagina):
    # Si intentan cargar la base de datos de manera directa, los redirigimos a la función correcta
    if pagina == 'basedatos_AOOM':
        return redirect('/basedatos_AOOM.html')
    return render_template(f'{pagina}.html')

# Conexión real a tu clúster de MongoDB Atlas
MONGO_URI = "mongodb+srv://dentista_dentaglat_db_aoom:UuizaYbYcFT55lb6@dentistadentaglat.4fgdqmm.mongodb.net/?appName=DentistaDentaGlat"
client = MongoClient(MONGO_URI)
db = client['clinica_dental'] # Nombre de tu base de datos

# =================================================================
# --- RUTAS PARA INSERTAR DATOS ---
# =================================================================

@app.route('/api/pacientes', methods=['POST'])
def registrar_paciente():
    datos = {
        "id_paciente": request.form.get('id_paciente'),
        "nombre_paciente": request.form.get('nombre_paciente'),
        "edad_paciente": request.form.get('edad_paciente'),
        "genero_paciente": request.form.get('genero_paciente'),
        "fecha_registro": request.form.get('fecha_registro'),
        "dom_actual": request.form.get('dom_actual'),
        "ocupacion": request.form.get('ocupacion'),
        "tutor": request.form.get('tutor'),
        "tel": request.form.get('tel'),
        "notas": request.form.get('notas')
    }
    db['pacientes'].insert_one(datos)
    return redirect('/pacientes_AOOM.html')

@app.route('/api/personal', methods=['POST'])
def registrar_personal():
    datos = {
        "nombre_personal": request.form.get('nombre_personal'),
        "genero_personal": request.form.get('genero_personal'),
        "edad_personal": request.form.get('edad_personal'),
        "fecha_nacimiento": request.form.get('fecha_nacimiento'),
        "lugar_nacimiento": request.form.get('lugar_nacimiento'),
        "cargo": request.form.get('cargo'),
        "especialidad": request.form.get('especialidad'),
        "tel_personal": request.form.get('tel_personal'),
        "email": request.form.get('email')
    }
    db['personal'].insert_one(datos)
    return redirect('/personal_AOOM.html')

@app.route('/api/examenes', methods=['POST'])
def registrar_examen():
    datos = {
        "id_exa_paciente": request.form.get('id_exa_paciente'),
        "fecha_hora": request.form.get('fecha_hora'),
        "motivo_consulta": request.form.get('motivo_consulta'),
        "signos_vitales": request.form.get('signos_vitales'),
        "evaluacion_odontologica": request.form.get('evaluacion_odontologica'),
        "examen_intra_extra": request.form.get('examen_intra_extra'),
        "med_evaluador": request.form.get('med_evaluador'),
        "estatus": request.form.get('estatus')
    }
    db['examenes'].insert_one(datos)
    return redirect('/examenes_AOOM.html')

@app.route('/api/tratamientos', methods=['POST'])
def registrar_tratamiento():
    datos = {
        "id_p": request.form.get('id_p'),
        "fecha_consulta": request.form.get('fecha_consulta'),
        "diagnostico": request.form.get('diagnostico'),
        "tratamiento_realizado": request.form.get('tratamiento_realizado'),
        "materiales_utilizados": request.form.get('materiales_utilizados'),
        "operador": request.form.get('operador')
    }
    db['tratamientos'].insert_one(datos)
    return redirect('/segtra_AOOM.html')


# =================================================================
# --- RUTA PARA MOSTRAR LAS TABLAS ACTUALIZADAS ---
# =================================================================

@app.route('/basedatos_AOOM.html')
def ver_base_datos():
    lista_personal = []
    for doc in db['personal'].find():
        doc['id'] = str(doc['_id']) # Transforma el ObjectId de Mongo a texto plano para el HTML
        lista_personal.append(doc)

    lista_pacientes = []
    for doc in db['pacientes'].find():
        doc['id'] = str(doc['_id'])
        lista_pacientes.append(doc)

    lista_examenes = []
    for doc in db['examenes'].find():
        doc['id'] = str(doc['_id'])
        lista_examenes.append(doc)

    lista_tratamientos = []
    for doc in db['tratamientos'].find():
        doc['id'] = str(doc['_id'])
        lista_tratamientos.append(doc)

    return render_template('basedatos_AOOM.html', 
                           personal=lista_personal, 
                           pacientes=lista_pacientes, 
                           examenes=lista_examenes, 
                           tratamientos=lista_tratamientos)


# =================================================================
# --- RUTA PARA EDITAR / ACTUALIZAR UN REGISTRO (MONGODB) ---
# =================================================================

@app.route('/api/editar/<coleccion>/<id_doc>', methods=['POST'])
def editar_registro(coleccion, id_doc):
    if coleccion in ['personal', 'pacientes', 'examenes', 'tratamientos']:
        datos_actualizados = {}
        formulario = request.form
        
        for clave, valor in formulario.items():
            valor_limpio = valor.strip() if valor else ""
            if valor_limpio != "":
                datos_actualizados[clave] = valor_limpio
        
        if datos_actualizados:
            # En MongoDB usamos update_one con el operador $set y su ObjectId correspondiente
            db[coleccion].update_one(
                {"_id": ObjectId(id_doc)}, 
                {"$set": datos_actualizados}
            )
        
    return redirect('/basedatos_AOOM.html')


# =================================================================
# --- RUTA PARA ELIMINAR UN REGISTRO (MONGODB) ---
# =================================================================

@app.route('/eliminar/<coleccion>/<id_doc>')
def eliminar_registro(coleccion, id_doc):
    if coleccion in ['personal', 'pacientes', 'examenes', 'tratamientos']:
        db[coleccion].delete_one({"_id": ObjectId(id_doc)})
        
    return redirect('/basedatos_AOOM.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)