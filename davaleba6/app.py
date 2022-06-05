import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    add_date = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    

@app.route("/")
def home():
    all_items = Inventory.query.all()
    return render_template("index.html", items=all_items)


@app.route("/inventory/<int:id>")
def get_item(id):
    item = Inventory.query.get(id)

    return render_template("tatoo.html", item=item)


@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        amount = request.form["amount"]

        item = Inventory(name=name, price=price, amount=amount)

        db.session.add(item)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("create.html")


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    item = Inventory.query.get(id)

    if request.method == "POST":
        item.name = request.form["name"]
        item.price = request.form["price"]
        item.amount = request.form["amount"]

        db.session.add(item)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("update.html", item=item)

# Delete Item
@app.route("/delete/<int:id>", methods=["post"])
def delete(id):
    item = Inventory.query.get(id)
    db.session.delete(item)
    db.session.commit()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
