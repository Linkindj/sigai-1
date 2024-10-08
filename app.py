import io
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, send_file, send_from_directory, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, CSRFError 
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DateField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email
from datetime import datetime
from flask_mail import Mail, Message,Attachment
import openpyxl
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')
    
app = Flask (__name__, template_folder = template_dir)

app.secret_key=os.urandom(24)

#csrf = CSRFProtect(app)

class formUser(FlaskForm):
# Formulario para registro de vivienda
    localizacion=StringField('Localización', render_kw={'class': 'form-control mb-2 sm' }, validators=[DataRequired()])
    fecha_entrevista=DateField('Fecha entrevista', render_kw={'class': 'form-control mb-2 sm'})
    nombre_promotor=StringField('Nombre promotor', render_kw={'class': 'form-control mb-2 sm' }, validators=[DataRequired()])
    direccion=StringField('Dirección', render_kw={'class': 'form-control mb-2 sm' })
    telefono_fijo=StringField('Teléfono fijo', render_kw={'class': 'form-control mb-2'}, validators=[DataRequired()])
    telefono_celular=StringField('Teléfono celular', render_kw={'class': 'form-control mb-3'}, validators=[DataRequired()])
    distancia=StringField('Distancia', render_kw={'class': 'form-control mb-3'}, validators=[DataRequired()])

    #Formulario para registro de familias   
    apellidos_familia=StringField('telefono', render_kw={'class': 'form-control mb-3'}, validators=[DataRequired()])

    #formulario para registro de personas
    num_documento=StringField('documento', render_kw={'class': 'form-control mb-3','placeholder': 'Número de documento'}, validators=[DataRequired()])
    p_nombre=StringField('p_nombre', render_kw={'class': 'form-control mb-3','placeholder': 'Primero nombre'}, validators=[DataRequired()])
    s_nombre=StringField('s_nombre', render_kw={'class': 'form-control mb-3','placeholder': 'Segundo nombre'}, validators=[DataRequired()])
    p_apellido=StringField('p_apellido', render_kw={'class': 'form-control mb-3','placeholder': 'Primer apellido' }, validators=[DataRequired()])
    s_apellido=StringField('s_apellido', render_kw={'class': 'form-control mb-3' ,'placeholder': 'Segundo apellido' }, validators=[DataRequired()])
    correo=EmailField('correo', render_kw={'class': 'form-control mb-3','placeholder': 'Correo eléctronico' }, validators=[DataRequired()])
    telefono=StringField('telefono', render_kw={'class': 'form-control mb-3' ,'placeholder': 'Teléfono' }, validators=[DataRequired()])
    observacion= TextAreaField('observacion', render_kw={'class': 'form-control mb-3','placeholder': 'Observaciones'}, validators=[DataRequired()])
    #tipo de evaluacion
    c_previa=StringField('citas previas', render_kw={'class': 'form-control mb-3'}, validators=[DataRequired()])
    estado=StringField('Estado', render_kw={'class': 'form-control mb-3'}, validators=[DataRequired()])
    cargo=StringField('Cargo', render_kw={'class': 'form-control mb-3'}, validators=[DataRequired()])

    save=SubmitField('save', render_kw={'class': 'btn btn-primary mb3 mt-4'})

# Formulario para Login 
    username=StringField('username', render_kw={'class': 'form-control mb-3','placeholder': 'Ingrese su usuario' }, validators=[DataRequired()])
    password=PasswordField('password', render_kw={'class': 'form-control mb-3','placeholder': 'Ingrese su contraseña'}, validators=[DataRequired()])
    login=SubmitField('Iniciar sesión', render_kw={'class': 'btn btn-secondary btn-block fw-bold'})

# Formulario para buscar 
    buscar=StringField('buscar', render_kw={'class': 'form-control mb-3'})
    btn_buscar=SubmitField('Buscar', render_kw={'class': 'btn btn-primary mb3 mt-4'})

PATH_URL = "/listado"

#Login
@app.route('/')
def home(): 
    form=formUser()
    if 'username' in session:
        cursor = db.database.cursor()
        return render_template('index.html', form=form)
    return render_template('cerrar_sesion.html')

