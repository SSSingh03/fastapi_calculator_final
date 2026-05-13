# FastAPI Calculator Final Project

## Overview

This project is a full-stack FastAPI calculator application with user authentication, calculation history management, profile updates, and secure password change functionality.

The application uses FastAPI for the backend, SQLAlchemy for database integration, PostgreSQL for persistent storage, Docker for containerization, and GitHub Actions for CI/CD automation.

The advanced final project feature is User Profile Management and Password Change. Authenticated users can update their profile information and securely change their password.

---

## Features

### Authentication

- User registration
- User login
- JWT-based authentication
- Protected API routes
- Secure password hashing

### Calculator Functionality

- Create calculations
- View saved calculations
- Edit calculations
- Delete calculations
- Store calculation history in PostgreSQL

### Profile Management

- View profile information
- Update username
- Update email
- Update first and last name
- Change password securely
- Re-login with the updated password

### Testing

- Unit tests
- Integration tests
- E2E/API workflow tests
- Automated testing through GitHub Actions

### DevOps

- Dockerized FastAPI application
- PostgreSQL database container
- GitHub Actions CI/CD pipeline
- DockerHub deployment
- Security scanning with Trivy

---

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT Authentication
- bcrypt
- Docker
- Docker Compose
- Pytest
- Playwright
- GitHub Actions
- DockerHub
- Trivy

---

## Project Structure

```text
app/
├── auth/
├── core/
├── models/
├── operations/
├── schemas/
├── database.py
├── database_init.py
└── main.py

templates/
├── dashboard.html
├── edit_calculation.html
├── index.html
├── layout.html
├── login.html
├── profile.html
├── register.html
└── view_calculation.html

tests/
├── unit/
├── integration/
└── e2e/

.github/
└── workflows/
    └── test.yml
```

---

## Running the Application

Clone the repository:

```bash
git clone https://github.com/SSSingh03/fastapi_calculator_final.git
cd fastapi_calculator_final
```

Start the application:

```bash
docker compose up --build
```

Open the application:

```text
http://localhost:8000
```

Initialize the database tables if needed:

```bash
docker compose exec web python -c "from app.database import Base, engine; from app.models.user import User; from app.models.calculation import Calculation; Base.metadata.create_all(bind=engine)"
```

---

## Running Tests

Run all tests:

```bash
docker compose exec web pytest -v
```

Run unit tests:

```bash
docker compose exec web pytest tests/unit/ -v
```

Run integration tests:

```bash
docker compose exec web pytest tests/integration/ -v
```

Run E2E tests:

```bash
docker compose exec web pytest tests/e2e/ -v
```

Current result:

```text
103 passed, 1 skipped
```

---

## GitHub Actions CI/CD

The GitHub Actions pipeline automatically:

- Runs tests
- Performs security scans
- Builds the Docker image
- Pushes the image to DockerHub

Pipeline status:

```text
test: pass
security: pass
deploy: pass
```

---

## DockerHub Repository

```text
https://hub.docker.com/r/ssingh1119/fastapi_calculator_final
```

---

## GitHub Repository

```text
https://github.com/SSSingh03/fastapi_calculator_final
```

---

## Final Project Feature

The advanced feature implemented for this project is User Profile Management and Password Change functionality.

Authenticated users can:

- Update profile information
- Change passwords securely
- Re-authenticate using updated credentials

The feature includes backend route handling, frontend integration, database updates, validation, authentication, and automated testing.

---

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Protected routes
- Password verification before updates
- GitHub Actions security scanning with Trivy

---

## Learning Outcomes Addressed

- CLO3: Create Python applications with automated testing
- CLO4: Configure GitHub Actions for CI/CD automation
- CLO9: Apply Docker containerization techniques
- CLO10: Create and test REST APIs using FastAPI
- CLO11: Integrate SQL databases using SQLAlchemy
- CLO12: Validate JSON data using Pydantic
- CLO13: Implement secure authentication and authorization
