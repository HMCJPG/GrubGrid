# GrubGrid

This is a simple Instagram-style application built with **FastAPI** for the backend and **React** for the frontend. It stores data in-memory for demonstration purposes.

## Features

- User authentication (signup, login)
- User profiles
- Upload posts with caption and image URL (image upload stub)
- Scrollable feed of recent posts
- Like posts and add comments

## Getting Started

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

The frontend expects the API to be running on `http://localhost:8000`.