#Listado
@app.route('/listado', methods=['POST', 'GET'])
def listado():
    form=formUser()
    if 'username' in session:
        if session.get('tipo_u') in [1, 3]:
            cursor = db.database.cursor()
            cursor.execute("SELECT a.*, e.estado as estado, f.nom_ficha as nom_ficha, c.competencia as nom_competencia, r.resultado as nom_resultado, i.instructor as nom_instructor, g.nom_gestor as nom_gestor FROM aprendiz a JOIN estado e ON a.estado_sol = e.idestado JOIN ficha f ON a.ficha = f.idficha JOIN competencia c ON a.competencia = c.idcompetencia JOIN resultado r ON a.resultado = r.idresultado JOIN instructor i ON a.instructor = i.idinstructor JOIN gestor g ON a.gestor = g.idgestor;")
            myresult= cursor.fetchall()
            insertObject = []
            columnNames=[column[0] for column in cursor.description]    
            for record in myresult:
                insertObject.append(dict(zip(columnNames, record)))
        
            # Consulta a la tabla 'tipo de documentos' para el select
            cursor.execute("SELECT * FROM tipo_documento")
            tipo_doc_result = cursor.fetchall()
            tipo_doc_columnNames = [column[0] for column in cursor.description]
            tipo_doc = []
            for record in tipo_doc_result:
                tipo_doc.append(dict(zip(tipo_doc_columnNames, record)))

            # Consulta a la tabla 'ficha' para el select
            cursor.execute("SELECT * FROM ficha")
            ficha_result = cursor.fetchall()
            ficha_columnNames = [column[0] for column in cursor.description]
            ficha = []
            for record in ficha_result:
                ficha.append(dict(zip(ficha_columnNames, record)))
            
            # Consulta a la tabla 'competencia' para el select
            cursor.execute("SELECT * FROM competencia")
            competencia_result = cursor.fetchall()
            competencia_columnNames = [column[0] for column in cursor.description]
            competencia = []
            for record in competencia_result:
                competencia.append(dict(zip(competencia_columnNames, record)))

            # Consulta a la tabla 'resultado' para el select
            cursor.execute("SELECT * FROM resultado")
            resultado_result = cursor.fetchall()
            resultado_columnNames = [column[0] for column in cursor.description]
            resultado = []
            for record in resultado_result:
                resultado.append(dict(zip(resultado_columnNames, record)))
            
            # Consulta a la tabla 'instructor' para el select
            cursor.execute("SELECT * FROM instructor")
            instructor_result = cursor.fetchall()
            instructor_columnNames = [column[0] for column in cursor.description]
            instructor = []
            for record in instructor_result:
                instructor.append(dict(zip(instructor_columnNames, record)))
            
            # Consulta a la tabla 'gestor' para el select
            cursor.execute("SELECT * FROM gestor")
            gestor_result = cursor.fetchall()
            gestor_columnNames = [column[0] for column in cursor.description]
            gestor = []
            for record in gestor_result:
                gestor.append(dict(zip(gestor_columnNames, record)))
            cursor.close()
            return render_template(f'{PATH_URL}/list_user.html',form=form, data=insertObject,tipo_doc=tipo_doc, ficha=ficha, competencia=competencia, resultado=resultado, instructor=instructor, gestor=gestor)
        else:    
            flash("No tienes permiso para acceder a esta función.")
            return render_template('sinpermiso.html')
    return render_template('cerrar_sesion.html')

#Buscar
@app.route('/buscar', methods=['POST'])
def buscar():
    search=request.json['busqueda']
    try:
        cursor = db.database.cursor()
        querySQL = "SELECT a.*, e.estado as estado, f.nom_ficha as nom_ficha, c.competencia as nom_competencia, r.resultado as nom_resultado, i.instructor as nom_instructor, g.nom_gestor as nom_gestor FROM aprendiz a JOIN estado e ON a.estado_sol = e.idestado JOIN ficha f ON a.ficha = f.idficha JOIN competencia c ON a.competencia = c.idcompetencia JOIN resultado r ON a.resultado = r.idresultado JOIN instructor i ON a.instructor = i.idinstructor JOIN gestor g ON a.gestor = g.idgestor WHERE p_nombre LIKE %s ORDER BY documento DESC"        
       # search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
        cursor.execute(querySQL, (f"%{search}%",))
        resultado_busqueda = cursor.fetchall()
        if resultado_busqueda:
            insertObject = []
            columnNames=[column[0] for column in cursor.description]
            for record in resultado_busqueda:
                insertObject.append(dict(zip(columnNames, record)))
            cursor.close()
            return render_template(f'{PATH_URL}/buscar_usuarios.html', resultado=insertObject)
        else:   
            return jsonify({'fin': 0})
    except Exception as e:
        print(f"Ocurrió un error en def buscar: {e}")
        return []
    
