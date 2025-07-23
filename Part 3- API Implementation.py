
"""
Assumptions:
------------
1. Product has a "type" field to determine its low-stock threshold.
2. Thresholds are stored in a separate table: product_thresholds(product_type, threshold).
3. Recent sales are defined as having sales in the last 30 days.
4. Sales are tracked in a sales table with product_id, warehouse_id, sold_at, quantity.
5. A product may have multiple suppliers, but we pick the first one for the alert.
6. All necessary SQLAlchemy models are available: Company, Warehouse, Product, Inventory,
   Supplier, SupplierProduct, Sale, ProductThreshold.
"""

from flask import Flask, jsonify
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from models import db, Company, Warehouse, Product, Inventory, Sale, Supplier, SupplierProduct, ProductThreshold

app = Flask(__name__)

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):
    try:
        # Step 1: Get all warehouses for this company
        warehouses = Warehouse.query.filter_by(company_id=company_id).all()
        if not warehouses:
            return jsonify({"alerts": [], "total_alerts": 0}), 200

        warehouse_ids = [w.id for w in warehouses]

        # Step 2: Get recent sales activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_sales = db.session.query(Sale.product_id).filter(
            Sale.warehouse_id.in_(warehouse_ids),
            Sale.sold_at >= thirty_days_ago
        ).distinct().all()
        recent_product_ids = [s.product_id for s in recent_sales]

        if not recent_product_ids:
            return jsonify({"alerts": [], "total_alerts": 0}), 200

        # Step 3: Join inventory and product threshold data
        alerts = []
        inventory_data = db.session.query(
            Inventory.product_id,
            Inventory.warehouse_id,
            Inventory.quantity,
            Product.name.label("product_name"),
            Product.sku,
            Product.type.label("product_type"),
            Warehouse.name.label("warehouse_name"),
            ProductThreshold.threshold
        ).join(Product, Product.id == Inventory.product_id)         .join(Warehouse, Warehouse.id == Inventory.warehouse_id)         .join(ProductThreshold, Product.type == ProductThreshold.product_type)         .filter(
            Inventory.product_id.in_(recent_product_ids),
            Inventory.warehouse_id.in_(warehouse_ids),
            Inventory.quantity < ProductThreshold.threshold
        ).all()

        for item in inventory_data:
            # Calculate simple stockout estimation (assume daily sales = avg of last 30 days)
            total_sales = db.session.query(func.sum(Sale.quantity)).filter(
                Sale.product_id == item.product_id,
                Sale.warehouse_id == item.warehouse_id,
                Sale.sold_at >= thirty_days_ago
            ).scalar() or 0

            daily_avg_sales = total_sales / 30 if total_sales > 0 else 0
            days_until_stockout = int(item.quantity / daily_avg_sales) if daily_avg_sales > 0 else None

            # Get supplier info
            supplier_data = db.session.query(Supplier).join(SupplierProduct)                .filter(SupplierProduct.product_id == item.product_id).first()

            supplier_info = {
                "id": supplier_data.id,
                "name": supplier_data.name,
                "contact_email": supplier_data.contact_info
            } if supplier_data else None

            alerts.append({
                "product_id": item.product_id,
                "product_name": item.product_name,
                "sku": item.sku,
                "warehouse_id": item.warehouse_id,
                "warehouse_name": item.warehouse_name,
                "current_stock": item.quantity,
                "threshold": item.threshold,
                "days_until_stockout": days_until_stockout,
                "supplier": supplier_info
            })

        return jsonify({
            "alerts": alerts,
            "total_alerts": len(alerts)
        }), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
