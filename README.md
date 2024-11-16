<!-- GETTING STARTED -->
## About The Project
This Task Management API allows users to create, update, delete, and view tasks. Each task includes a title, description, due date, and status. Users can view all tasks or filter them by status.
## Setup Guide

Follow these steps to set up the project locally:

### Prerequisites

Ensure Python and PostgreSQL are installed, or use a cloud database.

**Install Python:**

```sh
sudo apt-get update
sudo apt-get install python3.8
```

**Install PostgreSQL and create a database:**

```sh
sudo apt install postgresql postgresql-contrib
sudo -u postgres
psql
CREATE USER <USER_NAME> WITH PASSWORD <PASSWORD>;
CREATE DATABASE <DATABASE_NAME> WITH OWNER <USER_NAME>;
```

### Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/hgpnguyen/task_management.git
   ```
2. **Set up a virtual environment:**
    ```sh
    pip install virtualenv
    python3 -m venv <virtual-environment-name>
    source <virtual-environment-name>/bin/activate
    ```
3. **Install required packages:**
    ```sh
    pip install -r requirements.txt
    ```
4. **Create a `.env` file in the same folder as `manage.py` with database credentials:**
    ```sh
    DB_NAME='task_management'
    DB_USER='hgpnguyen'
    DB_PASS='******'
    DB_HOST='localhost'
    DB_PORT=5432
    ```
5. **Migrate the database:**
    ```sh
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```
6. **Start the server:**
    ```sh
    python3 manage.py runserver
    ```
7. **Send request to `http://127.0.0.1:8000/tasks/`**

## Usage
Endpoint for creating, viewing, and filtering tasks:
```sh
/tasks/?[status_filter]&[page]&[page_size]
```
1. `[status_filter]`(optional): Filters tasks by status ('Pending' or 'Completed'). Accepts variations like 'p', 'c', 'pending', or 'completed'. Invalid or empty values return all tasks.
2. `[page]`(optional): Specifies the page number for pagination (default is 1).
2. `[page_size]`(Optional): Specifies the page size for pagination (default is 10).

### Request Method
| Method   | Description                              |
| -------- | ---------------------------------------- |
| `GET`    | Retrieve a list of filtered tasks. |
| `POST`   | Create a new task. |

### Examples
| Method   | URL                                   | Description                              |
| -------- | --------------------------------------| ---------------------------------------- |
| `GET`    | `/tasks/`                             | Retrieve page 1 of all tasks (page size 10).                     |
| `POST`   | `/tasks/`                             | Create a new task.                       |
| `GET`    | `/tasks/?status=c`                          | Retrieve page 1 of 'completed' tasks (page size 10).10.                       |
| `GET`    | `/tasks/?status=pending&page_size=5`                          |Retrieve page 1 of 'pending' tasks (page size 5).                 |


Endpoint for viewing, updating, and deleting a specific task:
```sh
/tasks/{task_id}/
```
- `{task_id}`: The ID of the task.

### Request Method
| Method   | Description                              |
| -------- | ---------------------------------------- |
| `GET`    | Retrieve a single task. |
| `PUT`   | Update a task. |
| `DELETE`| Delete a task.

### Examples
| Method   | URL                                   | Description                               |
| -------- | --------------------------------------| ------------------------------------------|
| `GET`    | `/tasks/1/`                           | Retrieve task #1.                         |
| `PUT`    | `/tasks/2/`                           | Updated task #2.                  |
| `DELETE` | `/tasks/3/`                           | Deleted task #3.                          |

## Explanation & Justification
- Model `Task`:
    - `title = models.CharField(max_length=100, blank=False)`: Limits the length of title to 100 and makes this field a required.
    - `description = models.TextField(blank=True)`: Allows an optional description.
    - `due_date = models.DateField(blank=False)`: Required to indicate the task's completion date.
    - `status = models.CharField(max_length=1, choices=[('P', 'Pending'), ('C', 'Completed')], blank=False)`: Stores task status as 'P' or 'C' to save database space.
- The use of `TaskViewSerializer`: Ensures the response displays 'Pending' or 'Completed' for readability instead of 'P' or 'C'.
- `TaskSerializer`: Usefield `status = serializers.CharField(max_length=10)` and `validate_status(self, status)` to accept variations like 'p', 'c', 'pending', or 'completed' and convert them to 'P' and 'C' for flexibility.
- Endpoint `/tasks/?[status_filter]&[page]&[page_size]`: Supports task filtering by status with paginated results.
## Room for improvement
1. Add partial update capability (currently supports only full updates).
2. Ensure consistent pagination results (current pagination yields inconsistencies with unordered lists).
3. Implement test cases for the API.