@app.route('/download/<int:user_id>')
def download_file(user_id):
    cursor = db.database.cursor()
    cursor.execute("SELECT filename, data FROM aprendiz WHERE idusuario  = %s", (user_id,))
    result = cursor.fetchone()
    
    if result:
        filename, data = result
        return send_file(io.BytesIO(data), attachment_filename=filename, as_attachment=True)
    else:
        return "Archivo no encontrado", 404
    
#Ruta Apertura   
@app.route('/register', methods=['GET'])
def formulario():
    if 'username' in session:
        if session.get('tipo_u') == 1:
            form=formUser()
            cursor = db.database.cursor()
            cursor.execute("SELECT * FROM aprendiz")
            myresult= cursor.fetchall()
            insertObject = []
            columnNames=[column[0] for column in cursor.description]
            for record in myresult:
                insertObject.append(dict(zip(columnNames, record)))

            # Consulta a la tabla 'tipo de documentos' para el select
            cursor.execute("SELECT * FROM tipo_documento")
            tipo_doc_result = cursor.fetchall()
            tipo_doc_columnNames = [column[0] for column in cursor.description]
            tipo_doc = []
            for record in tipo_doc_result:
                tipo_doc.append(dict(zip(tipo_doc_columnNames, record)))

            # Consulta a la tabla 'ficha' para el select
            cursor.execute("SELECT * FROM ficha")
            ficha_result = cursor.fetchall()
            ficha_columnNames = [column[0] for column in cursor.description]
            ficha = []
            for record in ficha_result:
                ficha.append(dict(zip(ficha_columnNames, record)))
            
            # Consulta a la tabla 'competencia' para el select
            cursor.execute("SELECT * FROM competencia")
            competencia_result = cursor.fetchall()
            competencia_columnNames = [column[0] for column in cursor.description]
            competencia = []
            for record in competencia_result:
                competencia.append(dict(zip(competencia_columnNames, record)))

            # Consulta a la tabla 'resultado' para el select
            cursor.execute("SELECT * FROM resultado")
            resultado_result = cursor.fetchall()
            resultado_columnNames = [column[0] for column in cursor.description]
            resultado = []
            for record in resultado_result:
                resultado.append(dict(zip(resultado_columnNames, record)))
            
            # Consulta a la tabla 'instructor' para el select
            cursor.execute("SELECT * FROM instructor")
            instructor_result = cursor.fetchall()
            instructor_columnNames = [column[0] for column in cursor.description]
            instructor = []
            for record in instructor_result:
                instructor.append(dict(zip(instructor_columnNames, record)))
            
            # Consulta a la tabla 'gestor' para el select
            cursor.execute("SELECT * FROM gestor")
            gestor_result = cursor.fetchall()
            gestor_columnNames = [column[0] for column in cursor.description]
            gestor = []
            for record in gestor_result:
                gestor.append(dict(zip(gestor_columnNames, record)))

            cursor.close()
            return render_template('register.html', form=form, data=insertObject, tipo_doc=tipo_doc, ficha=ficha, competencia=competencia, resultado=resultado, instructor=instructor, gestor=gestor)
        else:    
            flash("No tienes permiso para acceder a esta función.")
            return render_template('sinpermiso.html')
    return render_template('cerrar_sesion.html')

