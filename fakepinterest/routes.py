from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Post
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from werkzeug.utils import secure_filename
import os

@app.route("/", methods =["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email = formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password,formlogin.password.data):
            login_user(usuario)
            return redirect(url_for("perfil",id_usuario = usuario.id))
    return render_template("homepage.html", form=formlogin)



@app.route("/criarconta", methods =["GET", "POST"])
def criarconta():
    formcriarconta= FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.password.data)
        usuario = Usuario(username=formcriarconta.username.data, 
                          password=senha, 
                          email=formcriarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember = True)
        return redirect(url_for("perfil", id_usuario = usuario.id))
    return render_template("criarconta.html",form= formcriarconta)



@app.route("/login/<id_usuario>/", methods = ["GET", "POST"])
@login_required
def perfil(id_usuario):
    if (int(id_usuario)) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.image.data
            nome_seguro = secure_filename(arquivo.filename)
            path = os.path.join(os.path.abspath(os.path.dirname(__file__))
                           , app.config['UPLOAD_FOLDER'],
                           nome_seguro)
            arquivo.save(path)
            imagem = Post(image = nome_seguro, id_usuario=current_user.id)
            database.session.add(imagem)
            database.session.commit()
        return render_template("perfil.html",usuario = current_user,form = form_foto)        
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html",usuario = usuario, form = None)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed(): 
    fotos = Post.query.order_by(Post.date.desc()).all()
    return render_template("feed.html", fotos = fotos)

