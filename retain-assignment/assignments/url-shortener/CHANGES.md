# CHANGES.md

## 🚀 Overview

This project implements a minimal URL shortening service similar to Bitly or TinyURL, using **Flask**, **in-memory storage**, and **pytest** for testing. It supports shortening URLs, redirecting with click tracking, and analytics.

---

## ✅ Features Implemented

| Feature | Endpoint | Description |
|--------|----------|-------------|
| Health check | `GET /` | Confirms the service is live |
| Shorten URL | `POST /api/shorten` | Accepts a long URL, returns a short code |
| Redirect | `GET /<short_code>` | Redirects to the original URL, tracks clicks |
| Analytics | `GET /api/stats/<short_code>` | Returns click count, creation time, and original URL |

---

## 🔧 Design Decisions

- **In-Memory Store**: Used a global dictionary (`url_store`) for simplicity and fast lookups. No external DB.
- **Short Code Generation**: Random 6-character alphanumeric using `random.choices()`.
- **URL Validation**: Regex-based validator ensures proper scheme and domain.
- **Error Handling**: All endpoints return consistent JSON errors with status codes.
- **Testability**: Built with `pytest` and Flask’s test client. Store is cleared before each test.

---

## 🧪 Tests Written (`tests/test_core.py`)

- ✅ Health check works
- ✅ Valid URL shortening
- ✅ Invalid URL returns 400
- ✅ Redirection works and increments click count
- ✅ 404 for invalid short codes
- ✅ Stats endpoint returns correct info

---

## 🤖 AI Usage Disclosure

- **Tool Used**: ChatGPT (GPT-4)
- **Usage**:
  - Designing architecture and modular file structure
  - Writing initial implementations and tests
  - Explaining decisions and summarizing in `CHANGES.md`
- **Human Review**: All code reviewed, verified, and tested manually.

---

## 🧠 If More Time…

- Add expiration for short codes
- Add concurrency lock/thread-safe store
- Switch to persistent storage (SQLite, Redis)
- Add Docker + CI integration
