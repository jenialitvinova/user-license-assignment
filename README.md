# User License Assignment

## Overview

This project automates Microsoft 365 license assignment for eligible users.

The solution is implemented in two ways:

- Python application compatible with Azure Functions
- n8n workflow

Both implementations use the same PostgreSQL database and follow the same business rules.

---

## Features

The application:

- imports users from a CSV file;
- stores users in PostgreSQL;
- retrieves users from the REST API;
- retrieves available licenses from the REST API;
- finds the required license by license code;
- skips users that do not exist;
- skips disabled users;
- skips users that already have the license assigned;
- assigns the Microsoft 365 E3 license;
- stores the processing result in PostgreSQL.

---

## Technologies

- Python 3.11
- Azure Functions
- PostgreSQL
- Docker
- Requests
- psycopg
- n8n

---

## Installation

### 1. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start PostgreSQL

```bash
docker compose up -d
```

### 4. Configure environment

Copy

```text
python/local.settings.example.json
```

to

```text
python/local.settings.json
```

and update the values if necessary.

---

## Environment Variables

The application uses the following environment variables:

| Variable | Description |
|----------|-------------|
| API_BASE_URL | REST API base URL |
| LICENSE_CODE | License code to assign |
| DB_HOST | PostgreSQL host |
| DB_PORT | PostgreSQL port |
| DB_NAME | Database name |
| DB_USER | Database user |
| DB_PASSWORD | Database password |

---

## Import Users

Import users from the CSV file into PostgreSQL:

```bash
cd python
python3 import_users.py
```

---

## Run the Python Application

```bash
python3 run.py
```

---

## Azure Functions

The Python implementation is compatible with Azure Functions.

Run locally:

```bash
func start
```

HTTP endpoint:

```
POST /api/process-licenses
```

---

## n8n Workflow

The project also contains an n8n implementation of the same business logic.

The workflow performs the following steps:

1. Read pending users from PostgreSQL.
2. Retrieve users from the REST API.
3. Retrieve available licenses.
4. Find the configured license.
5. Check whether the user exists.
6. Skip disabled users.
7. Skip users that already have the license.
8. Assign the license.
9. Update processing status in PostgreSQL.

Import the exported workflow into n8n and configure:

- PostgreSQL credentials
- REST API Base URL
- License code

---

## Processing Statuses

Each processed user receives one of the following statuses:

| Status | Description |
|---------|-------------|
| PENDING | Waiting for processing |
| ASSIGNED | License assigned successfully |
| ALREADY_ASSIGNED | User already has the license |
| DISABLED | User account is disabled |
| NOT_FOUND | User does not exist in the API |
| FAILED | Processing failed |

---

## Database

The PostgreSQL database stores:

- imported users;
- processing status;
- processing message;
- API user identifier;
- processing timestamp.

---

## Business Logic

For every pending user:

1. Load pending users from PostgreSQL.
2. Retrieve users from the REST API.
3. Retrieve available licenses.
4. Find the configured license.
5. Match users by UserPrincipalName.
6. Skip users that do not exist.
7. Skip disabled users.
8. Skip users that already have the required license.
9. Assign the license.
10. Update the processing result in PostgreSQL.

---

## AI Usage

AI tools were used during development for:

- code generation;
- debugging;
- documentation;
- workflow design;
- code review.

All generated code was manually reviewed, tested, and validated before being included in the final solution.