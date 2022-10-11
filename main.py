import sqlite3
from flask import *
from formulario import formulario_estudiantes,formulario_login
from markupsafe import escape
import hashlib
from werkzeug.security import generate_password_hash,check_password_hash
from sqlite3 import Error
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)
@app.route("/")
def index():
    return render_template ("index.html")
    

@app.route("/login", methods = ["GET","POST"]) 
def login ():
    form = formulario_login()
    return render_template("login.html",form=form)

# @app.route("/loginC",methods = ["GET","POST"])
# def loginC ():
#     form = formulario_estudiantes()
#     if request.method=="POST":
#         user = request.form["user"]
#         password = request.form["password"]
        

#         with sqlite3.connect("Colegio.db") as con: #conexion con la base de datos
#             cur = con.cursor()
#             cur.execute("select * from Usuario where user= '"+user+"' and password= '"+password+"' ")
#             if cur.fetchone():
#                 return render_template("formulario.html",formulario=form)
#     return "usuario no permitido"

@app.route("/loginC",methods = ["GET","POST"])
def loginC ():
    
    if request.method=="POST":
        usuario =escape(request.form["user"])
        password = escape(request.form["password"])
        
    try: 
        with sqlite3.connect("Colegio.db") as con: #conexion con la base de datos
            cur = con.cursor()
            a = cur.execute("select password from Usuario where user=?" ,[usuario] ).fetchone()
            if a != None :
                an= a[0]
                #print(an)
                if check_password_hash(an,password): #el check_password_hash compara la consulta realizada con la contraseña
                    session["usuario"]= usuario 
                    return render_template("index.html")
            else :
                return "usuario y clave invalida"
    except:
        print("ocurrio un error")
    
    return "usuario no permitido"

@app.route("/hashlogin", methods = ["GET","POST"]) 
def hashlogin ():
    form = formulario_login()
    return render_template("login.html",form=form)

@app.route("/validaciones", methods = ["GET","POST"]) 
def hashlogin2 ():
    form = formulario_login()
    if request.method=="POST":
        usuario=escape(request.form["user"])
        password=escape(request.form["password"])
        #m = hashlib.md5(password.encode())
        #m = hashlib.sha512(password.encode())
        ma = generate_password_hash(password)

        try: 
            with sqlite3.connect("Colegio.db") as con: #conexion con la base de datos
                cur = con.cursor()
                a = cur.execute("insert into Usuario (user,password) values (?,?)" ,[usuario,ma])
                con.commit()
                return "usuario guardado"
        except:
            print("ocurrio un error")
    return "no se pudo guardar"

@app.route("/logout")
def logout ():
        session.clear()
        return render_template("index.html")
      

@app.before_request
def before_request():
    usuario = session.get("usuario")
    print(usuario)
    if usuario  is None :
        g.user=None
    else: 
        try: 
            with sqlite3.connect("Colegio.db") as con: #conexion con la base de datos
                cur = con.cursor()
                g.user = cur.execute("select user from Usuario where user=?" ,[usuario] ).fetchone()
                print(g.user)
        except:
            print("ocurrio un error")

@app.route("/guardarestudiante",methods = ["GET","POST"])
def guardarestudiante ():
    if g.user :
        form = formulario_estudiantes()
        if request.method =="POST":
            documento = request.form["documento"]
            nombre = request.form["nombre"]
            genero = request.form["genero"]
            ciclo = request.form["ciclo"]
            print(documento,nombre,genero,ciclo)
            try:
                with sqlite3.connect("Colegio.db") as com:
                    cum = com.cursor()
                    print("aqui1")
                    cum.execute("insert into Estudiante (documento,nombre,genero,ciclo) values (?,?,?,?)",[documento,nombre,genero,ciclo])
                    com.commit()
                    print("aqui2")
                    flash("Estudiante Guardado")
                    return render_template("formulario.html",formulario=form)
            except Error:
                print(Error)
            return "estudiante no se puedo guardar"
    else:
        flash("no esta logeado")
        return ("Accion no permitida")

@app.route("/consultarestudiante",methods = ["GET","POST"])
def consultarestudiante ():
    form = formulario_estudiantes()
    documento= request.form["documento"]
    try:
        with sqlite3.connect("Colegio.db") as com:
            com.row_factory=sqlite3.Row
            cum=com.cursor()
            cum.execute (" select  * from Estudiante where documento=? ", [documento])
            row = cum.fetchone()
            if row :
                form.nombre.data= row["nombre"]
                form.genero.data= row["genero"]
                form.ciclo.data= row["ciclo"]
            else:
                form.nombre.data=""
                form.genero.data=""
                form.ciclo.data=""
                flash("estudiante no encontrado")
    except Error:
        print(Error)
    return render_template("formulario.html",formulario=form)


@app.route("/eliminarestudiante",methods = ["GET","POST"])
def elimiarestudiante ():
    form = formulario_estudiantes()
    documento = request.form["documento"]
    try:
        with sqlite3.connect("Colegio.db") as com:
            cum =com.cursor()
            cum.execute( "delete from Estudiante where documento=?",[documento])
            com.commit()
            flash("Estudiante eliminado")
    except Error:
        print(Error)
    return render_template("formulario.html",formulario=form)

@app.route("/actualizarestudiante",methods = ["GET","POST"])
def actualizarestudiante():
    form = formulario_estudiantes()
    documento = request.form["documento"]
    nombre = request.form["nombre"]
    genero = request.form["genero"]
    ciclo = request.form["ciclo"]
    try :
        with sqlite3.connect("Colegio.db") as com:
            cum = com.cursor()
            print("Aqui1")
            cum.execute("update Estudiante set nombre=?,genero=?,ciclo=? where documento =?",[nombre,genero,ciclo,documento])
            com.commit()
            print("Aqui2")
            if com.total_changes>0:
                flash("Estudiante actualizado")
            else:
                flash("nose pudo actualizar el estudiante")
    except Error:
        print(Error)
    return render_template("formulario.html",formulario=form)

app.run(debug=True)