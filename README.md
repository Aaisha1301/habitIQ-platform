# HabitIQ – Personal Habit Analytics & Prediction Platform

HabitIQ is a personal habit management and analytics platform designed to help users build consistent habits, track their daily progress, and understand their behavioral patterns.

The platform provides a secure backend with user authentication, habit management, and habit logging. It is designed to support future analytics and AI-powered habit predictions.

---

## 🎯 Project Objectives

- Help users create and manage personal habits.
- Track daily habit completion.
- Maintain habit history and progress records.
- Provide secure user authentication and authorization.
- Prevent duplicate habit logs for the same habit on the same date.
- Build a foundation for habit analytics and AI-based predictions.

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Argon2 Password Hashing
- Pydantic

### Development & Testing
- Swagger UI
- Pytest *(planned for automated testing)*

### Frontend
- React
- TypeScript
- Tailwind CSS

---

## ✨ Implemented Features

### 1. User Authentication
- User registration.
- User login.
- JWT-based authentication.
- Password hashing using Argon2.
- Authenticated user profile retrieval.
- Active-user validation.

### 2. Habit Management
- Create a new habit.
- Retrieve the authenticated user's habits.
- Update existing habits.
- Delete habits.
- Associate habits with users and categories.

### 3. Habit Logs
- Record daily habit activity.
- Track habit status:
  - `completed`
  - `skipped`
  - `missed`
- Add optional notes to habit logs.
- Retrieve habit logs belonging to the authenticated user.
- Prevent duplicate logs for the same habit and date.

### 4. API Documentation
- Interactive API documentation using Swagger UI.
- API endpoints can be tested through the browser.

---

## 🗄️ Database Design

HabitIQ is designed around the following database entities:

| Table | Purpose |
|---|---|
| users | Stores user accounts and authentication-related information |
| habits | Stores habits created by users |
| categories | Organizes habits into categories |
| habit_logs | Stores daily habit activity and completion status |
| goals | Stores user habit goals |
| reminders | Stores habit reminder information |
| analytics | Stores habit analytics information |
| ai_predictions | Stores AI-based habit prediction information |

The database uses PostgreSQL, with SQLAlchemy models defining the application's data structure and relationships.

---

## 📂 Project Structure

```text
habitIQ-platform/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── users.py
│   │   │   ├── habits.py
│   │   │   └── habit_logs.py
│   │   │
│   │   ├── core/
│   │   │   ├── database.py
│   │   │   ├── dependencies.py
│   │   │   └── security.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── habit.py
│   │   │   ├── category.py
│   │   │   ├── habit_log.py
│   │   │   ├── goal.py
│   │   │   ├── reminder.py
│   │   │   ├── analytics.py
│   │   │   ├── ai_prediction.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── habit.py
│   │   │   └── habit_log.py
│   │   │
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── habit_service.py
│   │   │   └── habit_log_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
├── docs/
│   └── diagrams/
├── .github/
│   └── workflows/
├── .gitignore
└── README.md
```

---

## ⚙️ Installation and Setup

### Prerequisites

Make sure the following are installed:

- Python 3.10+
- PostgreSQL
- Node.js and npm *(for frontend development)*
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Aaisha1301/habitIQ-platform.git
```

Navigate to the project directory:

```bash
cd habitIQ-platform
```

### 2. Set Up the Backend

Navigate to the backend folder:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the `backend` directory using `.env.example` as a reference.

Configure the following variables:

```env
DATABASE_URL=postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@localhost:5432/habitiq_db

JWT_SECRET_KEY=YOUR_SECRET_KEY
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace the database placeholders with your local PostgreSQL credentials.

**Security:** Never commit your `.env` file, database password, JWT secret, or other credentials to GitHub.

### 4. Set Up PostgreSQL

Create a PostgreSQL database for the project:

```sql
CREATE DATABASE habitiq_db;
```

Configure the database connection in your `.env` file.

Ensure the configured database user has the required permissions.

### 5. Run the Backend

From the `backend` directory, run:

```bash
uvicorn app.main:app --reload
```

The backend should now be available at:

```text
http://127.0.0.1:8000
```

---

## 📖 API Documentation

Once the backend is running, access the interactive Swagger documentation:

**Swagger UI:**

http://127.0.0.1:8000/docs

**ReDoc:**

http://127.0.0.1:8000/redoc

---

## 🔌 API Endpoints

### General

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/api/health` | Health check |

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/users/register` | Register a new user |
| POST | `/api/users/login` | Authenticate a user and obtain an access token |
| GET | `/api/users/me` | Retrieve the authenticated user's profile |

### Habits

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/habits/` | Create a habit |
| GET | `/api/habits/` | Retrieve the authenticated user's habits |
| PUT | `/api/habits/{habit_id}` | Update a habit |
| DELETE | `/api/habits/{habit_id}` | Delete a habit |

### Habit Logs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/habits/{habit_id}/logs` | Create a habit log |
| GET | `/api/habits/logs` | Retrieve the authenticated user's habit logs |

Protected endpoints require a valid JWT access token.

---

## 🧪 Testing

The implemented authentication, habit management, and habit logging endpoints have been tested through Swagger UI.

Verified scenarios include:

- Successful user registration and login.
- Rejection of invalid login credentials.
- Authenticated profile retrieval.
- Habit creation, retrieval, updating, and deletion.
- Successful habit log creation.
- Habit log retrieval.
- Duplicate habit log rejection with HTTP `409 Conflict`.

Automated testing with Pytest is part of the planned development work.

---

## 🚀 Future Enhancements

The following capabilities are planned for future development:

- Habit log update and deletion APIs.
- Habit streak calculation.
- Progress dashboards and habit statistics.
- Goal tracking and reminders.
- AI-powered habit completion predictions.
- Personalized habit recommendations.
- Frontend integration with the backend APIs.
- Automated testing and CI/CD integration.
- Cloud deployment.

---

## 🔐 Security

HabitIQ incorporates the following security measures:

- Password hashing using Argon2.
- JWT-based authentication.
- Protected API endpoints.
- User-specific data access.
- Environment variables for sensitive configuration.

---

## 👨‍💻 Developer

**M. AAISHA BANU**

B.Tech – Artificial Intelligence and Data Science

J.J. College of Engineering and Technology

---

## 📌 Project Status

**Currently in development.**

The backend foundation, user authentication, habit management, and basic habit logging functionality have been implemented and tested.

More features will be added as development progresses.

---

## 📄 License

No license has been specified yet.
