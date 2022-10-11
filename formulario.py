from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,SelectField,SubmitField,PasswordField


class formulario_estudiantes(FlaskForm):
    documento =IntegerField("documento")
    nombre = StringField("nombre")
    genero = StringField("genero")
    ciclo = SelectField("ciclo",choices=[("py","python"),("java","java"),("web","web")])
    guardar = SubmitField("guardar",render_kw=({"onclick":"cambiarRutaE('/guardarestudiante')"}))
    consultar = SubmitField("consultar",render_kw=({"onclick":"cambiarRutaE('/consultarestudiante')"}))
    eliminar = SubmitField("eliminar",render_kw=({"onclick":"cambiarRutaE('/eliminarestudiante')"}))
    actualizar = SubmitField ("actualizar",render_kw=({"onclick":"cambiarRutaE('/actualizarestudiante')"}))

class formulario_login (FlaskForm):
    user =StringField("user") 
    password =PasswordField ("password")
    enviar = SubmitField("entrar",render_kw=({"onclick":"cambiarRuta('/loginC')"}))
    guardar = SubmitField("guardar", render_kw=({"onclick":"cambiarRuta('/validaciones')"}))
