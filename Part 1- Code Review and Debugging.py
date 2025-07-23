@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    # Create new product
    product = Product(
        name=data['name'],
        sku=data['sku'],
        price=data['price'],
        warehouse_id=data['warehouse_id']
    )

    db.session.add(product)
    db.session.commit()

    # Update inventory count
    inventory = Inventory(
        product_id=product.id,
        warehouse_id=data['warehouse_id'],
        quantity=data['initial_quantity']
    )

    db.session.add(inventory)
    db.session.commit()
    
    return {"message": "Product created", "product_id": product.id}

Part 1: Code Review & Debugging

Issues & Impacts:

1: here in given code there is no input validation--------------------> Missing fields like name, sku, etc., can raise KeyError

2: there is no error handling in given code --------------------------> Any error during DB operations will crash the app and expose stack traces 

3: there are 2 db.commit statements which may lead to data inconsistency if there is Exception after saving product-------------> inconsitent data

4: No data type validation    ----------------------------> price or initial_quantity can be  string, causing runtime issues

5:  No check if warehouse_id exists --------------------> sql forein key error 

from flask import request, jsonify
from models import Product, Inventory, Warehouse, db
from sqlalchemy.exc import IntegrityError

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    # 1. Validate required fields
    required_fields = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # 2. Type & value checks
    try:
        price = float(data['price'])
        quantity = int(data['initial_quantity'])
        if price < 0 or quantity < 0:
            return jsonify({"error": "Price and quantity must be non-negative"}), 400
    except ValueError:
        return jsonify({"error": "Price must be a number and quantity must be an integer"}), 400

    # 3. Optional: Check if SKU already exists
    existing = Product.query.filter_by(sku=data['sku']).first()
    if existing:
        return jsonify({"error": "SKU already exists"}), 409

    # 4. Optional: Check if warehouse exists
    warehouse = Warehouse.query.get(data['warehouse_id'])
    if not warehouse:
        return jsonify({"error": "Invalid warehouse_id"}), 404

    try:
        # 5. Create product
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=price,
            warehouse_id=data['warehouse_id']
        )
        db.session.add(product)
        db.session.flush()  # To get product.id

        # 6. Create inventory
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=data['warehouse_id'],
            quantity=quantity
        )
        db.session.add(inventory)

        # 7. Commit both
        db.session.commit()

        return jsonify({
            "message": "Product created",
            "product_id": product.id
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e.orig)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
