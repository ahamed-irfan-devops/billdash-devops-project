from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.models import Product, Bill, BillItem
from app import db

billing_bp = Blueprint("billing", __name__)

@billing_bp.route("/billing")
@login_required
def billing():
    products = Product.query.filter(Product.stock > 0).order_by(Product.name).all()
    return render_template("billing.html", products=products)

@billing_bp.route("/billing/create", methods=["POST"])
@login_required
def create_bill():
    product_ids = request.form.getlist("product_id")
    quantities = request.form.getlist("quantity")

    if not product_ids:
        flash("No products selected.", "warning")
        return redirect(url_for("billing.billing"))

    total = 0
    items = []
    for pid, qty in zip(product_ids, quantities):
        qty = int(qty)
        if qty <= 0:
            continue
        product = Product.query.get_or_404(pid)
        if product.stock < qty:
            flash(f"Insufficient stock for {product.name}.", "danger")
            return redirect(url_for("billing.billing"))
        subtotal = float(product.price) * qty
        total += subtotal
        items.append((product, qty))

    bill = Bill(total_amount=total)
    db.session.add(bill)
    db.session.flush()

    for product, qty in items:
        db.session.add(BillItem(
            bill_id=bill.id,
            product_id=product.id,
            quantity=qty,
            unit_price=product.price,
        ))
        product.stock -= qty

    db.session.commit()
    flash("Bill created successfully.", "success")
    return redirect(url_for("billing.view_bill", id=bill.id))

@billing_bp.route("/billing/<int:id>")
@login_required
def view_bill(id):
    bill = Bill.query.get_or_404(id)
    return render_template("bill_view.html", bill=bill)
