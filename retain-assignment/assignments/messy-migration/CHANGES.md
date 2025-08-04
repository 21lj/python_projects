# CHANGES.md

## 🚀 Overview
This project is a complete refactor of a legacy Flask + SQLite user management API into a modern, production-ready **FastAPI** stack. The goal was to preserve functionality while improving **security**, **code quality**, **structure**, and **maintainability**.

---

## 🔍 Critical Issues Identified

| Category        | Problem                                                                 |
|----------------|-------------------------------------------------------------------------|
| ❌ Security     | - SQL Injection due to raw queries<br>- Passwords stored as plain text<br>- No input validation or sanitation |
| ⚠️ Code Quality | - Single-file monolithic structure<br>- Tightly coupled logic and routing<br>- No error handling<br>- No consistent status codes |
| 🔧 Maintainability | - No separation of concerns<br>- Hard to test, debug, or extend<br>- Logic, data, and transport layers intermixed |

---

## ✅ Refactor Summary

| Area            | Old                            | New                                    |
|------------------|----------------------------------|-----------------------------------------|
| Framework        | Flask                          | FastAPI                                 |
| DB Access        | sqlite3 + raw SQL              | SQLAlchemy ORM                          |
| Security         | None                           | bcrypt-hashed passwords + parameterized queries |
| Validation       | `json.loads()`                 | Pydantic Schemas                        |
| Error Handling   | None                           | FastAPI’s HTTPException + proper codes  |
| Structure        | Single file                    | Modular `app/` package layout           |
| Testing          | Manual                         | Auto-reload + clean API routes          |
| API Output       | Raw strings                    | JSON response models with `orm_mode`    |

---

## 🧱 Architecture Decisions

- Chose **FastAPI** for its automatic docs, type-checking, and async readiness.
- Used **SQLAlchemy ORM** for safe and scalable DB interactions.
- Employed **Pydantic** for request/response validation and parsing.
- Passwords are now securely stored using **bcrypt** via `passlib`.
- All database interactions routed through a **CRUD abstraction layer**.
- Routes isolated into modular **routers** for maintainability and scalability.

---

## 🔁 Trade-offs / Assumptions

- Chose SQLite for simplicity; for production, migrate to PostgreSQL or similar.
- Authentication was kept minimal (username/password check); JWT or OAuth can be added if required.
- No frontend/UI was added, in line with challenge guidelines.
- Did not aim for 100% test coverage due to scope constraints.

---

## 🧠 If I Had More Time

- Add JWT-based token auth for login sessions.
- Add pagination and sorting for user listing.
- Add proper unit and integration tests with `pytest`.
- Containerize with Docker + `.env` file for configuration.
- Add async support to DB calls via `async SQLAlchemy` or `Tortoise ORM`.

---

## 🤖 AI Usage Disclosure

- **Tool Used:** ChatGPT (GPT-4)
- **Purpose:** Refactoring strategy, module design, security improvements, and code generation
- **Edits:** All AI-generated code was reviewed, tested, and in some cases rewritten to improve clarity or efficiency.

---
