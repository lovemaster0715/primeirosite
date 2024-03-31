from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario


class FormLogin(FlaskForm):
    email = StringField("E-mail",validators = [DataRequired(),Email()])
    password = PasswordField("Senha", validators= [DataRequired()])
    login = SubmitField("Login")
    
    def validate_email(self,email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError("Usuário inexistente.")




class FormCriarConta(FlaskForm):
    email = StringField("E-mail",validators = [DataRequired(),Email()])
    username= StringField("Nome de usuário",validators = [DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
    confirm_password = PasswordField("Confirme a senha", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Criar conta")

    def validate_email(self,email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado.")


class FormFoto(FlaskForm):
    image = FileField("Foto", validators= [DataRequired()])
    submit = SubmitField("Enviar")