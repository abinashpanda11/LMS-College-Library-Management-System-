# 📚 Library Manager Web App

A full-stack web application built using Python (Flask) to streamline college library operations. It replaces manual registers and spreadsheet tracking with role-based dashboards for administrators and students, complete with borrowing records, fine calculations, and automated email verification.

---

## 🚀 Features

### 👨‍💼 Admin Dashboard
* **Book Management:** Add, update, view, and bulk-delete books. Supports importing book lists via CSV.
* **Borrowing & Returns:** Issue books to students, log returns, and monitor overdue status.
* **User Management:** View registered students and handle account statuses.
* **Payment Records:** Track library fees, overdue fines, and payment transaction logs.

### 🎓 Student Portal
* **Catalog Search:** Real-time book search and availability check.
* **Borrowing History:** View currently borrowed titles, due dates, and return history.
* **Payments & Dues:** Check accumulated fines and payment receipts.

### 🔐 Authentication & Security
* Role-based access control (Admin vs. Student).
* Email verification upon registration and secure password reset flow.
* Password hashing using Werkzeug / bcrypt.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite (local development) / PostgreSQL (Neon / production) via SQLAlchemy ORM
* **Frontend:** HTML5, CSS3, JavaScript
* **Containerization & Deployment:** Docker, Vercel

---

## 📂 Project Structure

```text
library_manager_flask/
├── app.py                 # Application entry point & route definitions
├── config.py              # App configuration & environment variables
├── requirements.txt       # Project dependencies
├── Dockerfile             # Docker container configuration
├── static/                # CSS, JavaScript, and uploaded media
├── templates/             # HTML templates (Admin & Student views)
└── instance/              # Local SQLite database
