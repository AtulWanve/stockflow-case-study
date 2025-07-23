# stockflow-case-study  
**Backend Intern Case Study – Bynry Inc**

This repository contains my submission for the Backend Engineering Intern Case Study at Bynry Inc. It is organized into three parts and a detailed write‑up.

---

## 📖 Table of Contents

1. [Case Study Write‑Up](#case-study-write-up)  
2. [Part 1: Code Review & Bug Fix](#part-1-code-review--bug-fix)  
3. [Part 2: Database Schema Design](#part-2-database-schema-design)  
4. [Part 3: Low‑Stock Alerts API](#part-3-low-stock-alerts-api)  
5. [Folder Structure](#folder-structure)  
6. [How to Run & Test](#how-to-run--test)  

---

## Case Study Write‑Up

See **`CaseStudyResponse.md`** for:
- Detailed **issue inventory**, impact analysis, and before/after code (Part 1)  
- **Gaps & assumptions**, DDL commentary, and schema rationale (Part 2)  
- Full API endpoint design, edge cases, sample request/response, and business‑rule notes (Part 3)  

---

## Part 1: Code Review & Bug Fix (`code_review/`)

**What’s inside?**  
- **Original snippet** with annotations  
- **List of issues** (e.g. negative stock, missing SKU validation)  
- **Fixed `stock_service.js`** with validation for:
  - Non‑existent items  
  - Invalid quantities  
  - Preventing negative inventory  

**Quick test:**
```bash
cd code_review
node test.js
