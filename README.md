# Ogmen-Robotics-Task-Scheduler
A full-stack Robot Task Scheduler built with Python FastAPI (backend) and vanilla JS/HTML (frontend) to manage devices, define tasks, schedule executions, and track execution logs. Supports real-time updates and easy device/task management.

## Approch followed
Created a repository Ogmen-Robotics-Task-Scheduler with separate backend and frontend directories.

Set up the backend using FastAPI and configured Uvicorn to run the server.

Designed database models for Devices, Tasks, Schedules, and Logs using SQLAlchemy.

Configured Alembic for database migrations and schema management.

Implemented API endpoints for: listing and adding devices, task definitions, scheduling tasks, executing tasks, and fetching execution logs.

Built a frontend dashboard (tasks.html) to view devices, task definitions, schedules, and logs.

Developed app.js to interact with backend APIs and update the frontend dynamically.

Added polling every 5 seconds on the frontend to fetch real-time schedules and logs.

Created a Python virtual environment and installed dependencies using requirements.txt.

Ran Alembic migrations to create tables in the database.

Used PostgreSQL and DBeaver for local database testing and Postman for api testing.

Started the backend on http://localhost:8000 and frontend on http://localhost:5500/tasks.html.

Tested API endpoints and ensured proper functionality of task scheduling, execution, and logging.

Verified that the frontend displayed tasks, schedules, and logs in real-time correctly.

## ⚡ Quick Start

### 1. Clone Repo

git clone https://github.com/akjajay9315/Ogmen-Robotics-Task-Scheduler.git
cd Ogmen-Robotics-Task-Scheduler/backend

### 2. Create Virtual Environment & Install Dependencies

python -m venv .venv

# Activate virtual environment:

# Linux/macOS:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

pip install -r requirements.txt


### 3. Run Database Migrations


alembic upgrade head

### 4. Start Backend

uvicorn app.main:app --reload


API will be available at [http://localhost:8000](http://localhost:8000).

### 5. Run Frontend

cd ../frontend
python -m http.server 5500


Frontend will be available at [http://localhost:5500/tasks.html](http://localhost:5500/tasks.html).

## 🌐 API Endpoints

* GET /devices/ — List all devices
* POST /devices/ — Add a device
* GET /tasks/definitions/ — List task definitions
* POST /tasks/definitions/ — Add a task definition
* GET /tasks/{device_id}/scheduled/ — Get scheduled tasks for a device
* POST /tasks/{device_id}/schedule/ — Schedule a task
* GET /tasks/{device_id}/logs/ — Get execution logs for a device
* POST /tasks/{schedule_id}/execute/ — Execute a scheduled task


## 📦 Frontend

* tasks.html — Main dashboard
* app.js — JS logic for fetching devices, definitions, schedules, and logs
* Polling every 5s to update schedules and logs automatically




