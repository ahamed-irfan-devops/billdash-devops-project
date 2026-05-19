from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.models import Product
from app import db

products_bp = Blueprint("products", __name__)

@products_bp.route("/products")
@login_required
def list_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("products.html", products=products)

@products_bp.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():
    if request.method == "POST":
        name = request.form["name"].strip()
        if Product.query.filter_by(name=name).first():
            flash("Product already exists.", "warning")
        else:
            product = Product(
                name=name,
                category=request.form["category"].strip(),
                price=request.form["price"],
                stock=request.form["stock"],
            )
            db.session.add(product)
            db.session.commit()
            flash("Product added successfully.", "success")
            return redirect(url_for("products.list_products"))
    return render_template("products.html", form=True)