#Registrar solicitud   
@app.route('/register_on', methods=['POST'])
def addUsuario():
    form=formUser()
    tipo_doc= request.form['tipo_doc']
    ficha=request.form['ficha']
    competencia= request.form['competencia']
    resultado=request.form['resultado']
    instructor=request.form['instructor']
    gestor=request.form['gestor']
    fecha_sol=datetime.now().date()
    estado_sol=1
    archivo=request.files['file']
    if archivo:
        filename = archivo.filename
        filetype = archivo.content_type
        datas = archivo.read()
    if 'username' in session:
        if session.get('tipo_u') == 1:
            if form.is_submitted:
                cursor = db.database.cursor()
                sql="INSERT INTO aprendiz (tipo_doc, documento, p_nombre, s_nombre, p_apellido, s_apellido,correo,telefono,ficha,competencia,resultado, instructor, gestor,fecha_sol, observacion,filename,filetype,data, estado_sol) VALUES (%s, %s, %s, %s,%s, %s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                data=(tipo_doc,form.num_documento.data, form.p_nombre.data, form.s_nombre.data, form.p_apellido.data, form.s_apellido.data,form.correo.data, form.telefono.data, ficha, competencia, resultado, instructor, gestor, fecha_sol, form.observacion.data, filename, filetype, datas, estado_sol)
                cursor.execute(sql, data)
                db.database.commit() 
                flash("ok")
                id_solicitud = cursor.lastrowid
            return redirect(url_for('listado', id_solicitud=id_solicitud , show_Save=True))
        flash("No tienes permiso para acceder a esta función.")
        return redirect(url_for('home'))
    return render_template('cerrar_sesion.html')   

#Ruta informe
@app.route('/informe', methods=['GET'])
def reporte():
    if 'username' in session:
        return render_template('reporte.html')
    return render_template('cerrar_sesion.html')

#Ruta Familias
@app.route('/familia/<string:cod_vivienda>', methods=['GET'])
def familias(cod_vivienda):
    cod_vivienda=cod_vivienda
    form=formUser()
    if 'username' in session:

        cursor = db.database.cursor()
        try:
            cursor.execute("SELECT * FROM aprendiz WHERE idusuario=%s", (cod_vivienda,))
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            aprendiz_data = [dict(zip(columns, record)) for record in result]
        finally:
            cursor.close()

        cursor = db.database.cursor()
        try:
            cursor.execute("SELECT * FROM familia WHERE cod_vivienda=%s", (cod_vivienda,))
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            familia_data = [dict(zip(columns, record)) for record in result]
        finally:
            cursor.close()

        return render_template('register_family.html', form=form, data2=familia_data, data=aprendiz_data)
    return render_template('cerrar_sesion.html')

#Registrar familias    
@app.route('/familia_on', methods=['POST'])
def addfamilia():
    form=formUser()
    tipo_familia= request.form['tipo_familia']
    ciclo_Vital= request.form['ciclo_vital']
    disolucion= request.form['disolucion']
    situacion= request.form['situacion']
    id_= request.form['cod_vivienda']
    if 'username' in session:
        if form.is_submitted:
            cursor = db.database.cursor()
            sql="INSERT INTO familia (cod_vivienda, apellidos_familia, tipo_familia, ciclo_vital, disolucion, situacion) VALUES (%s, %s, %s, %s,%s, %s)"
            data=(id_, form.apellidos_familia.data, tipo_familia, ciclo_Vital, disolucion, situacion)
            cursor.execute(sql, data)
            db.database.commit() 
            flash("ok")        
        return redirect(url_for('familias', cod_vivienda=id_))
    return render_template('cerrar_sesion.html') 

@app.route('/cuenta', methods=['GET'])
def cuenta():
    if 'username' in session:
            username=session.get('username')
            cursor = db.database.cursor()
            cursor.execute("SELECT * FROM login WHERE username=%s", (username,))
            myresult= cursor.fetchall()
            insertObject = []
            columnNames=[column[0] for column in cursor.description]
            for record in myresult:
                insertObject.append(dict(zip(columnNames, record)))
            return render_template('cuenta.html', data=insertObject)
    return render_template('cerrar_sesion.html')

#Editar
@app.route('/edit_cuenta/<string:idlogin>', methods=['POST'])
def edit_cuenta(idlogin):
    usernames= request.form['username']
    nombres= request.form['nombres']
    correo= request.form['correo']
    if 'username' in session:
        flash = idlogin
        cursor = db.database.cursor()
        sql="UPDATE login SET username=%s, fullname=%s, correo=%s WHERE idlogin=%s"
        data=(usernames, nombres, correo, idlogin)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('cuenta', Show_Edit=True))

