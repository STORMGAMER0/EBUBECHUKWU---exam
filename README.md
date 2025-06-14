# Event Management API System

A simple FastAPI-based API for managing users, events, and registrations.

## Features

- Create, read, update, and delete users and events
- Activate/deactivate users
- Register users for events
- Mark attendance
- List users who attended events
- Full test coverage using `pytest`

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/STORMGAMER0/EBUBECHUKWU---exam.git
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
uvicorn main:app --reload
```

### 5. Run Tests

```bash
pytest
```
