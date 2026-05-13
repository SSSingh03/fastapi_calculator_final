# FastAPI Calculator Final Project

## Overview

This project is a full-stack FastAPI calculator application that supports user authentication, calculation history management, profile updates, and secure password changes. The application uses FastAPI for backend development, SQLAlchemy for database integration, PostgreSQL for persistent storage, Docker for containerization, and GitHub Actions for CI/CD automation.

The final project feature implemented was a User Profile & Password Change system. Users can securely update their account information and change passwords using hashed password storage.

---

# Features

## Authentication

* User registration
* User login using JWT authentication
* Protected routes for authenticated users
* Secure password hashing using bcrypt

## Calculator Features

* Create calculations
* View saved calculations
* Edit calculations
* Delete calculations
* Store calculation history in PostgreSQL

## Profile Management

* Update username
* Update email
* Update first and last name
* Change password securely
* Password verification before updates

## Testing

* Unit tests
* Integration tests
* End-to-end Playwright tests
* Automated testing through GitHub Actions

## DevOps

* Docker containerization
* PostgreSQL database container
* GitHub Actions CI/CD pipeline
* DockerHub image deployment
* Security scanning with Trivy

---

# Technologies Used

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Docker
* Docker Compose
* JWT Authentication
* bcrypt
* Pytest
* Playwright
* GitHub Actions

---

# Project Structure

```text
app/
├── auth/
├── core/
├── models/
├── operations/
├── schemas/
├── main.py
├── database.py

templates/
├── dashboard.html
├── login.html
├── register.html
├── profile.html

tests/
├── unit/
├── integration/
├── e2e/
```

---

# Running the Application

## Clone the Repository

```bash
git clone https://github.com/SSSingh03/fastapi_calculator_final.git
cd fastapi_calculator_final
```

## Start Docker Containers

```bash
docker compose up --build
```

## Application URL

```text
http://localhost:8000
```

---

# Running Tests

## Run All Tests

```bash
docker compose exec web pytest -v
```

## Run Unit Tests

```bash
pytest tests/unit/
```

## Run Integration Tests

```bash
pytest tests/integration/
```

## Run E2E Tests

```bash
pytest tests/e2e/
```

---

# DockerHub Repository

[https://hub.docker.com/r/ssingh1119/fastapi_calculator_final](https://hub.docker.com/r/ssingh1119/fastapi_calculator_final)

---

# GitHub Repository

[https://github.com/SSSingh03/fastapi_calculator_final](https://github.com/SSSingh03/fastapi_calculator_final)

---

# CI/CD Pipeline

The GitHub Actions pipeline automatically:

* Runs unit, integration, and E2E tests
* Builds the Docker image
* Runs security scans using Trivy
* Pushes the Docker image to DockerHub

Pipeline jobs:

* test
* security
* deploy

---

# Security Features

* JWT-based authentication
* Password hashing with bcrypt
* Protected API routes
* Secure password update validation
* Security scanning through GitHub Actions

---

# Final Project Feature

The advanced feature implemented for this final project was User Profile Management and Password Change functionality.

Users can:

* View their profile information
* Update account details
* Change passwords securely
* Re-authenticate using the new password

This feature required backend route implementation, database updates, frontend integration, authentication handling, and automated testing.

---

# Learning Outcomes Addressed

* CLO3: Create Python applications with automated testing
* CLO4: Configure GitHub Actions for CI/CD automation
* CLO9: Apply Docker containerization techniques
* CLO10: Create and test REST APIs using FastAPI
* CLO11: Integrate SQL databases using SQLAlchemy
* CLO12: Validate JSON data with Pydantic
* CLO13: Implement secure authentication and authorization