@app.route('/cambiocontrasena/<string:idlogin>', methods=['POST'])
def cambiocontrasena(idlogin):
    passActual= request.form['passActual']
    passNew= request.form['passNew']
    passComfirm= request.form['passComfirm']
    if 'username' in session:
        if passNew==passComfirm:
            cursor = db.database.cursor()
            sql="UPDATE login SET password=%s  WHERE password=%s and idlogin=%s"
            data=(passNew, passActual, idlogin)
            cursor.execute(sql, data)
            db.database.commit()
            return redirect(url_for('cuenta', Show_Edit=True))
        else: 
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for('cuenta', Show_passFail=True))
        
    return redirect(url_for('cuenta'))

#Generar Informe
@app.route('/informe_on')
def generarInforme():
    if 'username' in session:
            cursor = db.database.cursor()
            cursor.execute("SELECT * FROM aprendiz")
            myresult= cursor.fetchall()
            insertObject = []
            columnNames=[column[0] for column in cursor.description]
            for record in myresult:
                insertObject.append(dict(zip(columnNames, record)))
            cursor.close()
            excel_book=openpyxl.Workbook()
            sheet=excel_book.active
            sheet['A1']="ID"
            sheet['B1']="NOMBRE"
            sheet['C1']="APELLIDO"
            sheet['D1']="CORREO"

            for index, row in enumerate(insertObject):
                sheet[f'A{index+2}'] = row['idusuario']
                sheet[f'B{index+2}'] = row['p_nombre']
                sheet[f'C{index+2}'] = row['documento']
                sheet[f'D{index+2}'] = row['idusuario']
            excel_book.save("informe.xlsx")
            return redirect(url_for('descargar_informe'))
    return render_template('cerrar_sesion.html')  

#Descargar
@app.route('/descargar_informe')
def descargar_informe():
    # Ruta del archivo en el servidor
    ruta_archivo = 'c:/users/usuario/Onedrive/Escritorio/Proyecto HC/informe.xlsx'
   # C:\Users\Usuario\OneDrive\Escritorio\Proyecto HC\Proyecto HC
    return send_file(ruta_archivo, as_attachment=True)
#Borrar
@app.route('/delete/<string:idusuario>')
def delete(idusuario):
    cursor = db.database.cursor()
    sql = "DELETE FROM aprendiz WHERE idusuario=%s"
    data = (idusuario,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('listado', show_Delete=True))

#Editar
@app.route('/edit/<string:idusuario>', methods=['POST'])
def edit(idusuario):
    p_nombre= request.form['p_nombre']
    s_nombre= request.form['s_nombre']
    p_apellido= request.form['p_apellido']
    s_apellido= request.form['s_apellido']
    telefono = request.form['telefono']
    correo = request.form['correo']
    ficha=request.form['ficha']
    competencia=request.form['competencia']
    resultado= request.form['resultado']
    instructor = request.form['instructor']
    gestor = request.form['gestor']
    observacion=request.form['observacion']
    archivo=request.files['file']
    if archivo:
        filename = archivo.filename
        filetype = archivo.content_type
        datas = archivo.read()
    if p_nombre:
        cursor = db.database.cursor()
        sql="UPDATE aprendiz SET p_nombre=%s, s_nombre=%s, p_apellido=%s, s_apellido=%s, correo=%s, telefono=%s,  ficha=%s, competencia=%s, resultado=%s, instructor=%s, gestor=%s,observacion=%s, filename=%s, filetype=%s, data=%s WHERE idusuario =%s"
        data=(p_nombre,s_nombre, p_apellido, s_apellido, correo, telefono, ficha, competencia, resultado, instructor, gestor, observacion,  filename,filetype,datas ,idusuario)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('listado', Show_Edit=True))

