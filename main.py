from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Boolean, URL
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, InputRequired
import requests
import os

# defining database file path
db_path = os.path.abspath("cafes.db")
class Base(DeclarativeBase):
    pass

app= Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# defination of database model
class Cafe(db.Model):
    __tablename__ = "cafe"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=True)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

# form for adding a new cafe
class AddCafeForm(FlaskForm):
    name = StringField("Cafe name", validators=[DataRequired()])
    map_url = StringField("Google Maps URL", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])

    has_sockets = RadioField("Has sockets?", choices=[("1", "Yes"), ("0", "No")], validators=[DataRequired()])
    has_toilet = RadioField("Has toilet?", choices=[("1", "Yes"), ("0", "No")], validators=[DataRequired()])
    has_wifi = RadioField("Has wifi?", choices=[("1", "Yes"), ("0", "No")], validators=[DataRequired()])
    can_take_calls = RadioField("Can take calls?", choices=[("1", "Yes"), ("0", "No")], validators=[DataRequired()])

    seats = StringField("Number of seats (e.g., 10-20)", validators=[DataRequired()])
    coffee_price = StringField("Coffee price (e.g., $2.50)", validators=[DataRequired()])

    submit = SubmitField("Add Cafe")

# form editing a cafe
class EditForm(FlaskForm):
    wifi = RadioField("Has wifi?", choices=[("1", "Yes"), ("0", "No")], validators=[DataRequired()])
    sockets = RadioField("Has sockets?", choices=[("1", "Yes"), ("0", "No")], validators=[DataRequired()])
    toilet = RadioField("Has toilets?", choices=[("1", "Yes"), ("0", "No")], validators=[DataRequired()])
    coffe_price = StringField("New coffee price", validators=[DataRequired()])
    seats = StringField("Number of seats", validators=[DataRequired()])
    submit = SubmitField("Okay!")

@app.route("/")
def home():
    cafes= db.session.execute(db.select(Cafe)).scalars()
    return render_template("index.html", cafes= cafes)

# Adding the Update functionality
@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditForm()
    cafe_id = request.args.get("id")
    cafe = db.get_or_404(Cafe, cafe_id)
    if form.validate_on_submit():
        cafe.has_wifi = form.wifi.data == "1"
        cafe.has_sockets = form.sockets.data == "1"
        cafe.has_toilet= form.toilet.data == "1"
        cafe.coffee_price= form.coffe_price.data
        cafe.seats= form.seats.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", cafe=cafe , form=form)

@app.route("/add", methods = ["GET", "POST"])
def add():
    form= AddCafeForm()
    if form.validate_on_submit():
        new_cafe= Cafe(
            name = form.name.data,
            map_url = form.map_url.data,
            img_url = form.img_url.data,
            location = form.location.data,
            has_sockets = form.has_sockets.data == "1",
            has_toilet = form.has_toilet.data == "1",
            has_wifi = form.has_wifi.data == "1",
            can_take_calls = form.can_take_calls.data == "1",
            seats = form.seats.data,
            coffee_price = form.coffee_price.data)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("add.html", form= form)

@app.route("/delete")
def delete():
    cafe_id = request.args.get("id")
    movie = db.get_or_404(Cafe, cafe_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)