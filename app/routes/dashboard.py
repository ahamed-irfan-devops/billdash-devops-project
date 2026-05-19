from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Product, Bill, BillItem
from app import db
from datetime import date, timedelta

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    return redirect(url_for("dashboard.dashboard"))

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    total_products = Product.query.count()
    low_stock = Product.query.filter(Product.stock <= 5).count()
    out_of_stock = Product.query.filter(Product.stock == 0).count()
    stock_value = db.session.query(
        db.func.sum(Product.price * Product.stock)
    ).scalar() or 0
    bills_today = Bill.query.filter(
        db.func.date(Bill.created_at) == date.today()
    ).count()
    revenue_today = db.session.query(
        db.func.sum(Bill.total_amount)
    ).filter(db.func.date(Bill.created_at) == date.today()).scalar() or 0
    total_revenue = db.session.query(db.func.sum(Bill.total_amount)).scalar() or 0
    total_bills = Bill.query.count()
    recent_bills = Bill.query.order_by(Bill.created_at.desc()).limit(8).all()
    low_stock_products = Product.query.filter(Product.stock <= 5).order_by(Product.stock.asc()).limit(5).all()
    return render_template(
        "dashboard.html",
        total_products=total_products,
        low_stock=low_stock,
        out_of_stock=out_of_stock,
        stock_value=stock_value,
        bills_today=bills_today,
        revenue_today=revenue_today,
        total_revenue=total_revenue,
        total_bills=total_bills,
        recent_bills=recent_bills,
        low_stock_products=low_stock_products,
    )
