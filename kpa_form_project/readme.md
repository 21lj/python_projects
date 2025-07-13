
# 🚆 KPA Form API

This project implements two endpoints from the **KPA Form Postman Collection** using **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. It allows submission and retrieval of `wheel-specifications` form data.

---

## 📦 Tech Stack

- **Backend**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Testing**: REST Client (`test.http`) or Postman
- **Environment**: Python 3.10+

---

## ✅ Implemented Endpoints

### 1. `POST /api/forms/wheel-specifications`

Submits wheel specification data to the server.

**Sample Request Body:**
```json
{
  "formNumber": "WHEEL-2025-001",
  "submittedBy": "user_id_123",
  "submittedDate": "2025-07-03",
  "fields": {
    "treadDiameterNew": "915 (900-1000)",
    "lastShopIssueSize": "837 (800-900)",
    "condemningDia": "825 (800-900)",
    "wheelGauge": "1600 (+2,-1)",
    "variationSameAxle": "0.5",
    "variationSameBogie": "5",
    "variationSameCoach": "13",
    "wheelProfile": "29.4 Flange Thickness",
    "intermediateWWP": "20 TO 28",
    "bearingSeatDiameter": "130.043 TO 130.068",
    "rollerBearingOuterDia": "280 (+0.0/-0.035)",
    "rollerBearingBoreDia": "130 (+0.0/-0.025)",
    "rollerBearingWidth": "93 (+0/-0.250)",
    "axleBoxHousingBoreDia": "280 (+0.030/+0.052)",
    "wheelDiscWidth": "127 (+4/-0)"
  }
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Wheel specification submitted successfully.",
  "data": {
    "formNumber": "WHEEL-2025-001",
    "submittedBy": "user_id_123",
    "submittedDate": "2025-07-03",
    "status": "Saved"
  }
}
```

---

### 2. `GET /api/forms/wheel-specifications`

Retrieves form data based on filters.

**Query Parameters:**
- `formNumber`
- `submittedBy`
- `submittedDate`

**Example:**
```
GET /api/forms/wheel-specifications?formNumber=WHEEL-2025-001&submittedBy=user_id_123&submittedDate=2025-07-03
```

**Success Response:**
```json
{
  "success": true,
  "message": "Filtered wheel specification forms fetched successfully.",
  "data": [ { ... } ]
}
```

---

## 🧪 Local Testing

### ✅ Run Server
```bash
uvicorn app.main:app --reload
```

### 🧪 Test Using REST Client (VS Code)

Use the included `test.http` file to send API requests inside VS Code.

Or, import the original Postman collection and hit the `localhost` endpoints.

---

## 🛠 Setup Instructions

### 1. Clone this Repo
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>/kpa_form_api
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a database:

```sql
CREATE DATABASE kpa_db;
```

Then update `.env`:

```env
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/kpa_db
```

### 5. Run Migrations (create tables)
```bash
uvicorn app.main:app --reload
```

---

## 📁 Project Structure

```
kpa_form_api/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   ├── crud.py
│   └── routes.py
├── test.http
├── .env
└── README.md
```

---

