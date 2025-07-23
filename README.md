# stockflow-case-study
Backend Intern Case Study – Bynry Inc
# Bynry Backend Case Study – StockFlow

This repository contains my submission for the Backend Engineering Intern Case Study at Bynry Inc. It is divided into three parts:

---

## 1. Code Review and Bug Fix (`code_review/`)

- File: `stock_service.js`
- Summary: Fixed a critical issue where stock could go negative due to missing validation.
- Added proper checks for:
  - Non-existing items
  - Invalid quantity values
  - Negative inventory deduction

Run test:
```bash
cd code_review
node test.js
