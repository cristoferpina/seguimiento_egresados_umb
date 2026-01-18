from flask import Flask, Response, jsonify, render_template, request, redirect, session, url_for
import pymysql
import logging
import os
import uuid
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'UMB-UES'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def conectar_db():
    try:
        conexion = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='seguimiento_egresados_umb',
            charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor 
        )
        print("Conexión exitosa a la base de datos")
        return conexion
    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return  None

@app.route('/')
# Define la ruta principal ('/') de la aplicación, es decir, el punto de entrada para los usuarios.
def index():
    conexion = conectar_db()
    return render_template('index.html')

@app.route('/admin')
def dashboard_admin():
    return render_template('dashboard_admin.html')


@app.route('/login_admin', methods=['POST'])
def login_admin():
    username = request.form['useradmin']
    password = request.form['password_coordi']

    conexion = conectar_db()
    if conexion is None:
        return redirect(url_for('index', error = 'db'))
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM coordinador WHERE numero_empleado = %s"
            cursor.execute(sql, (username))
            usuario = cursor.fetchone()
            if usuario:
                if usuario['password'] == password:
                    session['useradmin'] = usuario['numero_empleado']
                    session['nombre'] = usuario['nombre_coordinador']
                    session['fotografia'] = usuario['fotografia']
                    print
                    return redirect(url_for('dashboard_admin'))
                else:
                    return redirect(url_for('index', error='password'))
            else:
                return redirect(url_for('index', error='usuario'))
    finally:
        conexion.close()

@app.route('/login_control', methods=['POST'])
def login_control():
    username = request.form['usercontrol']
    password = request.form['password_control']

    conexion = conectar_db()
    if conexion is None:
        return redirect(url_for('index', error='db'))

    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM control_escolar WHERE numero_empleado = %s"
            cursor.execute(sql, (username,))
            usuario = cursor.fetchone()

            if usuario:
                if usuario['password'] == password:
                    session['usercontrol'] = usuario['numero_empleado']
                    session['nombre'] = usuario['nombre_control']
                    session['fotografia'] = usuario.get('fotografia', None)
                    return redirect(url_for('dashboard_control'))
                else:
                    return redirect(url_for('index', error='password'))
            else:
                return redirect(url_for('index', error='usuario'))
    finally:
        conexion.close()

@app.route('/control')
def dashboard_control():
    if 'usercontrol' not in session:
        return redirect(url_for('index'))

    return render_template('dashboard_control_escolar.html', nombre=session.get('nombre'))

@app.route('/login_ehct', methods=['POST'])
def login_ehct():
    username = request.form['userehct']
    password = request.form['password_ehct']

    conexion = conectar_db()
    if conexion is None:
        return redirect(url_for('index', error='db'))

    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM encargado_hct WHERE numero_empleado = %s"
            cursor.execute(sql, (username,))
            usuario = cursor.fetchone()

            if usuario:
                if usuario['password'] == password:
                    session['userehct'] = usuario['numero_empleado']
                    session['nombre'] = usuario['nombre_encargado']
                    session['perfil'] = usuario['perfil']
                    return redirect(url_for('dashboard_ehct'))
                else:
                    return redirect(url_for('index', error='password'))
            else:
                return redirect(url_for('index', error='usuario'))
    finally:
        conexion.close()

@app.route('/ehct')
def dashboard_ehct():
    if 'userehct' not in session:
        return redirect(url_for('index'))

    return render_template('dashboard_ehct.html', nombre=session.get('nombre'))

##Inicio del app route de egresados

@app.route('/login_egresados', methods=['POST'])
def login_egresados():
    username = request.form['useregresados1']
    password = request.form['password_egresados']

    conexion = conectar_db()
    if conexion is None:
        return redirect(url_for('index', error='db'))

    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM egresados WHERE matricula = %s"
            cursor.execute(sql, (username,))
            usuario = cursor.fetchone()

            if usuario:
                if usuario['password'] == password:
                    session['useregresados1'] = usuario['matricula']
                    session['nombre'] = usuario['nombre_encargado']
                    session['perfil'] = usuario['perfil']
                    return redirect(url_for('dashboard_estudiante'))
                else:
                    return redirect(url_for('index', error='password'))
            else:
                return redirect(url_for('index', error='usuario'))
    finally:
        conexion.close()

