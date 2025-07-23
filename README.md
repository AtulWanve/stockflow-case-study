# 📦 Low Stock Alert System

## Overview
This project manages inventory across multiple warehouses and provides low-stock alerts for products based on recent sales and product-specific thresholds.

## Features
- Products can exist in multiple warehouses
- Low stock thresholds vary by product type
- Alerts only for recently sold products (last 30 days)
- Supplier info included in alerts
- Supports bundles and inventory history

## API
**GET /api/companies/{company_id}/alerts/low-stock**  
Returns low-stock alerts with estimated days until stockout.

## Assumptions
- Thresholds stored by product type
- Recent sales = last 30 days
- First supplier is used in alerts
- Products have a `type` field
