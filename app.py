from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Cargar configuraciones del archivo .env
load_dotenv()

# Crear una instancia de Flask
app = Flask(__name__)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Definir el modelo de datos
class Alumno(db.Model):
    __tablename__ = 'alumnos'
    
    no_control = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    ap_paterno = db.Column(db.String, nullable=False)
    ap_materno = db.Column(db.String, nullable=False)
    semestre = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, no_control, nombre, ap_paterno, ap_materno, semestre):
        self.no_control = no_control
        self.nombre = nombre
        self.ap_paterno = ap_paterno
        self.ap_materno = ap_materno
        self.semestre = semestre

# Rutas de la API
# Crear un nuevo alumno
@app.route('/alumnos', methods=['POST'])
def create_alumno():
    data = request.json
    nuevo_alumno = Alumno(
        no_control=data['no_control'],
        nombre=data['nombre'],
        ap_paterno=data['ap_paterno'],
        ap_materno=data['ap_materno'],
        semestre=data['semestre']
    )
    db.session.add(nuevo_alumno)
    db.session.commit()
    return jsonify({'mensaje': 'Alumno creado con éxito'}), 201

# Obtener un alumno por su número de control
@app.route('/alumnos/<no_control>', methods=['GET'])
def get_alumno(no_control):
    alumno = Alumno.query.get(no_control)
    if alumno:
        return jsonify({
            'no_control': alumno.no_control,
            'nombre': alumno.nombre,
            'ap_paterno': alumno.ap_paterno,
            'ap_materno': alumno.ap_materno,
            'semestre': alumno.semestre
        }), 200
    return jsonify({'mensaje': 'Alumno no encontrado'}), 404

# Listar todos los alumnos
@app.route('/alumnos', methods=['GET'])
def list_alumnos():
    alumnos = Alumno.query.all()
    result = [
        {
            'no_control': alumno.no_control,
            'nombre': alumno.nombre,
            'ap_paterno': alumno.ap_paterno,
            'ap_materno': alumno.ap_materno,
            'semestre': alumno.semestre
        } for alumno in alumnos
    ]
    return jsonify(result), 200

# Actualizar un alumno
@app.route('/alumnos/<no_control>', methods=['PUT'])
def update_alumno(no_control):
    data = request.json
    alumno = Alumno.query.get(no_control)
    if alumno:
        alumno.nombre = data['nombre']
        alumno.ap_paterno = data['ap_paterno']
        alumno.ap_materno = data['ap_materno']
        alumno.semestre = data['semestre']
        db.session.commit()
        return jsonify({'mensaje': 'Alumno actualizado con éxito'}), 200
    return jsonify({'mensaje': 'Alumno no encontrado'}), 404

# Borrar un alumno
@app.route('/alumnos/<no_control>', methods=['DELETE'])
def delete_alumno(no_control):
    alumno = Alumno.query.get(no_control)
    if alumno:
        db.session.delete(alumno)
        db.session.commit()
        return jsonify({'mensaje': 'Alumno borrado con éxito'}), 200
    return jsonify({'mensaje': 'Alumno no encontrado'}), 404

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
