1. Design Schema:

-- 1. Companies
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- 2. Warehouses (belongs to a company)
CREATE TABLE warehouses (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255),
    location TEXT
);

-- 3. Products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    is_bundle BOOLEAN DEFAULT FALSE
);

-- 4. Inventory (product per warehouse with quantity)
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0,
    UNIQUE(product_id, warehouse_id)
);

-- 5. Inventory History (track changes over time)
CREATE TABLE inventory_history (
    id SERIAL PRIMARY KEY,
    inventory_id INTEGER NOT NULL REFERENCES inventory(id) ON DELETE CASCADE,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    change_type VARCHAR(50),  -- e.g., "add", "remove", "transfer"
    quantity_before INTEGER,
    quantity_after INTEGER,
    note TEXT
);

-- 6. Suppliers
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_info TEXT
);

-- 7. Supplier Products (many-to-many: suppliers <-> products)
CREATE TABLE supplier_products (
    id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    price NUMERIC(10, 2),
    lead_time_days INTEGER
);

-- 8. Bundles (self-referencing many-to-many for bundles)
CREATE TABLE product_bundles (
    id SERIAL PRIMARY KEY,
    bundle_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    component_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1,
    UNIQUE(bundle_id, component_id),
    CHECK (bundle_id <> component_id)
);

2. Identify Gaps:

1: How should inventory changes be categorized?
2: Should each warehouse have reorder rules (min/max levels)?
3: Do suppliers belong to a company, or are they shared globally?
4: Should we track batch/lot numbers or expiry dates?


3. Explain Design Decisions

 Relationships
- One-to-many:
  • companies → warehouses
  • suppliers → products

- Many-to-many:
  • products ↔ suppliers (via `supplier_products`)
  • products ↔ products (bundles via `product_bundles`)

Data Integrity
-----------------
- Foreign keys ensure proper relational links
- Constraints:
  • UNIQUE(sku) for global SKU uniqueness
  • UNIQUE(product_id, warehouse_id) in inventory
  • CHECK (bundle_id <> component_id) avoids recursive self-bundling

Indexes
----------
- UNIQUE constraints double as indexes
- inventory_history.changed_at for querying recent changes
- Optionally, add GIN indexes on location/description for full-text search

Flexibility
--------------
- is_bundle flag avoids ambiguity when querying composite products
- inventory_history provides full audit trail of stock changes