@app.route('/egresados')
def dashboard_estudiante():
    if 'useregresados1' not in session:
        return redirect(url_for('index'))

    return render_template('dashboard_estudiante.html', nombre=session.get('nombre'))

##Fin del app route de egresados

@app.route('/consulta_egresados')
def consulta_egresados():
    conexion = conectar_db()
    if conexion:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM egresados"
            cursor.execute(sql)
            egresados = cursor.fetchall()
            return render_template('consulta_egresados.html', egresados=egresados)
    else:
        return "Error al conectar a la base de datos"

@app.route("/consulta_carrera")
def consulta_carrera():
    conexion = conectar_db()
    if not conexion:
        return jsonify({"error": "Error al conectar a la base de datos"}), 500
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT id_carrera, nombre_carrera FROM carreras")
            carreras = cursor.fetchall()
        return jsonify(carreras)
    finally:
        conexion.close()


@app.route("/consulta_ues")
def consulta_ues():
    conexion = conectar_db()
    if not conexion:
        return jsonify({"error": "Error al conectar a la base de datos"}), 500
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT id_ues, nombre_ues FROM ues")
            ues = cursor.fetchall()
        return jsonify(ues)
    finally:
        conexion.close()

@app.route("/consulta_municipio")
def consulta_municipio():
    conexion = conectar_db()
    if not conexion:
        return jsonify({"error": "Error al conectar a la base de datos"}), 500
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT id_municipio, nombre_municipio FROM municipios")
            municipios = cursor.fetchall()
        return jsonify(municipios)
    finally:
        conexion.close()        