@app.route('/login', methods=['GET', 'POST'])
#/login: Esta ruta maneja la página de inicio de sesión. Si se envía un formulario POST.  Si se accede a la página mediante GET, muestra el formulario de inicio de sesión.
def login():
    form=formUser()
    if request.method == 'POST':
        # Validación de entrada: Evita la inyección SQL
        cursor = db.database.cursor()
        cursor.execute("SELECT * FROM login WHERE username=%s AND password=%s", (form.username.data, form.password.data))
        user = cursor.fetchone()
        cursor.close()
  
        if user:
            # Iniciar sesión
            session['user_id'] = user[5]
            session['username'] = user[1]
            session['tipo_u'] = user[4]
            session['nombres'] = user[3]       
            return redirect(url_for('home', show_welcome=True, username=session['nombres']))
        else:
            return render_template('login.html', form=form, show_login=True, invalid_credentials=True)
    return render_template('login.html', form=form, )

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
    flash(error)

@app.route('/citacion', methods=['GET'])
def citacion():
    if 'username' in session:
        return render_template('citacion.html')
    return render_template('cerrar_sesion.html')

@app.route('/citacion_pendiente', methods=['GET'])
def citacion_pendiente():
    form=formUser()
    estado=1
    if 'username' in session:
        if session.get('tipo_u') in [3]:
            cursor = db.database.cursor()
            cursor.execute("SELECT a.*, e.estado as estado, f.nom_ficha as ficha, i.instructor as instructor, g.nom_gestor as gestor, c.competencia as competencia, r.resultado as resultado FROM aprendiz a JOIN estado e ON a.estado_sol = e.idestado JOIN ficha f ON a.ficha = f.idficha JOIN instructor i ON a.instructor = i.idinstructor JOIN gestor g ON a.gestor = g.idgestor JOIN competencia c ON a.competencia = c.idcompetencia JOIN resultado r ON a.resultado = r.idresultado WHERE a.estado_sol = %s;", (estado,))
            myresult= cursor.fetchall()
            insertObject = []
            columnNames=[column[0] for column in cursor.description]    
            for record in myresult:
                insertObject.append(dict(zip(columnNames, record)))
            cursor.close()
            db.database.commit()
            return render_template('/citacion_pendiente.html',form=form, data=insertObject)
        else:    
            flash("No tienes permiso para acceder a esta función.")
            return render_template('sinpermiso.html')
    return render_template('cerrar_sesion.html')

@app.route('/citar/<string:idusuario>', methods=['POST'])
def citar(idusuario):
    fecha_cita= request.form['fecha_cita']
    hora_cita = request.form['hora_cita']
    lugar_cita = request.form['lugar_cita']
    asunto_cita = request.form['asunto']
    archivo_cita=request.files['file']
    estado=2
    if archivo_cita:
        filename = archivo_cita.filename
        filetype = archivo_cita.content_type
        datas= archivo_cita.read()
    if 'username' in session:
        if session.get('tipo_u') in [3]:     
            cursor = db.database.cursor()
            sql="INSERT INTO citacion (idsolicitud, fecha_cita, hora_cita, lugar_cita, asunto_cita,filename,filetype,data) VALUES (%s, %s, %s, %s,%s, %s,%s, %s)"
            data=( idusuario,fecha_cita,hora_cita,lugar_cita,asunto_cita,filename,filetype,datas)
            cursor.execute(sql, data)

            sql2="UPDATE aprendiz SET estado_sol=%s WHERE idusuario=%s"
            data2=(estado,idusuario)
            cursor.execute(sql2, data2)
            
            # Obtener el correo electrónico del usuario
            cursor.execute("SELECT * FROM aprendiz WHERE idusuario = %s", (idusuario,))
            datos = cursor.fetchone()
            p_nombre = datos[3]
            s_nombre = datos[4]
            p_apellido = datos[5]
            s_apellido = datos[6]
            user_email = datos[7]
            image_path= "static/img/SIGAI.png"

             # Enviar notificación interna
            message = f"""<html>
                            <body>
                                <h2>Hola, {p_nombre} {s_nombre} {p_apellido} {s_apellido}</h2>
                                <p>Tienes una citación programada para el <strong>{fecha_cita}</strong> a las <strong>{hora_cita}</strong> en <strong>{lugar_cita}</strong>.<p>
                                <p>Para realización de comité de evaluación por novedades presentada durante tu proceso educativo</p>
                                <p>Por favor, asegúrate de estar presente a tiempo en el lugar citado.</p>
                                <p>Saludos,</p>
                                <p><em>Comité de evaluación</em></p>
                                <p><img src="cid:image1" alt="Imagen"></p>
                            </body>
                        </html>     
                        """

            # Enviar correo electrónico
            send_email(user_email, "Tienes una citación del comité de evaluación", message, image_path)

            db.database.commit() 

            flash("Cita programada exitosamente.")

        else:    
            flash("No tienes permiso para acceder a esta función.")
            return render_template('sinpermiso.html')      
    return redirect(url_for('cronograma', show_cita=True))

