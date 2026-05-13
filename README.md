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
