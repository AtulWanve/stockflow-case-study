-- Inventory Management Schema

CREATE TABLE Products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  reorder_level INT NOT NULL
);

CREATE TABLE Warehouses (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  location TEXT
);

CREATE TABLE Inventory (
  id SERIAL PRIMARY KEY,
  product_id INT REFERENCES Products(id),
  warehouse_id INT REFERENCES Warehouses(id),
  quantity INT NOT NULL
);
