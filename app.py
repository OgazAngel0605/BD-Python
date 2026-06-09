import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__, template_folder='.')

MONGO_URI = "mongodb+srv://<usuario>:<password>@cluster.xxxx.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['clinica_dental'] 

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
    db.pacientes.insert_one(datos)
    return redirect('/basedatos_AOOM.html')

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
    db.personal.insert_one(datos)
    return redirect('/basedatos_AOOM.html')

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
    db.examenes.insert_one(datos)
    return redirect('/basedatos_AOOM.html')

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
    db.tratamientos.insert_one(datos)
    return redirect('/basedatos_AOOM.html')



@app.route('/basedatos_AOOM.html')
def ver_base_datos():

    lista_personal = list(db.personal.find())
    lista_pacientes = list(db.pacientes.find())
    lista_examenes = list(db.examenes.find())
    lista_tratamientos = list(db.tratamientos.find())
    
    return render_template('basedatos_AOOM.html', 
                           personal=lista_personal, 
                           pacientes=lista_pacientes, 
                           examenes=lista_examenes, 
                           tratamientos=lista_tratamientos)



@app.route('/eliminar/<coleccion>/<id_doc>')
def eliminar_registro(coleccion, id_doc):
    if coleccion in ['personal', 'pacientes', 'examenes', 'tratamientos']:
        db[coleccion].delete_one({"_id": ObjectId(id_doc)})
    return redirect('/basedatos_AOOM.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
