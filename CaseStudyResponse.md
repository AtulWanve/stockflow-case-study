
# CaseStudyResponse.md

## Part 1: Code Review & Bug Fix

### Issues Found
- No check for non-existent products.
- Inventory could go negative if quantity exceeded stock.
- No validation for invalid quantity values.

### Fix Summary
- Added a check to ensure the product exists.
- Validated input quantity to be a positive number.
- Prevented negative stock updates.

### Why It Matters
These fixes avoid data inconsistency and help maintain realistic inventory values.

---

## Part 2: Database Schema Design

### Tables Created
- `products`: Contains product ID, name, and reorder level.
- `warehouses`: Contains warehouse ID and location.
- `inventory`: Tracks quantity of each product in each warehouse.

### Design Highlights
- Used composite keys for product-warehouse uniqueness.
- Applied foreign key constraints for integrity.
- Normalized to avoid data duplication.

### Assumptions
- A product can be stored in multiple warehouses.
- Each warehouse has independent stock tracking.

---

## Part 3: Low-Stock Alerts API

### Endpoint
```
GET /api/companies/:company_id/alerts/low-stock
```

### Response Example
```json
{
  "alerts": [
    {
      "product": "item-1",
      "quantity": 3,
      "reorder_level": 5
    }
  ],
  "total_alerts": 1
}
```

### Logic Used
- Returned items where quantity is less than or equal to reorder level.
- Used simple filter function to simulate real-time alerting.

### Edge Cases Considered
- Empty inventory list
- No low-stock items
- Products exactly at reorder level

---

Thanks for reviewing my case study!
