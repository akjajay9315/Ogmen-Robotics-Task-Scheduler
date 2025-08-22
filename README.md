# Ogmen-Robotics-Task-Scheduler
A full-stack Robot Task Scheduler built with Python FastAPI (backend) and vanilla JS/HTML (frontend) to manage devices, define tasks, schedule executions, and track execution logs. Supports real-time updates and easy device/task management.


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




