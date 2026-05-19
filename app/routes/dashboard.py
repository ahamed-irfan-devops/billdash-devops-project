from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from app.models import Product, Bill
from app import db
from datetime import date

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    return redirect(url_for("dashboard.dashboard"))

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    total_products = Product.query.count()
    stock_value = db.session.query(
        db.func.sum(Product.price * Product.stock)
    ).scalar() or 0
    bills_today = Bill.query.filter(
        db.func.date(Bill.created_at) == date.today()
    ).count()
    recent_bills = Bill.query.order_by(Bill.created_at.desc()).limit(5).all()
    return render_template(
        "dashboard.html",
        total_products=total_products,
        stock_value=stock_value,
        bills_today=bills_today,
        recent_bills=recent_bills,
    )