@app.route('/consulta_localidades/<int:id_municipio>')
def consulta_localidades(id_municipio):
    conexion = conectar_db()
    if conexion:
        try:
            with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT id_localidad, nombre_localidad 
                    FROM localidades
                    WHERE id_municipio = %s
                    ORDER BY nombre_localidad ASC
                """, (id_municipio,))
                localidades = cursor.fetchall()
            return jsonify(localidades)
        finally:
            conexion.close()
    else:
        return jsonify({'error': 'Error al conectar a la base de datos'}), 500


@app.route('/registrar_egresado', methods=['POST'])
def registrar_egresado():

    try:
      
        data = request.form
        files = request.files

        campos = [
            'nombre_encargado', 'apellido_paterno', 'apellido_materno', 'telefono', 'correo',
            'ni', 'ne', 'estatus_laboral', 'estatus_titulacion', 'matricula',
            'generacion', 'password', 'id_carrera', 'perfil',
            'id_ues', 'id_municipio', 'id_localidad'
        ]

    
        for campo in campos:
            if not data.get(campo):
                return jsonify({"success": False, "message": f"Falta el campo {campo}"}), 400

      
        password_hash = generate_password_hash(data['password'])

      
        foto = files.get('fotografiaegr')
        if not foto:
            return jsonify({"success": False, "message": "Debe subir una fotografía"}), 400

        nombre_foto = f"{uuid.uuid4().hex}_{secure_filename(foto.filename)}"
        ruta_foto = f'uploads/egresados/{nombre_foto}'
        ruta_completa = f'static/{ruta_foto}'
        os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
        foto.save(ruta_completa)

       
        modalidad = data.get('modalidad')
        archivo_modalidad = ''
        if modalidad in ('I', 'II', 'III', 'VI', 'VIII', 'XI'):
            doc = files.get('archivo_modalidad')
            if doc:
                nombre_doc = f"{uuid.uuid4().hex}_{secure_filename(doc.filename)}"
                ruta_doc = os.path.join('static/uploads/modalidades', nombre_doc)
                os.makedirs(os.path.dirname(ruta_doc), exist_ok=True)
                doc.save(ruta_doc)
                archivo_modalidad = ruta_doc

      
        conexion = conectar_db()
        if not conexion:
            return jsonify({"success": False, "message": "No se pudo conectar a la base de datos"}), 500

        with conexion.cursor() as cursor:
            sql = """
                INSERT INTO egresados (
                    nombre_encargado, apellido_paterno, apellido_materno, id_bot, telefono, correo,
                    ni, ne, generacion, modalidad, estatus_laboral, matricula, fotografia, estatus_titulacion, password, perfil, id_carrera, id_ues, id_municipio, id_localidad, documentos
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(sql, (
                data['nombre_encargado'], data['apellido_paterno'], data['apellido_materno'],
                '', data['telefono'], data['correo'], data['ni'], data['ne'],
                data['generacion'], modalidad, data['estatus_laboral'], 
                data['matricula'], ruta_foto, data['estatus_titulacion'], password_hash,
                data['perfil'], data['id_carrera'], data['id_ues'],
                data['id_municipio'], data['id_localidad'], archivo_modalidad
            ))
            conexion.commit()

        return jsonify({"success": True, "message": "Registro exitoso"})

    except Exception as e:
        logging.exception("Error en registrar_egresado")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/eliminar_egresado/<int:id_egresado>', methods=['DELETE', 'POST'])
def eliminar_egresado(id_egresado):
    try:
        conexion = conectar_db()
        if not conexion:
            return jsonify({"success": False, "message": "No se pudo conectar a la base de datos"}), 500

        with conexion.cursor() as cursor:
            # Obtener la fotografía antes de eliminar
            sql = "SELECT fotografia FROM egresados WHERE id_egresado = %s"
            cursor.execute(sql, (id_egresado,))
            egresado = cursor.fetchone()
            
            if egresado and egresado.get('fotografia'):
                foto_path = egresado['fotografia']
                if os.path.exists(foto_path):
                    try:
                        os.remove(foto_path)
                    except Exception as e:
                        logging.warning(f"No se pudo eliminar la foto: {e}")
            
            # Eliminar el egresado
            sql = "DELETE FROM egresados WHERE id_egresado = %s"
            cursor.execute(sql, (id_egresado,))
            conexion.commit()
        
        return jsonify({"success": True, "message": "Egresado eliminado exitosamente"})
    
    except Exception as e:
        logging.exception("Error en eliminar_egresado")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/actualizar_egresado', methods=['POST'])
def actualizar_egresado():
    try:
        data = request.form
        id_egresado = data.get('id_egresado_ac')
        
        if not id_egresado:
            return jsonify({"success": False, "message": "ID de egresado no proporcionado"}), 400
        
        conexion = conectar_db()
        if not conexion:
            return jsonify({"success": False, "message": "No se pudo conectar a la base de datos"}), 500
        
        with conexion.cursor() as cursor:
            sql = """
                UPDATE egresados SET
                    nombre_encargado = %s,
                    apellido_paterno = %s,
                    apellido_materno = %s,
                    telefono = %s,
                    correo = %s,
                    generacion = %s,
                    modalidad = %s,
                    estatus_titulacion = %s,
                    estatus_laboral = %s,
                    id_carrera = %s,
                    id_ues = %s,
                    id_municipio = %s,
                    id_localidad = %s
                WHERE id_egresado = %s
            """
            cursor.execute(sql, (
                data.get('nombre_egresado_ac'),
                data.get('apellido_paterno_ac'),
                data.get('apellido_materno_ac'),
                data.get('telefono_ac'),
                data.get('correo_ac'),
                data.get('generacion_ac'),
                data.get('modalidad'),
                data.get('estatus_titulacion_ac'),
                data.get('estatus_laboral_ac'),
                data.get('id_carrera_ac'),
                data.get('id_ues_ac'),
                data.get('id_municipio_ac'),
                data.get('id_localidad_ac'),
                id_egresado
            ))
            conexion.commit()
        
        # Obtener los datos actualizados para devolver al frontend
        conexion = conectar_db()
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM egresados WHERE id_egresado = %s"
            cursor.execute(sql, (id_egresado,))
            egresado = cursor.fetchone()
        
        return jsonify({
            "success": True, 
            "message": "Egresado actualizado exitosamente",
            "egresado": egresado
        })
    
    except Exception as e:
        logging.exception("Error en actualizar_egresado")
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    conexion = conectar_db()
    if conexion:
        conexion.close()
    app.run(debug=True, host='0.0.0.0', port=5000)