from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.models import Product
from app import db

stock_bp = Blueprint("stock", __name__)

@stock_bp.route("/stock")
@login_required
def stock():
    products = Product.query.order_by(Product.name).all()
    return render_template("stock.html", products=products)

@stock_bp.route("/stock/update", methods=["POST"])
@login_required
def update_stock():
    product = Product.query.get_or_404(request.form["product_id"])
    product.stock = int(request.form["stock"])
    db.session.commit()
    flash(f"Stock updated for {product.name}.", "success")
    return redirect(url_for("stock.stock"))
