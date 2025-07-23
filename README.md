# stockflow-case-study  
**Backend Intern Case Study – Bynry Inc**

This repository contains my submission for the Backend Engineering Intern Case Study at Bynry Inc. It is divided into three parts:

---

## Table of Contents

1. [Case Study Write‑Up](#case-study-write-up)  
2. [Part 1: Code Review & Bug Fix](#part-1-code-review--bug-fix)  
3. [Part 2: Database Schema Design](#part-2-database-schema-design)  
4. [Part 3: Low‑Stock Alerts API](#part-3-low-stock-alerts-api)  
5. [How to Run](#how-to-run)  

---

## Case Study Write‑Up

Please refer to `CaseStudyResponse.md` for detailed explanations related to:
- Code issues and fixes (Part 1)
- Database schema structure and assumptions (Part 2)
- API logic and behavior (Part 3)

---

## Part 1: Code Review & Bug Fix

- Reviewed and fixed the logic in `stock_service.js` to avoid negative stock updates.
- Added validation for non-existent items and invalid quantities.

Test using:
```bash
cd code_review
node test.js
```

---

## Part 2: Database Schema Design

- Designed the schema with `products`, `warehouses`, and `inventory` tables.
- Used basic constraints and keys to ensure data consistency.
- SQL file provided in `schema/schema.sql`.

---

## Part 3: Low‑Stock Alerts API

- Built using Express.js
- Endpoint: `GET /api/companies/:company_id/alerts/low-stock`
- Returns products where quantity is less than or equal to reorder level.
- Sample response:
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

---

## How to Run

### Part 1
```bash
cd code_review
node test.js
```

### Part 3 API
```bash
cd api
npm install
node app.js
```

Open browser or use curl:
```
http://localhost:3000/api/companies/1/alerts/low-stock
```

---

## Submission

GitHub Repo: [https://github.com/AtulWanve/stockflow-case-study](https://github.com/AtulWanve/stockflow-case-study)