@app.route('/cronograma', methods=['GET'])
def cronograma():
    form=formUser()
    if 'username' in session:
        if session.get('tipo_u') in [3]:
            cursor = db.database.cursor()
            cursor.execute("SELECT a.*, e.p_nombre AS p_nombre, e.s_nombre AS s_nombre, e.p_apellido AS p_apellido, e.s_apellido AS s_apellido FROM citacion a JOIN aprendiz e ON a.idsolicitud = e.idusuario;")
            myresult= cursor.fetchall()
            insertObject = []
            columnNames=[column[0] for column in cursor.description]    
            for record in myresult:
                insertObject.append(dict(zip(columnNames, record)))

            events = []
            for row in myresult:
                event_date = row[2].strftime('%Y-%m-%d')
                event_time= row[3]  
                events.append({
                'title': event_time,  # Título del evento
                'start': event_date,  # Fecha y hora de inicio
        })
            cursor.close()
            return render_template('/cronograma.html',form=form, data=insertObject, events=events)

        else:    
            flash("No tienes permiso para acceder a esta función.")
            return render_template('sinpermiso.html')
    return render_template('cerrar_sesion.html')

@app.route('/download_cita/<int:user_id>')
def download_cita(user_id):
    cursor = db.database.cursor()
    cursor.execute("SELECT filename, data FROM citacion WHERE idcitacion = %s", (user_id,))
    result = cursor.fetchone()
    if result:
        filename, data = result
        return send_file(io.BytesIO(data), attachment_filename=filename, as_attachment=True)
    else:
        return "Archivo no encontrado", 404

@app.route('/editar_cita/<string:idcitacion>', methods=['POST'])
def editar_cita(idcitacion):
    fecha_cita= request.form['fecha_cita']
    hora_cita = request.form['hora_cita']
    lugar_cita = request.form['lugar_cita']
    asunto_cita = request.form['asunto']
    archivo_cita=request.files['file']
    if archivo_cita:
        filename = archivo_cita.filename
        filetype = archivo_cita.content_type
        datas = archivo_cita.read()
    if 'username' in session:
        cursor = db.database.cursor()
        sql="UPDATE citacion SET fecha_cita=%s, hora_cita=%s, lugar_cita=%s, asunto_cita=%s, filename=%s, filetype=%s,  data=%s WHERE idcitacion =%s"
        data=(fecha_cita,hora_cita, lugar_cita, asunto_cita, filename,filetype,datas ,idcitacion)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('cronograma'))


@app.route('/descargo', methods=['GET'])
def descargo():
    if 'username' in session:
        form=formUser()
        cursor = db.database.cursor()
        cursor.execute("SELECT * FROM aprendiz")
        myresult= cursor.fetchall()
        insertObject = []
        columnNames=[column[0] for column in cursor.description]
        for record in myresult:
            insertObject.append(dict(zip(columnNames, record)))

        return render_template('descargo.html',form=form, data=insertObject)
    return render_template('cerrar_sesion.html')
################################################################
#NOTIFICACIÓN

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'sigaiaplication@gmail.com'
app.config['MAIL_PASSWORD'] = 'gshqadtjktozwbny'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
        
def send_email(to, subject, body, image_path=None):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = body
    msg.html = body

    if image_path and os.path.isfile(image_path):
        with app.open_resource(image_path) as img:
            # Adjuntar la imagen con un Content-ID
            msg.attach(
                os.path.basename(image_path),  # Nombre del archivo
                'image/png',                  # Tipo de contenido
                img.read(),                   # Contenido del archivo
                headers={"Content-ID": "<image1>"}  # Content-ID para referenciar en HTML
            )
    else:
        print(f"El archivo {image_path} no se encuentra.")
    mail.send(msg)



if __name__ == '__main__':
    app.run(debug=True)

